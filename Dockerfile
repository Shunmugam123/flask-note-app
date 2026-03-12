# Use an official Python runtime as a parent image
FROM python:3.9-slim-buster

# Set the working directory in the container
WORKDIR /app

# Install any needed packages specified in requirements.txt
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy the current directory contents into the container at /app
COPY . .

# Expose the port that Gunicorn will listen on
EXPOSE 8080

# Run gunicorn to serve the Flask application
# Gunicorn will listen on all interfaces (0.0.0.0) and on port 8080
# The 'app:app' refers to the 'app' variable within the 'app.py' file
CMD ["gunicorn", "--bind", "0.0.0.0:8080", "app:app"]