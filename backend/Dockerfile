# Use the official Python image as the base
FROM python:3.9-slim

# Set the working directory inside the container
WORKDIR /app

# Install the dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Install watchdog for file change detection (optional if not using Uvicorn's reload)
RUN pip install watchdog

# Copy the entire application into the container
COPY . .

# Expose the port the app runs on
EXPOSE 8000

# Run the application with automatic reload
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000", "--reload"]
