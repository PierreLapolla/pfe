# Use an official Node.js runtime as a parent image
FROM node:18-alpine

# Set the working directory in the container
WORKDIR /app

# Copy package.json and package-lock.json (or yarn.lock) files to the container
COPY package*.json ./

# Install dependencies
RUN npm install

# Copy the rest of the application code to the container
COPY . .

# Expose the port Next.js will run on
EXPOSE 3000

# Define environment variable
ENV NODE_ENV=development

# Set the environment variable for the backend URL
# This needs to be consistent with what you put in the docker-compose.yml
ENV NEXT_PUBLIC_BACKEND_URL=http://backend:8000

# Start the Next.js development server
CMD ["npm", "run", "dev"]
