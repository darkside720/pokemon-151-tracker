# Dockerfile
FROM nginx:alpine

# Remove default NGINX static content
RUN rm -rf /usr/share/nginx/html/*

# Copy your HTML to the NGINX root
COPY index.html /usr/share/nginx/html/index.html

# Expose port 80
EXPOSE 80

