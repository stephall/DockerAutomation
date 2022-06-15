# dockerfile_templates.py

# Define Dockerfile templates
jupyter_template = """
# Define the python base image
FROM python:{{ python_version }}

# Expose (container internal) port 8888
EXPOSE 8888

# Update pip
RUN pip install --upgrade pip

# Install jupyterlab
RUN pip install --no-cache-dir jupyterlab && useradd -ms /bin/bash lab

#######################################################
# Install further python packages here
#######################################################
RUN pip install {{ python_modules }}

#######################################################
#######################################################

# Set the USER
USER lab

# Set the WORKDIR
WORKDIR /home/lab

# Define the default entry command
CMD jupyter lab --ip=0.0.0.0

"""


def get_template(template_name):
    # Return the string of the template by name
    if template_name=='jupyter':
        return jupyter_template

    raise ValueError(f"There exists no template with the name '{template_name}'")





#+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
#+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
# OLD DOCKERFILES BELOW
#+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
#+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++

# # Use jupyter/minimal-notebook as base image
# FROM jupyter/minimal-notebook

# # Update pip
# RUN pip install --upgrade pip

# #######################################################
# # Install python packages here
# #######################################################
# RUN pip install numpy \
#                 matplotlib \
#                 pandas \
#                 scipy

# #######################################################
# #######################################################

# # Switch back to jovyan (non-root) to avoid accidental
# # container runs as root
# USER $NB_UID

# # Set the 'jovyan's work' directory to the work directory
# # Remark: The user will automatically start in the WORKDIR.
# WORKDIR /home/jovyan/work
