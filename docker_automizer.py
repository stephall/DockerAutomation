# docker_automizer.py

# Import modules
import os
import re
import subprocess
import random
import string
import hashlib
import base64
import dockerfile_templates
from pathlib import Path

class DockerAutomizer(object):
    def __init__(self):
        pass

        # Define the docker alias as class attribute
        #self.docker_alias = '/usr/local/bin/docker'

    ##################################################################
    # Interface methods
    ##################################################################
    def generate_dockerfile(self, **kwargs):
        """ Generate a Dockerfile in the current directory. """
        # Parse the kwargs
        # Template
        template = 'jupyter'
        if 'template' in kwargs:
            template = kwargs['template']

        # Python version
        version = '3.9'
        if 'version' in kwargs:
            version = kwargs['version']

        # Python modules
        modules = 'numpy matplotlib pandas scipy'
        if 'modules' in kwargs:
            version = kwargs['modules']

        # Get the string of the Dockerfile template
        dockerfile_str = dockerfile_templates.get_template(template)

        # Substitute/Replace the marked parts of the templated with their
        # corresponding inputs
        dockerfile_str = re.sub(r'{{ python_version }}', version, dockerfile_str)
        dockerfile_str = re.sub(r'{{ python_modules }}', modules, dockerfile_str)

        # Store the Dockerfile in the current directory
        with open('Dockerfile', 'w') as f:
            f.write(dockerfile_str)

    def build_image(self):
        """ Build a docker image based on the Dockerfile in the current directory. """
        # Check that there exists a Dockerfile in the current directory
        if not os.path.isfile(Path(os.getcwd(), 'Dockerfile')):
            err_msg = f"Can't build image because there exists no Dockerfile in the current directory."
            raise FileNotFoundError(err_msg)

        # Get the name of the image
        image_name = self._get_image_name()

        # Construct the shell command to run the container
        docker_shell_command = 'docker build -t ' + image_name + ' .'

        # Execute the shell command
        self._exec_shell_command(docker_shell_command)

    def run(self, port='8888'):
        """ Run the container associated with the docker image associated with the current directory. """
        # Get the name of the docker image associated with the current directory
        image_name = self._get_image_name()

        # Generate the jupyter token
        jupyter_token = self._generate_jupyter_token()

        # Construct the shell command to run the container
        # Remark: We provide the (local) port (of the computer), and the generated security token
        docker_shell_command = 'docker run -it --rm -p ' + port + ':8888 -e JUPYTER_TOKEN=' + jupyter_token + ' -v "${PWD}":/home/lab ' + image_name

        # Print the shell command
        print(docker_shell_command)

        # Define a shell command to open Jupyter Notebook in the browser
        # Remark: 1) Wait some seconds before opening the Jupyter Notebook.
        #         2) We need to pass the jupyter token.
        open_browser_shell_command = 'sleep 7; open -a "Google Chrome" http://127.0.0.1:8888/lab?token=' + jupyter_token

        # Run the subprocesses
        processes = [
            subprocess.Popen(docker_shell_command, shell=True), 
            subprocess.Popen(open_browser_shell_command, shell=True),
        ]

        # Collect process statuses
        exitcodes = [p.wait() for p in processes]

    def exec(self, exec_command):
        """
        Run the container, which is associated with the docker image associated 
        with the current directory), and execute a command within this container.
        """
        # Get the name of the docker image associated with the current directory
        image_name = self._get_image_name()

        # Construct the shell command to run the container and execute a command
        # Remark: We provide the (local) port (of the computer), and the generated security token
        docker_shell_command = 'docker run -it --rm -v "${PWD}":/home/lab ' + image_name + ' ' + exec_command

        # Run the subprocesses
        self._exec_shell_command(docker_shell_command)

    def display_image_name(self):
        """ Display how docker images are named in the current directory. """
        # Get the name of the docker image associated with the current directory
        # and print it
        print(self._get_image_name())

    def remove_image(self):
        """ Remove the docker image associated with the current directory. """
        # Get the name of the docker image associated with the current directory
        image_name = self._get_image_name()

        # Construct the shell command to run the container
        docker_shell_command = 'docker rmi ' + image_name

        # Execute the shell command
        self._exec_shell_command(docker_shell_command)

    ##################################################################
    # Internal methods
    ##################################################################
    def _exec_shell_command(self, shell_command):
        """ Execute a shell command as subprocess. """
        # Print the shell command
        print(shell_command)

        # Run the shell command as subprocess
        process = subprocess.Popen(shell_command, shell=True)

        # Collect the process status
        process.wait()

    def _get_image_name(self):
        """ Get the name of the image associated with the current directory. """
        # Get the name of the current directory
        dir_name = os.path.basename( os.getcwd() )

        # In case that the directory name contains at least one underscore it is assumed 
        # to be in 'Snake_Case' and otherwise in 'CamelCase'.
        if '_' in dir_name:
            # Construct the image name by mapping the directory name from 'Snake_Case'
            # to 'kebab-case'.
            image_name = self._map_snake_to_kebab_case(dir_name)
        else:
            # Construct the image name by mapping the directory name from 'CamelCase'
            # to 'kebab-case'.
            image_name = self._map_camel_to_kebab_case(dir_name)

        # Get a (hexadecimal) hash of the current (absolute) directory path as string
        dir_hash = self._get_dir_hash()

        # Prefix the docker image by 'stephall/' and postfix it by the directory hash
        # Remark: We add the hash just in case that a project (directory containing
        #         the Dockerfile) might be named like an already existing one.
        return 'stephall/' + image_name + '/' + dir_hash

    def _map_snake_to_kebab_case(self, dir_name):
        """ Map a directory name in 'Snake_Case' to 'kebab-case'."""
        # Replace '_' in the directory name by '-' to obtain the image name
        image_name = re.sub('_', '-', dir_name)

        # Only use lowercase characters
        image_name = image_name.lower()

        return image_name

    def _map_camel_to_kebab_case(self, dir_name):
        """ Map a directory name in 'CamelCase' to 'kebab-case'."""
        # If there are upper case letters, split the directory name s.t.
        # these uppercased words are separated.
        dir_name_split = re.findall('[A-Z][^A-Z]*', dir_name)

        # Loop over the splitted items and create the image name for
        # the current directory.
        # Remark: We turn CamelCase to kebab-case.
        #         E.g. 'FolderName' becomes 'folder-name', 'BestAPI' becomes 'best-api', or 'MLProject' becomes 'ml-project'.
        image_name = ''
        for counter, item in enumerate( dir_name_split ):
            # In case the current item is not the first one and consists
            # out of more than one character, prepend a '-' character
            if 0<counter and 1<len(item):
                image_name += '-'

            # Append the current item
            image_name += item

            # In case the current item is not the last one and consists
            # out of more than one character, append a '-' character
            if counter<len(dir_name_split)-1 and 1<len(item):
                image_name += '-'

        # Replace '--' by '-'
        image_name = re.sub('--', '-', image_name)

        # Only use lowercase characters
        image_name = image_name.lower()

        return image_name

    def _generate_jupyter_token(self, length=20):
        """ Generate a jupyter token. """
        # Define the set of chars
        chars = string.ascii_letters + string.digits
    
        # Randomly sample from the set of chars to obtain a string of the requested length
        jupyter_token = ''.join(random.choice(chars) for _ in range(length))

        return jupyter_token

    def _get_dir_hash(self):
        """ Return the hexadecimal md5 hash of the current absolute directory path as string. """
        # First byte encode the current working directory (using 'ascii' encoding)
        byte_cwd = bytes(os.getcwd(), 'ascii')

        # Second, hash it using the 'md5' hash algorithm of the hashlib module
        # and return it as hexadecimal number
        dir_hash = hashlib.md5( byte_cwd ).hexdigest()

        # Finally, make this hash a string and return it
        # Remark: Use only the first 10 characters, which will of course increase
        #         the chance for collisions...
        return str( dir_hash[:10] )

