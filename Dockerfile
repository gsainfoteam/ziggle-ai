FROM python:3.12

WORKDIR /app

COPY . .

RUN pip install poetry && poetry install --no-root

ENV PYTHONPATH=/app/src

EXPOSE 8000

CMD ["poetry" ,"run", "uvicorn", "src.main:app", "--host", "0.0.0.0", "--port", "8000"]
