# Этап сборки
FROM node:alpine as build
# Установите рабочую директорию для надежности
WORKDIR /app
COPY package*.json ./
RUN npm install
COPY . .
RUN npm run build
# Этап запуска (production)
FROM nginx:stable-alpine
# Копируем статику из этапа сборки (обратите внимание на путь '/app/dist')
COPY --from=build /app/dist /usr/share/nginx/html
# Копируем конфигурационный файл Nginx для SPA (создайте его ниже)
COPY nginx.conf /etc/nginx/conf.d/default.conf