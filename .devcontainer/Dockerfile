# Use the official Home Assistant dev container base image
FROM ghcr.io/home-assistant/devcontainer:addons

# Update and install additional OS-level dependencies for Home Assistant
RUN apt-get update && apt-get install -y \
    libpcap-dev \
    libjpeg-dev \
    zlib1g-dev \
    libjpeg62-turbo-dev \
    && rm -rf /var/lib/apt/lists/*

# Set environment variables to avoid potential errors with cryptography
ENV CRYPTOGRAPHY_DONT_BUILD_RUST=1

# Ensure pip and Home Assistant dependencies are up-to-date
RUN pip install --upgrade pip wheel setuptools \
    && pip install homeassistant

# Switch to non-root user (vscode) for Codespaces
USER vscode
