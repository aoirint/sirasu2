FROM python:3.9

ENV PATH=/home/user/.local/bin:$PATH
ENV UPLOAD_ROOT=/uploads

RUN apt-get update && \
    apt-get install -y \
        gosu && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

RUN useradd -m --uid=1000 -o user

ADD ./requirements.txt /requirements.txt
RUN gosu user pip3 install -r /requirements.txt

ADD ./sirasu2 /code/sirasu2

WORKDIR /code/sirasu2
CMD [ "gosu", "user", "uvicorn", "run:app", "--host", "0.0.0.0", "--port", "8000" ]
