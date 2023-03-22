FROM ubuntu:20.04

# Update the package lists
RUN apt-get update && \
    apt-get install -y ffmpeg \
    && apt-get install -y python3-pip

RUN pip install --upgrade pip
RUN apt-get install -y wget
# RUN INSTALL_PATH=~/anaconda \
#     && wget http://repo.continuum.io/miniconda/Miniconda2-latest-Linux-x86_64.sh \
#     && bash Miniconda2-latest* -fbp $INSTALL_PATH \
#     ENV PATH=/root/anaconda/bin:$PATH

ADD ./requirements.txt /tmp/requirements.txt
RUN pip install --no-cache-dir -q -r /tmp/requirements.txt
# RUN conda install pytorch torchvision torchaudio cpuonly -c pytorch

ADD ./app.py /opt/app.py
ADD ./templates /opt/templates
ADD ./audio /opt/audio

WORKDIR /opt

CMD gunicorn --timeout 360 --bind 0.0.0.0:$PORT -k gevent --worker-connections 32 app:app 