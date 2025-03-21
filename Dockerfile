FROM python:3.10-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install -r requirements.txt

COPY . .

EXPOSE 5000

# Setting the default command when the containter starts:
#CMD ['python', 'Code/API ML Solution/api.py']

