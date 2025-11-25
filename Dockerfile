FROM python:3.10-slim

RUN useradd -m appuser

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

RUN chown -R appuser:appuser /app
USER appuser

CMD ["uvicorn", "Back.app:app", "--host", "0.0.0.0", "--port", "8000"]
