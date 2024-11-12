# Use the official Home Assistant dev container base image
FROM ghcr.io/home-assistant/devcontainer:addons

# Update and install OS-level dependencies, including python3-venv
RUN apt-get update && apt-get install -y \
    python3-venv \
    libpcap-dev \
    libjpeg-dev \
    zlib1g-dev \
    libjpeg62-turbo-dev \
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