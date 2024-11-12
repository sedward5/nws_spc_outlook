# Start from a Python 3.12 dev container base
FROM mcr.microsoft.com/devcontainers/python:3.12

# Set environment variables for non-interactive installation
ENV DEBIAN_FRONTEND=noninteractive \
    DEVCONTAINER=1

#  Install Home Assistant-specific dependencies
RUN apt-get update && apt-get install -y \
    libpcap-dev \
    libffi-dev \
    libssl-dev \
    libjpeg-dev \
    zlib1g-dev \
    build-essential \
    && rm -rf /var/lib/apt/lists/*

# Create and activate a Python virtual environment
ENV VIRTUAL_ENV=/opt/venv
RUN python3 -m venv $VIRTUAL_ENV
ENV PATH="$VIRTUAL_ENV/bin:$PATH"

# Upgrade pip and install Home Assistant in the virtual environment
RUN pip install --upgrade pip wheel setuptools \
    && pip install homeassistant

# Switch to non-root user (vscode) for Codespaces
USER vscode