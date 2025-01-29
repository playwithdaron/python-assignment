# Use official Python image as base
FROM python:3.9-slim

# Set working directory
WORKDIR /app

# Copy requirements first to leverage Docker cache
COPY requirements.txt .

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt \
    && pip install gunicorn  # Explicitly install gunicorn if not in requirements.txt

# Copy the rest of the application
COPY . .

# Expose port
EXPOSE 5000

# Set Flask environment variables
ENV FLASK_APP=app.py
ENV FLASK_ENV=production

# Run gunicorn
CMD ["gunicorn", "--bind", "0.0.0.0:5000", "app:app"]