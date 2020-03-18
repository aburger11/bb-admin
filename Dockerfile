FROM python:3.7.4
RUN mkdir /bb-admin
COPY . /bb-admin

RUN pip install --editable /bb-admin
WORKDIR /bb-admin
VOLUME /bb-admin

ENTRYPOINT [ "bb-admin" ]
