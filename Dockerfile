FROM python:3.9

WORKDIR /pyrate-stocks
COPY . . 

# Install dependencies
COPY requirements.txt .
RUN pip3 install -r requirements.txt 

# Set Flask File and Run App
COPY fin_app.py .
ENTRYPOINT FLASK_APP=fin_app.py flask run --host=0.0.0.0