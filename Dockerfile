FROM python:3.11.3

EXPOSE 3000

COPY requirements_docker.txt ./
RUN pip install --no-cache-dir -r requirements_docker.txt

COPY src/ src
COPY main.py main.py
COPY not-config.json not-config.json

CMD [ "python", "main.py" ]
