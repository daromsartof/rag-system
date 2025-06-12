FROM python:3.10.8-slim

WORKDIR /app

# Install system dependencies and newer SQLite
RUN apt-get update && apt-get install -y \
    build-essential \
    tesseract-ocr \
    libmagic1 \
    poppler-utils \
    libreoffice \
    wget \
    && rm -rf /var/lib/apt/lists/*

# Install newer SQLite
RUN wget https://www.sqlite.org/2025/sqlite-autoconf-3500100.tar.gz \
    && tar xvfz sqlite-autoconf-3500100.tar.gz \
    && cd sqlite-autoconf-3500100 \
    && ./configure \
    && make \
    && make install \
    && cd .. \
    && rm -rf sqlite-autoconf-3500100*
    
ENV LD_LIBRARY_PATH="/usr/local/lib"
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
CMD ["python", "main.py"] 