FROM node:latest

WORKDIR /web

COPY web/package.json package.json
RUN npm install

COPY web/src src/
COPY web/public public/
RUN npm build

ADD /web .

EXPOSE 3000

CMD ["npm", "start"]