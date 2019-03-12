FROM node:8.15

RUN yarn global add bs-platform

RUN mkdir -p /src
WORKDIR /src
