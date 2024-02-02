# build step
FROM oven/bun:latest as build-stage

# Create app directory
WORKDIR /app

# args
ARG NODE_ENV='development'
ARG VITE_API_URL='http://localhost:8000/v1'

# Install app dependencies & build
COPY package*.json ./
RUN bun install
COPY . .
RUN NODE_ENV=$NODE_ENV VITE_API_URL=$VITE_API_URL bun run build

# prod step
FROM nginx:stable-alpine as production-stage

# Copy all build
COPY --from=build-stage /app/dist /usr/share/nginx/html

# Expose
EXPOSE 80

# Command to run
CMD ["nginx", "-g", "daemon off;"]
