FROM node:20-alpine

WORKDIR /app

COPY package*.json ./

RUN npm install --legacy-peer-deps
RUN npm install -g npm@latest

COPY . .

EXPOSE 5173

CMD ["npm", "run", "dev", "--", "--host"]