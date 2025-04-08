FROM python:3.11-slim

# Install ffmpeg
RUN apt update && apt install -y ffmpeg

# Set working directory
WORKDIR /app

# Copy everything
COPY . .

# Install Python deps
RUN pip install -r requirements.txt

# Expose the FastAPI port
EXPOSE 8000

# Run your app
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
