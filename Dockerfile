FROM python:3.9

RUN mkdir /app

# Set the working directory in the container
WORKDIR /app

# Copy the current directory contents into the container at /app
COPY . /app

RUN pip install poetry
RUN poetry install
# Make port 7860 available to the world outside this container
EXPOSE 7860

# Run app.py when the container launches
CMD ["poetry","run","python", "app.py"]