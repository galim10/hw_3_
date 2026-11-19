FROM python:3.13-slim
RUN apt-get update && \
    apt-get install -y --no-install-recommends curl && \
    rm -rf /var/lib/apt/lists/*
WORKDIR /src
COPY ../app/requirements.txt .
RUN python -m pip install --no-cache-dir -r requirements.txt
COPY .. .

RUN useradd --create-home --uid 1000 appuser
COPY --chown=appuser:appuser .. .
USER appuser
CMD ["python", "app/app.py"]
