FROM python:3.11-slim

WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    build-essential \
    tesseract-ocr \
    libmagic1 \
    poppler-utils \
    libreoffice \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements first to leverage Docker cache
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of the application
COPY . .

# Create necessary directories
RUN mkdir -p data chroma

# Expose the port the app runs on
EXPOSE 3038

# Command to run the application
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "3038"] 