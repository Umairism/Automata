FROM python:3.9-slim

# Install system dependencies including Graphviz
RUN apt-get update && apt-get install -y \
    graphviz \
    && rm -rf /var/lib/apt/lists/*

# Set working directory
WORKDIR /app

# Copy requirements first for better caching
COPY requirements.txt .

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy application code
COPY . .

# Create static directory for generated diagrams
RUN mkdir -p static

# Expose the port dynamically (Railway will set it)
EXPOSE $PORT

# Run the application using Railway's assigned port
CMD ["sh", "-c", "gunicorn app:app -w 4 -b 0.0.0.0:${PORT}"]
