# using an existing dockerimage as the base image
FROM python:3.9-slim

# working directory in docker container will be in /app
WORKDIR /app

# Copy the Python requirements file into the container at /app
COPY requirements.txt .

# Install any dependencies specified in requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of the application code into the container at /app
COPY . .

# Expose port 80 for the FastAPI application
EXPOSE 80

# Specify the command to run when the container starts
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "80"]
