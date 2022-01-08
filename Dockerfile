FROM python:3

ADD src/ /
ADD py-requirements.txt /

RUN apt-get update
RUN apt-get install ffmpeg libsm6 libxext6  -y

RUN pip3 install --no-cache-dir --default-timeout=1000 --upgrade pip
RUN pip3 install --no-cache-dir --default-timeout=1000 -r py-requirements.txt

EXPOSE 50001
CMD python3 main.py
