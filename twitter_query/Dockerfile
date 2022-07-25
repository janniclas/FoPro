FROM node


WORKDIR /usr/app

COPY package*.json /usr/app/
COPY tsconfig.json /usr/app/
COPY src /usr/app/src/
RUN npm install
COPY start.sh /usr/app/
COPY .env /usr/app/

RUN npm run compile 

ENTRYPOINT ["/usr/app/start.sh"]
