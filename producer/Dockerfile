FROM fedora:43

RUN dnf install -y python3 python3-qpid-proton cyrus-sasl-plain \
    && dnf clean all

WORKDIR /app

COPY producer.py /app/producer.py

CMD ["python3", "producer.py"]