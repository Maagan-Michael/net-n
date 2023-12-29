# Stage 1: Build the React app
FROM node:lts-slim as builder
WORKDIR /app
COPY switch-manager-react/package*.json ./
RUN npm install --legacy-peer-deps
COPY . .
WORKDIR /app/switch-manager-react
RUN npm run build 
# Stage 2: Create the production image
FROM nginx:mainline-alpine-slim
COPY --from=builder /app/switch-manager-react/dist /usr/share/nginx/html
EXPOSE 80
CMD ["nginx", "-g", "daemon off;"]
