FROM python:3.12-slim

WORKDIR /app/Discord-ChatBot

COPY requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

COPY . .

CMD ["python", "run.py"]