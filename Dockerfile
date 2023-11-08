FROM python:3-slim AS builder
ADD . /app
WORKDIR /app

RUN apt-get update && apt-get install -y git
# We are installing a dependency here directly into our app source dir
#RUN pip install --target=/app requests
RUN pip install --target=/app --requirement /app/requirements.txt

# A distroless container image with Python and some basics like SSL certificates
# https://github.com/GoogleContainerTools/distroless
FROM gcr.io/distroless/python3-debian10
COPY --from=builder /app /app
WORKDIR /app
ENV PYTHONPATH /app
CMD ["/app/main.py"]

#
#
#FROM ghcr.io/cicirello/pyaction:latest AS builder
#
#COPY . /app
#ADD . /app
#WORKDIR /app
#
## A distroless container image with Python and some basics like SSL certificates
## https://github.com/GoogleContainerTools/distroless
##FROM gcr.io/distroless/python3-debian10
##COPY --from=builder /app /app
##WORKDIR /app
#
##RUN apt-get update && apt-get install -y git
#
## We are installing a dependency here directly into our app source dir
#
#
#ENV PYTHONPATH /app
#RUN python --version
#COPY . /app
#CMD ["/app/main.py"]
