FROM python:3.7-slim

WORKDIR /app

ADD . /app

RUN apt-get update \
    && apt-get install -y --no-install-recommends gcc libgmp3-dev python3-dev \
    && rm -rf /var/lib/apt/lists/* \
    && pip install --trusted-host pypi.python.org -r requirements.txt \
    && apt-get purge -y --auto-remove gcc libgmp3-dev python3-dev
    
ENTRYPOINT ["python"]

CMD ["/app/pay_contributor.py"]