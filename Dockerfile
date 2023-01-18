From python:3.9.7
WORKDIR /flask-app
COPY . .

RUN pip install -r requirements.txt

RUN apt-get update
RUN apt-get install ffmpeg libsm6 libxext6  -y

EXPOSE 10000
ENTRYPOINT ["python"]
CMD ["app.py"]
