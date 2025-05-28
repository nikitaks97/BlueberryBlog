# Use a smaller base image for better performance and security
FROM python:3.9-slim-buster

# Set environment variable for the application (best practice)
ENV FLASK_APP=app

# Set the working directory
WORKDIR /app

# Install system dependencies (if any are needed)
RUN apt-get update && apt-get install -y --no-install-recommends libpq-dev && rm -rf /var/lib/apt/lists/*

# Create a virtual environment
RUN python3 -m venv /opt/venv

# Activate the virtual environment
ENV PATH="/opt/venv/bin:$PATH"

# Install application dependencies from requirements.txt
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy the application code into the container
COPY . .

# Expose the port used by the application
EXPOSE 5000

# Run the application using Gunicorn (recommended for production)
CMD ["gunicorn", "-w", "4", "-b", "0.0.0.0:5000", "app:create_app()", "--worker-class", "gunicorn.workers.ggevent.GeventWorker"]
