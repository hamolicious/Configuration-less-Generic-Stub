FROM python:3.7.4

EXPOSE 3000

COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

COPY src/ src
COPY main.py main.py
COPY not-config.json not-config.json

CMD [ "python", "main.py" ]
