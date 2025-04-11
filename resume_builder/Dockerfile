FROM python:3.10-slim

WORKDIR /app

COPY clean_requirements.txt .

# Install system-level dependencies including WeasyPrint requirements
RUN apt-get update && apt-get install -y \
    build-essential \
    libffi-dev \
    libssl-dev \
    libxml2-dev \
    libxslt1-dev \
    zlib1g-dev \
    libjpeg-dev \
    libmariadb-dev \
    libcairo2 \
    pango1.0-tools \
    libpangocairo-1.0-0 \
    libgdk-pixbuf2.0-0 \
    libpango1.0-0 \
    libglib2.0-0 \
    shared-mime-info \
    fonts-liberation \
    fonts-dejavu \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

# Install Python dependencies
RUN pip install --upgrade pip && pip install -r clean_requirements.txt

COPY . .

EXPOSE 8000

CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]

