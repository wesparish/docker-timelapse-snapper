FROM ubuntu:20.04

RUN apt-get update && \
    apt-get install python3-pip git python3 vim-tiny curl -y && \
    apt-get autoremove -y && \
    apt-get clean

# Add Tini
ENV TINI_VERSION v0.19.0
ADD https://github.com/krallin/tini/releases/download/${TINI_VERSION}/tini /tini
RUN chmod +x /tini

ADD timelapse-snapper/requirements.txt /
RUN pip3 install -r requirements.txt

ENV LOG_LEVEL="INFO" LC_ALL=C.UTF-8 LANG=C.UTF-8

ADD timelapse-snapper/lib /lib
COPY timelapse-snapper/timelapse-snapper.py /timelapse-snapper.py
RUN chown root:root timelapse-snapper.py

EXPOSE 9000

ENTRYPOINT ["/tini", "--", "/timelapse-snapper.py"]
