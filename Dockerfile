FROM docker.io/library/python:3.11-alpine
COPY requirements.txt app.py /
RUN pip install -r /requirements.txt
CMD ["python", "/app.py"]
