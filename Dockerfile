
FROM python:3.9.7

COPY . .
WORKDIR . .
RUN apt-get update && apt-get install -y python3-opencv
RUN pip install opencv-python
RUN pip install -r requirements.txt
EXPOSE 8000
ENTRYPOINT ["python"]
CMD ["./app.py"]
