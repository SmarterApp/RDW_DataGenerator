# This Dockerfile builds a runtime image for the data generator
# It uses a multi-stage build to minimize duplicate build work (faster!) and reduce footprint (smaller!)

FROM python:3.7.2-alpine as base

FROM base as builder
RUN mkdir /install
WORKDIR /install
COPY ./requirements.txt /requirements.txt
RUN pip install --prefix=/install -r /requirements.txt

FROM base
COPY --from=builder /install /usr/local
COPY ./datagen /datagen
COPY ./README.md /datagen
VOLUME /out
VOLUME /in

ENTRYPOINT ["python", "-m", "datagen.generate_data"]
CMD ["--help"]
