FROM python:3.8

RUN \
    wget https://github.com/alecthomas/chroma/releases/download/v2.8.0/chroma-2.8.0-linux-amd64.tar.gz \
    && tar --extract --verbose --file=chroma-2.8.0-linux-amd64.tar.gz chroma \
    && mv chroma /usr/bin/ \
    && rm chroma-2.8.0-linux-amd64.tar.gz 

RUN pip install --no-cache-dir pygments

WORKDIR /shitty-pygments-chrmoa-wrapper

COPY setup.cfg setup.py .
COPY ./shitty_pygments_chroma_wrapper ./shitty_pygments_chroma_wrapper

RUN pip install .
