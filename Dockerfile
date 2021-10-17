FROM python:3.8-buster

WORKDIR /pyrate-stocks

# Copy file and install dependencies
COPY requirements.txt .
RUN pip install -r requirements.txt 

# Copy required files
COPY . .

EXPOSE 5000
ENV PORT 5000

# Use gunicorn as the entrypoint
# Timeout is set to 0 to disable the timeouts of the workers to allow Cloud Run to handle instance scaling.
CMD exec gunicorn --bind :$PORT fin_app:app --workers 1 --threads 8 --timeout 0