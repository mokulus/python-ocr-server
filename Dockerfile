FROM python:3.11-bookworm
WORKDIR /app
COPY ./requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt
RUN apt-get update
RUN apt-get install -y tesseract-ocr-all
ENV GUNICORN_CMD_ARGS="--bind=0.0.0.0 --chdir=./src/"
COPY . .
EXPOSE 8000
CMD [ "gunicorn", "main:app" ]
