FROM python:3.3.6

COPY ./data_generator /src/data_generator
COPY ./setup.cfg /src
COPY ./setup.py /src
COPY ./README.md /src

WORKDIR /src
RUN ["python", "setup.py", "install"]

WORKDIR /src/data_generator

VOLUME /src/data_generator/out
VOLUME /src/data_generator/in

ENTRYPOINT ["python", "generate_data.py"]
CMD ["--help"]