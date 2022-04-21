FROM dockershelf/python:3.10
LABEL maintainer "Luis Alejandro Martínez Faneyth <luis@collagelabs.org>"

RUN apt-get update && \
    apt-get install sudo python3.10-venv

RUN useradd -ms /bin/bash luisalejandro
RUN echo "luisalejandro ALL=(ALL) NOPASSWD: ALL" > /etc/sudoers.d/luisalejandro

ADD requirements.txt /root/
RUN pip install -r /root/requirements.txt
RUN rm /root/requirements.txt

COPY entrypoint.sh /entrypoint.sh
COPY entrypoint.py /entrypoint.py

ENTRYPOINT ["/entrypoint.sh"]

CMD ["tail", "-f", "/dev/null"]