# Use an Ubuntu-based image as the base
FROM mcr.microsoft.com/devcontainers/python:3.12

# Install OS-level dependencies for Home Assistant
RUN apt-get update && apt-get install -y \
    libpcap-dev \
    libffi-dev \
    libssl-dev \
    libjpeg-dev \
    zlib1g-dev \
    libturbojpeg \
    build-essential \
    && rm -rf /var/lib/apt/lists/*

# Set environment variables to avoid potential errors
ENV CRYPTOGRAPHY_DONT_BUILD_RUST=1

# Install Home Assistant dependencies
RUN pip install homeassistant

# Default to non-root user (vscode) for Codespaces
USER vscode