FROM node:20

WORKDIR /app

# Copy only the base dependency list
COPY package.json ./

# Install dependencies for Linux (this also creates a package-lock.json)
RUN npm install --include=optional && \
    npm rebuild esbuild && \
    npm dedupe

# Now copy everything else
COPY . .

EXPOSE 5173

CMD ["npm", "run", "dev"]