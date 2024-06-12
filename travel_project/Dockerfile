# Use the official Python image from the Docker Hub
FROM python:3.11-slim

# Install netcat for wait-for-it script
RUN apt-get update && apt-get install -y netcat-openbsd

# Set the working directory
WORKDIR /usr/src/app

# Copy the requirements.txt file
COPY requirements.txt ./

# Install the required packages
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of the application code
COPY . .

# Copy the custom entrypoint script
# COPY entrypoint.sh /entrypoint.sh
# RUN chmod +x /entrypoint.sh

# Expose the port the app runs on
EXPOSE 8000

# Run the custom entrypoint script
# ENTRYPOINT ["/entrypoint.sh"]
