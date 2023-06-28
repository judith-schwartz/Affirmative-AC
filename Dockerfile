FROM python:3.10-alpine

RUN apk add --no-cache --update \
    python3 python3-dev g++ \
    gfortran musl-dev linux-headers \
    postgresql-dev

RUN pip3 install --upgrade pip setuptools

COPY . .
RUN pip3 install --no-cache-dir -r requirements.txt

ENV OTREE_AUTH_LEVEL=STUDY
ENV OTREE_ADMIN_PASSWORD=DiCe-Lab2023!

# Run oTree prodserver command
CMD [ "otree", "prodserver" , "3001"]
