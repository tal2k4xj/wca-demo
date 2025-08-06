FROM registry.access.redhat.com/ubi8/python-39
COPY requirements.txt /app/requirements.txt
RUN python -m pip install -r /app/requirements.txt
COPY ../.. /app
ENTRYPOINT ["python", "/app/app.py"]
EXPOSE 4321
