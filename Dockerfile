FROM ubuntu:16.04

ADD ./requirements.txt /tmp/requirements.txt
RUN pip install --no-cache-dir -q -r /tmp/requirements.txt
RUN conda install pytorch torchvision torchaudio cpuonly -c pytorch

ADD ./app.py /opt/app.py
ADD ./templates /opt/templates

WORKDIR /opt

CMD 
