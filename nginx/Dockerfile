FROM nginx:latest

# This step is not required normally, but in rare cases, files in /etc/nginx may be removed by COPY command.
# So move them to nginxcopy and then copy them back
RUN mv /etc/nginx /etc/nginxcopy\
    && rm /etc/nginxcopy/nginx.conf

COPY nginx.conf /etc/nginx/nginx.conf
COPY my_nginx.conf /etc/nginx/sites-available/
COPY ./dist /dist

RUN mkdir -p /etc/nginx/sites-enabled/\
    && ln -s /etc/nginx/sites-available/my_nginx.conf /etc/nginx/sites-enabled/

# Copy files in /etc/nginxcopy back to /etc/nginx
RUN cp -r /etc/nginxcopy/* /etc/nginx/

CMD ["nginx", "-g", "daemon off;"]
