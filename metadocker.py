# metadocker.py

# Import modules
import argparse
from docker_automizer import DockerAutomizer

# Define some general settings
expected_commands = {
    'init':  'Create a new Dockerfile.',
    'build': 'Build an image with the name of the current folder based on a Dockerfile (in the current folder).',
    'run':   'Run the container of the image built from the Dockerfile in the current directory.',
    'image': 'Display the name of the docker image associated with the current directory.',
    'remove': 'Remove the docker image associated with the current directory.',
}

# Generate the help text for the 'command' argument
help_text_command = 'Meta command. Options: '
for command, description in expected_commands.items():
    help_text_command += f"({command}) {description}\n"

# Only allow this file to be run as script
if __name__!='__main__':
    err_msg = f"The Python script 'metadocker.py' can only be run from command line (as '__main__')!"
    raise ValueError(err_msg)

# Intialize the argument partser object
parser = argparse.ArgumentParser(description="Automate 'Docker' workflow.")
parser.add_argument('command', type=str, help=help_text_command)
#parser.add_argument('--sum', dest='accumulate', action='store_const',
#                    const=sum, default=max,
#                    help='sum the integers (default: find the max)')

# Parse the arguments
args = parser.parse_args()

# Check the input arguments
if args.command not in expected_commands:
    err_msg = f"The first argument of 'metadocker' must be a (meta) 'command' corresponding to one of the following:\n{list(expected_commands)}."
    raise ValueError(err_msg)

# Differ cases depending on the commands
automizer = DockerAutomizer()

# Call the class method of the docker automizer object corresponding to the passed command
if args.command=='init':
    automizer.generate_dockerfile()
elif args.command=='build':
    automizer.build_image()
elif args.command=='image':
    automizer.display_image_name()
elif args.command=='remove':
    automizer.remove_image()
else: # Must be 'run' in this case (checked commands already above)
    automizer.run()



