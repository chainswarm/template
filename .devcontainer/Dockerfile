FROM python:3.13-slim

# Set environment variables
ENV PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1 \
    PIP_NO_CACHE_DIR=1 \
    PIP_DISABLE_PIP_VERSION_CHECK=1 \
    DEBIAN_FRONTEND=noninteractive

# Install system dependencies
RUN apt-get update && apt-get install -y \
    # Build essentials
    build-essential \
    gcc \
    g++ \
    make \
    # Version control
    git \
    # Utilities
    curl \
    wget \
    vim \
    nano \
    less \
    jq \
    # Database clients
    postgresql-client \
    # Network tools
    netcat-openbsd \
    iputils-ping \
    # Other
    sudo \
    && rm -rf /var/lib/apt/lists/*

# Create non-root user
ARG USERNAME=vscode
ARG USER_UID=1000
ARG USER_GID=$USER_UID

RUN groupadd --gid $USER_GID $USERNAME \
    && useradd --uid $USER_UID --gid $USER_GID -m $USERNAME \
    && echo $USERNAME ALL=\(root\) NOPASSWD:ALL > /etc/sudoers.d/$USERNAME \
    && chmod 0440 /etc/sudoers.d/$USERNAME

# Create workspace directory
WORKDIR /workspace

# Install Python development tools
RUN pip install --no-cache-dir \
    # Testing
    pytest \
    pytest-cov \
    pytest-asyncio \
    pytest-mock \
    # Linting and formatting
    black \
    ruff \
    mypy \
    # Development
    ipython \
    ipdb \
    # Common libraries
    python-dotenv \
    loguru \
    # Database drivers
    psycopg2-binary \
    redis \
    clickhouse-driver

# Switch to non-root user
USER $USERNAME

# Set PYTHONPATH
ENV PYTHONPATH=/workspace

CMD ["/bin/bash"]
