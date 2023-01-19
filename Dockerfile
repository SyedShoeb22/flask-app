
FROM python:3.9.7

COPY . .
WORKDIR . .
RUN pip install -r requirements.txt
EXPOSE 8000
ENTRYPOINT ["python"]
CMD ["./app.py"]
