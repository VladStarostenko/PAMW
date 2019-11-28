FROM node:11.7.0

WORKDIR /app

COPY package*.json ./

RUN npm install

COPY . .

EXPOSE 8888

CMD ["npm", "start"]
