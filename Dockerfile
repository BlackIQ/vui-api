# Use the Python base image
FROM python:3.9

# Set the working directory in the container
WORKDIR /app

# Copy the Pipfile and Pipfile.lock to the container
COPY Pipfile Pipfile.lock ./

# Install Pipenv and project dependencies
RUN pip install pipenv && \
    pipenv install --system --deploy

# Copy the application code to the container
COPY api ./api
COPY wsgi.py ./

# Set the environment variables
ENV FLASK_APP=api.main
ENV FLASK_RUN_HOST=0.0.0.0
ENV FLASK_RUN_PORT=5000

# Expose the container port
EXPOSE 5000

# Start the Flask application
CMD ["pipenv", "run", "flask", "run"]
