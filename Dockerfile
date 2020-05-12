FROM python:3.6
#FROM python:2.7.10
RUN apt-get update
# copy file
WORKDIR /app
COPY ./ /app
ENV GOOGLE_APPLICATION_CREDENTIALS="/app/gcp_credentials.json"

