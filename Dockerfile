# FROM python:3.13.7

# WORKDIR /usr/src/app

# RUN apt-get update && apt-get install -y \
#     gcc \
#     libpq-dev \
#     && rm -rf /var/lib/apt/lists/*

# COPY requirements.txt ./

# RUN pip install --no-cache-dir -r requirements.txt

# COPY . .

# EXPOSE 8000
# CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000", "--reload"]

# Use official lightweight Python image
FROM python:3.11-slim

# Set working directory
WORKDIR /usr/src/app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    build-essential \
    libpq-dev \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements first for caching
COPY requirements.txt .

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy app source
COPY . .

# Run FastAPI with uvicorn
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]

# Use the following command to build the Docker image:
# docker build -t fastapi_crud .

# Use the following command to run the Docker container:
# docker run -d -p 8000:8000 fastapi_crud

# Access the application at http://localhost:8000

# To stop the container, use:
# docker stop <container_id>

# To remove the container, use:
# docker rm <container_id>

# To remove the image, use:
# docker rmi fastapi_crud

# To view logs, use:
# docker logs <container_id>

# To run the container in detached mode, use:
# docker run -d -p 8000:8000 --name fastapi_crud

# To run the container with a specific name, use:
# docker run -d -p 8000:8000 --name my_fastapi_app

# To run the container with an interactive terminal, use:
# docker run -it -p 8000:8000 fastapi_crud /bin
