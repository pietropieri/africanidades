FROM python:3.9-slim-bullseye

RUN python3 -m venv /opt/venv

# Install dependencies:
COPY requirements.txt .
RUN . /opt/venv/bin/activate && pip install -r requirements.txt

# Run the application:
COPY africanidades_01.py .
COPY credentials.json .
COPY token.json .
CMD . /opt/venv/bin/activate && exec python africanidades_01.py
