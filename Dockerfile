FROM python:3.9-slim

# Install gcc and build dependencies for tgcrypto
RUN apt-get update && apt-get install -y --no-install-recommends \
    gcc \
    build-essential \
    libffi-dev \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app
COPY repo /app

# Install Python dependencies
RUN if [ -f "requirements.txt" ]; then pip install --no-cache-dir -r requirements.txt; fi

# Start your bot
CMD ["python", "bot.py"]
