
FROM python:3.9.7

COPY . .
WORKDIR . .
RUN apt-get update
RUN apt-get install ffmpeg libsm6
RUN pip install -r requirements.txt
EXPOSE 8000
ENTRYPOINT ["python"]
CMD ["./app.py"]
