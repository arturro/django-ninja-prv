# Use a slim Python image for a smaller footprint
FROM python:3.13-slim

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

RUN pip install --upgrade pip \
    && pip install uv

# Set the working directory in the container
WORKDIR /app

# Copy only the dependency files to leverage Docker cache
COPY uv.lock .

# Use uv to install dependencies from the locked file
# The --no-deps flag is used because the lock file already contains all dependencies
RUN uv pip install --no-deps -r uv.lock

# Copy the rest of the application code
COPY . .

# Expose the port the app will run on
EXPOSE 8000

CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]

# Run the Django application with Gunicorn
# Using 0.0.0.0 is important for Docker to expose the port correctly
#CMD ["gunicorn", "--bind", "0.0.0.0:8000", "your_project_name.wsgi:application"]
# Note: Replace 'your_project_name' with your actual Django project name.