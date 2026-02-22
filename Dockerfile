# Use modern slim image (Debian Bookworm)
FROM python:3.10-slim

ENV PIP_NO_CACHE_DIR=1
ENV PYTHONUNBUFFERED=1

# Install only required system dependencies
RUN apt-get update && \
    apt-get install -y --no-install-recommends \
        git \
        curl \
        ffmpeg \
        libpq-dev \
        gcc \
        build-essential \
        libffi-dev \
        libssl-dev \
        libxml2-dev \
        libxslt1-dev \
        libjpeg-dev \
        zlib1g-dev \
        postgresql-client \
        xvfb \
        libopus0 \
        libopus-dev \
        wget \
        unzip \
    && rm -rf /var/lib/apt/lists/*

# Upgrade pip
RUN pip install --upgrade pip setuptools wheel

# Clone repo
RUN git clone https://github.com/Anonymous-068/DazaiRobot /root/DazaiRobot
WORKDIR /root/DazaiRobot

# Copy config
COPY ./DazaiRobot/config.py ./DazaiRobot/config.py* /root/DazaiRobot/DazaiRobot/

# Install Python requirements
RUN pip install -r requirements.txt

# Start bot
CMD ["python", "-m", "DazaiRobot"]
