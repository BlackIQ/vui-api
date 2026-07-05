# Use the Python base image
FROM python:alpine

# Set the working directory in the container
WORKDIR /app

# Install some stuff
RUN apk add --no-cache bash shadow util-linux

# Copy the Pipfile and Pipfile.lock to the container
COPY Pipfile Pipfile.lock ./

# Install Pipenv and project dependencies
RUN pip install pipenv && \
    pipenv install --system --deploy

# Copy the application code to the container
COPY . .

# Create some stuff
RUN python3 api/database/create.py

# Set the environment variables
ENV APP_PORT=8000
ENV DB_NAME=vui.db
ENV API_KEY=hello-amir-hi-hossein

# Expose the container port
EXPOSE 8000

# Start the Flask application
CMD ["python3", "wsgi.py"]
