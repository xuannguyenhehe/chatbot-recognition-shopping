FROM node:11.15.0

COPY . ./frontend/

WORKDIR /frontend/
COPY bot.js /frontend/
COPY package.json /frontend/
RUN npm install
RUN npm install --save botkit