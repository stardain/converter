# Use the official Python 3.13 image from the Docker Hub
FROM python:3.13-slim

# Set the working directory in the container
WORKDIR /app

# Copy the requirements.txt file to the working directory
COPY requirements.txt .

# Install the required packages
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of your application code to the working directory
COPY . .

# Expose the port that Uvicorn will run on (default is 8000)
EXPOSE 8000

# Command to run the Uvicorn server
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]

# docker build --progress=plain -t imaaage .
# Get-NetTCPConnection

# docker tag fixed_image stardain/converter-app:latest
# docker push stardain/converter-app:latest