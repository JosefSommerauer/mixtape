FROM debian:bullseye-20200514-slim as base

# https://bugs.debian.org/cgi-bin/bugreport.cgi?bug=863199
RUN mkdir -p /usr/share/man/man1

RUN set -ex \
    && apt-get -yq update \
    && apt-get install -yq --no-install-recommends --no-upgrade \
        python3-minimal \
        python3-pip \ 
        python3-gst-1.0 \
        gstreamer1.0-plugins-base \
        gstreamer1.0-tools \
        gstreamer1.0-pulseaudio \
        gstreamer1.0-python3-plugin-loader 

RUN update-alternatives --install /usr/bin/pip pip /usr/bin/pip3 10
RUN update-alternatives --install /usr/bin/python python /usr/bin/python3 10


# req test changes less often than req install
WORKDIR /src
COPY *.txt /src/
RUN pip install -r /src/req-test.txt && pip install -r /src/req-install.txt 

# Copy everything now
COPY . /src
RUN pip3 install -e /src[test]
WORKDIR /src

# RUN groupadd -g 999 mixtape && \
#     useradd -r -u 999 -g mixtape mixtape
# USER mixtape