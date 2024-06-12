# Use an official node image as a parent image
FROM node:18

# Set the working directory
WORKDIR /app

# Copy the package.json and package-lock.json to the working directory
COPY package*.json ./

# Install dependencies
RUN npm install

# Update browserslist database
RUN npx browserslist@latest --update-db

# Copy the rest of the application code to the working directory
COPY . .

# Build the Vite app for production
RUN npm run build

# Expose the port the app runs on
EXPOSE 5173

# Command to run the app
CMD ["npm", "run", "dev"]



# docker build -t my-react-app .
# docker run -p 5173:5173 my-react-app
