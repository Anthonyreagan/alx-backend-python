# File: messaging_app/Dockerfile
# Dockerfile for the Django Messaging App

# Use the official Python 3.10 image as the base image
FROM python:3.10

# Set the working directory inside the container
# This is where our application code will live
WORKDIR /app

# Copy the requirements file into the container at /app
# This step is done separately to leverage Docker's build cache.
# If requirements.txt doesn't change, this layer won't be rebuilt.
COPY Requirements.txt /app/

# Install the Python dependencies
# --no-cache-dir: Don't store cache locally in the container, reduces image size
# -r requirements.txt: Install packages listed in requirements.txt
RUN pip install --no-cache-dir -r Requirements.txt

# Copy the entire Django project into the container at /app
# The '.' at the end means "copy everything from the current directory (host)
# to the WORKDIR (/app) in the container."
COPY . /app

# Expose the port that the Django development server runs on
# The default Django runserver port is 8000
EXPOSE 8000

# Define the command to run the Django development server
# 0.0.0.0 allows access from outside the container.
# This ensures that your app is accessible via the exposed port.
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]