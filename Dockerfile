FROM python:3.10-slim

WORKDIR /app

RUN pip install huggingface-hub

RUN huggingface-hub download \
    apple/MobileCLIP2-S0 \
    --local-dir /app/model \
    --local-dir-use-symlinks False \
    --include "*.pt"

COPY requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

COPY ./app /app/app

EXPOSE 8000


CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]