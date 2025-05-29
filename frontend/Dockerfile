# frontend/Dockerfile
FROM node:slim

WORKDIR /app                

ENV NODE_ENV=development    
COPY package*.json ./
RUN npm install --include=dev

COPY . .

CMD ["npm", "run", "start"]
