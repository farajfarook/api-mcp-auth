# Use an official Node.js runtime as a parent image
FROM node:20-alpine AS build

# Set the working directory
WORKDIR /app

# Copy package.json and package-lock.json (or yarn.lock)
COPY Spa/package*.json ./

# Install dependencies
RUN npm install

# Copy the rest of the application code
COPY Spa/. .

# Build the React app
RUN npm run build

# Use a lightweight web server to serve the static files
FROM nginx:alpine

# Copy the build output from the previous stage
COPY --from=build /app/dist /usr/share/nginx/html

# Expose port 80
EXPOSE 80

# Start Nginx when the container launches
CMD ["nginx", "-g", "daemon off;"]
