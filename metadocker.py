# metadocker.py

# Import modules
import argparse
from docker_automizer import DockerAutomizer

# Define some general settings
expected_commands = {
    'init':   'Create a new Dockerfile.',
    'build':  'Build an image with the name of the current folder based on a Dockerfile (in the current folder).',
    'run':    'Run the container of the image built from the Dockerfile in the current directory.',
    'exec':   'Run the container of the image built from the Dockerfile in the current directory and execute a passed command within this container.',
    'image':  'Display the name of the docker image associated with the current directory.',
    'remove': 'Remove the docker image associated with the current directory.',
}

# Generate the help text for the 'command' argument
help_text_command = 'Meta command. Options: '
for command, description in expected_commands.items():
    help_text_command += f"({command}) {description}\n"

# Generate the help text for the additional argument
help_text_additional = "Extra arguments that can be passed in addition to some of the 'commands'."

# Only allow this file to be run as script
if __name__!='__main__':
    err_msg = f"The Python script 'metadocker.py' can only be run from command line (as '__main__')!"
    raise ValueError(err_msg)

# Intialize the argument partser object
parser = argparse.ArgumentParser(description="Automate 'Docker' workflow.")
parser.add_argument('command', type=str, help=help_text_command)
parser.add_argument('additional', type=str, help=help_text_additional, nargs='*')

# Parse the arguments
args = parser.parse_args()

def check_additional_arguments(args, checking_mode):
    """ Check that no additional arguments were passed and throw an error if they were. """
    # Handle different checking modes
    if checking_mode=='no_additional_arguments':
        # Remark: The additional arguments (args.additional) are stored as list of strings.
        if 0<len(args.additional):
            err_msg = f"In case the (meta) command is '{args.command}' no additional arguments are expected, but got the additional arguments: {args.additional}"
            raise ValueError(err_msg)
    elif checking_mode=='at_least_one_additional_argument':
        # Remark: The additional arguments (args.additional) are stored as list of strings.
        if 0==len(args.additional):
            err_msg = f"In case the (meta) command is '{args.command}' at least one additional argument is expected, but no were passed."
            raise ValueError(err_msg)
    else:
        err_msg = f"The input 'checking_mode' was '{checking_mode}', which is not one of the expected checking modes."
        raise ValueError(err_msg)

# Differ cases depending on the commands
automizer = DockerAutomizer()

# Call the class method of the docker automizer object corresponding to the passed command
if args.command=='init':
    # Check the additional arguments
    check_additional_arguments(args, checking_mode='no_additional_arguments')

    # Call the corresponding method of the automizer
    automizer.generate_dockerfile()
elif args.command=='build':
    # Check the additional arguments
    check_additional_arguments(args, checking_mode='no_additional_arguments')

    # Call the corresponding method of the automizer
    automizer.build_image()
elif args.command=='image':
    # Check the additional arguments
    check_additional_arguments(args, checking_mode='no_additional_arguments')

    # Call the corresponding method of the automizer
    automizer.display_image_name()
elif args.command=='remove':
    # Check the additional arguments
    check_additional_arguments(args, checking_mode='no_additional_arguments')

    # Call the corresponding method of the automizer
    automizer.remove_image()
elif args.command=='run':
    # Check the additional arguments
    check_additional_arguments(args, checking_mode='no_additional_arguments')

    # Call the corresponding method of the automizer
    automizer.run()
elif args.command=='exec':
    # Check the additional arguments
    check_additional_arguments(args, checking_mode='at_least_one_additional_argument')

    # Combine the additional arguments to a string using spaces (' ') between additional arguments
    # to obtain the command to be executed within the container.
    exec_command = " ".join(args.additional)
    
    # Run the corresponding method of the automizer, while passing the exec_command as argument.
    automizer.exec(exec_command)
else:
    err_msg = f"The first argument of 'metadocker' must be a (meta) 'command' corresponding to one of the following:\n{list(expected_commands)}."
    raise ValueError(err_msg)
