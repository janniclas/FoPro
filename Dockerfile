FROM node


WORKDIR /usr/app

COPY package*.json /usr/app/
COPY tsconfig.json /usr/app/
COPY src /usr/app/src/
RUN npm install

COPY .env /usr/app/

RUN npm run compile 

CMD [ "node", "/usr/app/build/src/main.js" ]