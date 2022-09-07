FROM python:3.10

COPY ./requirements.txt /tmp/requirements.txt
RUN pip install -r /tmp/requirements.txt
RUN rm /tmp/requirements.txt

COPY ./src/ /usr/local/share/drone-global-env/
WORKDIR /usr/local/share/drone-global-env/
ENTRYPOINT ["python", "-um", "hypercorn", "main:app", "--bind", "0.0.0.0:8080"]
