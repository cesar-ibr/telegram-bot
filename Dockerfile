# Use Python 3.11.7 slim image as base
FROM python:3.11.7-slim

# Set working directory in container
WORKDIR /app

# Install poetry
RUN pip install poetry==1.7.1

# Copy poetry configuration files
COPY pyproject.toml poetry.lock* ./

# Configure poetry to not create virtual environment inside container
RUN poetry config virtualenvs.create false

# Copy project files
COPY . .

# Install dependencies
RUN poetry install --no-interaction --no-ansi

# Set the default command to run your application
CMD ["python", "ai_engineer/main.py"]
