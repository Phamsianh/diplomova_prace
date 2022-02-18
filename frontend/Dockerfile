FROM node:14-alpine

WORKDIR /usr/src/app

COPY ./package.json .

RUN npm install

# ENV CHOKIDAR_USEPOLLING=true

COPY . .

CMD [ "npm", "start" ]