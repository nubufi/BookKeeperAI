FROM python:3.12-slim

RUN apt-get update && apt-get install -y --no-install-recommends \
    curl \
    && pip install --no-cache-dir pipenv \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app

COPY /src Pipfile Pipfile.lock .env /app

RUN pipenv install --system --deploy --ignore-pipfile

EXPOSE 9000
ENV GRADIO_SERVER_NAME="0.0.0.0"

CMD ["python", "app.py"]



