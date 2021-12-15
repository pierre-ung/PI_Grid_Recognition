FROM python:3

ADD src/ /
ADD py-requirements.txt /

RUN apt-get update
RUN apt-get install ffmpeg libsm6 libxext6  -y

RUN pip install --no-cache-dir --upgrade pip && \
    pip install --no-cache-dir -r py-requirements.txt

CMD python main.py
