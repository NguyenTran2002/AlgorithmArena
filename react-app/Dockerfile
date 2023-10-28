# Use the official Node.js image as the base image
FROM node:16-alpine3.14

# Set the working directory inside the container
WORKDIR /app

# Install curl
RUN apk --no-cache add curl

# Copy package.json and package-lock.json (if available) to the container
COPY package.json ./

# Install project dependencies
RUN yarn install

# Copy the entire project to the container
COPY . .

# Build the React app for production
# RUN npm run build

# Expose the port that your app will run on (adjust as needed)
EXPOSE 8080

# Define the command to start your app
# CMD ["yarn", "run", "vite", "--host", "0.0.0.0"]
CMD ["yarn", "run", "dev"]

