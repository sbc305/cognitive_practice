ARG NODE_IMG=node:lts-alpine
FROM $NODE_IMG

WORKDIR /app
RUN npm install -g http-server

COPY package*.json ./
RUN npm install
COPY . .

RUN npm run build

EXPOSE 8080
CMD [ "http-server", "dist", "--cors" ]
