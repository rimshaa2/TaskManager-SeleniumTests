FROM python:3.10-slim

# Install Chrome (v137)
RUN apt-get update && apt-get install -y wget gnupg unzip curl \
    && wget https://dl.google.com/linux/direct/google-chrome-stable_current_amd64.deb \
    && apt install -y ./google-chrome-stable_current_amd64.deb

# Install ChromeDriver (v137)
RUN CHROME_VERSION=$(google-chrome --version | awk '{print $3}') && \
    CHROMEDRIVER_VERSION=$(echo $CHROME_VERSION | cut -d '.' -f 1-3) && \
    wget https://storage.googleapis.com/chrome-for-testing-public/${CHROMEDRIVER_VERSION}/linux64/chromedriver-linux64.zip && \
    unzip chromedriver-linux64.zip && \
    mv chromedriver-linux64/chromedriver /usr/bin/chromedriver && \
    chmod +x /usr/bin/chromedriver

# Install Python dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Add test files
COPY . /tests
WORKDIR /tests

# Run tests by default
CMD ["pytest"]
