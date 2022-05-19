FROM python:3.10
RUN apt-get update && apt-get install -y g++

ENV wd /workdir
WORKDIR ${wd}       


# adds files from your Docker client’s current directory
COPY src /workdir/src
COPY script /workdir/script
COPY result/ /workdir/result
COPY requirements.txt /workdir/

RUN pip install -r /workdir/requirements.txt     
RUN pip install --upgrade protobuf

ENTRYPOINT [ "/bin/bash", "/workdir/script/start.sh" ]