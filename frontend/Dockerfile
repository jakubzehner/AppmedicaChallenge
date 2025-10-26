FROM node:lts-alpine As build

WORKDIR /app

COPY package*.json package-lock.json ./
RUN npm ci

COPY ./ ./
RUN npm run build


FROM nginx:stable-alpine as production

COPY --from=build /app/nginx.conf /etc/nginx/conf.d
COPY --from=build /app/dist /usr/share/nginx/html

EXPOSE 80
ENTRYPOINT ["nginx", "-g", "daemon off;"] 