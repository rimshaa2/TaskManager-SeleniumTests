FROM python:3.9-slim

# Install required dependencies
RUN apt-get update && apt-get install -y \
    wget gnupg unzip curl chromium chromium-driver \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

# Set path for Chrome and Chromedriver
ENV CHROME_BIN=/usr/bin/chromium
ENV CHROMEDRIVER_PATH=/usr/bin/chromedriver

# Install Python dependencies
COPY requirements.txt .
RUN pip install --upgrade pip && pip install -r requirements.txt

# Copy test code
COPY . /app
WORKDIR /app

# Default command
CMD ["pytest", "-v", "test_task_manager.py"]


