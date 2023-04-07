FROM ubuntu:20.04

RUN apt-get -y update
RUN apt-get -y upgrade


RUN apt install -y default-jdk
RUN apt install -y make gcc build-essential libgtk-3-dev
RUN apt-get install -y python3-pip default-libmysqlclient-dev libnotify-dev libsdl2-dev
RUN apt-get install -y \
freeglut3 \
freeglut3-dev \
libgl1-mesa-dev \
libglu1-mesa-dev \
libgstreamer-plugins-base1.0-dev \
libgtk-3-dev \
libjpeg-dev \
libnotify-dev \
libsdl2-dev \
libsm-dev \
libtiff-dev \
libwebkit2gtk-4.0-dev \
libxtst-dev

RUN apt install -y wget
RUN apt install -y zip

RUN apt install -y build-essential
ARG DEBIAN_FRONTEND=noninteractive

RUN mkdir /build/
RUN mkdir -p /root/

WORKDIR /build/

RUN wget -nv \
	https://repo.anaconda.com/miniconda/Miniconda3-py37_4.10.3-Linux-x86_64.sh\
	&& mkdir /root/.conda \
	&& bash Miniconda3-py37_4.10.3-Linux-x86_64.sh -b -p /root/miniconda3 \
	&& rm -f Miniconda3-py37_4.10.3-Linux-x86_64.sh

RUN wget --no-check-certificate https://github.com/samuelbunga/cxp-lite/archive/refs/heads/master.zip
RUN unzip master.zip

RUN wget --no-check-certificate https://github.com/CellProfiler/CellProfiler/archive/refs/tags/v4.2.5.zip

RUN unzip v4.2.5.zip

RUN wget -nv --no-check-certificate https://wsr.imagej.net/distros/linux/ij153-linux64-java8.zip
RUN unzip ij153-linux64-java8.zip

ENV PATH="/root/miniconda3/bin:${PATH}"
ARG PATH="/root/miniconda3/bin:${PATH}"


RUN conda create --name cxplite python=3.8
RUN conda install -y -n cxplite pandas imageio pandas tifffile openpyxl


RUN cd CellProfiler-4.2.5 && conda run -n cxplite pip3 install .

RUN mkdir /user_home
WORKDIR /user_home

CMD ["conda run -n cxplite python /build/cxp-lite-master/cxp.py"]

# brew install xquartz
# open -a xquartz
# IP=$(ifconfig en0 | grep inet | awk '$1=="inet" {print $2}')
# export DISPLAY=$IP:0

# docker run --rm -it -e DISPLAY=$IP:0 -v /tmp/.X11-unix:/tmp/.X11-unix --mount type=bind,source="$HOME",target=/user_home cxp




