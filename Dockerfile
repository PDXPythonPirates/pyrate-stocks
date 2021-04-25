FROM python:3.9

WORKDIR /pyrate-stocks
COPY . . 

# Install dependencies
COPY requirements.txt .
RUN pip3 install -r requirements.txt 

# Run application
CMD [ "python", "fin_app.py" ]