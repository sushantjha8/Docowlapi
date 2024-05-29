# FROM python:3.9

# RUN mkdir /app

# # Set the working directory in the container
# WORKDIR /app
# RUN pip install poetry timm==0.6.13
# # Copy the current directory contents into the container at /app
# COPY . /app
# RUN poetry install
# # Make port 7860 available to the world outside this container
# EXPOSE 7860

# # Run app.py when the container launches
# CMD ["poetry","run","python", "app.py"]

# Use the NVIDIA CUDA base image
FROM nvidia/cuda:12.1.1-cudnn8-devel-ubuntu20.04

# Create a directory for the app
RUN mkdir /app

# Install Python and pip
RUN apt-get update && \
    apt-get install -y python3 python3-pip && \
    ln -s /usr/bin/python3 /usr/bin/python && \
    ln -s /usr/bin/pip3 /usr/bi


# Install Poetry and timm
RUN pip install poetry

# Set environment variables for CUDA
ENV LD_LIBRARY_PATH=/usr/local/cuda/lib64:/usr/local/cuda/extras/CUPTI/lib64:$CUDA_PATH 
ENV PATH=/usr/local/cuda-12.1/bin:$PATH

RUN apt-get update && apt-get install -y coreutils

# Install Poetry
RUN curl -sSL https://install.python-poetry.org | python3 -

# Ensure Poetry is in the PATH
ENV PATH="/root/.local/bin:$PATH"

# Set the working directory in the container
WORKDIR /app

COPY ./pyproject.toml /app
# Install project dependencies using Poetry
RUN poetry install 

# Copy the current directory contents into the container at /app
COPY . /app

EXPOSE 7860

# Command to run the application
CMD ["poetry", "run", "python", "app.py"]
