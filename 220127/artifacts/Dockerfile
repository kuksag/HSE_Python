FROM ubuntu:20.04

RUN apt-get update && \
    apt-get install -y python3 pip texlive-full

COPY requirements.txt /usr/src/app/
RUN pip3 install --no-cache-dir -r /usr/src/app/requirements.txt

COPY main.py /usr/src/app/

CMD ["python3", "/usr/src/app/main.py"]