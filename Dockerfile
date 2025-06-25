FROM ubuntu:22.04

WORKDIR /app
ENV DEBIAN_FRONTEND=noninteractive
ENV PYTHONUNBUFFERED=1
ENV PYTHONPATH=/app

RUN apt-get update && apt-get install -y \
    make \
    python3 \
    python3-pip \
    && ln -s /usr/bin/python3 /usr/bin/python \
    && apt-get clean

COPY . .

RUN pip3 install --no-cache-dir -r requirements.txt

CMD [ "bash" ]
