FROM httpd:2.4

RUN apt-get update && apt-get install -y openssl && rm -rf /var/lib/apt/lists/*

RUN sed -i 's/#LoadModule ssl_module/LoadModule ssl_module/' /usr/local/apache2/conf/httpd.conf
RUN sed -i 's/#LoadModule socache_shmcb_module/LoadModule socache_shmcb_module/' /usr/local/apache2/conf/httpd.conf
RUN sed -i 's/#LoadModule rewrite_module/LoadModule rewrite_module/' /usr/local/apache2/conf/httpd.conf
RUN sed -i 's/#LoadModule proxy_module/LoadModule proxy_module/' /usr/local/apache2/conf/httpd.conf
RUN sed -i 's/#LoadModule proxy_http_module/LoadModule proxy_http_module/' /usr/local/apache2/conf/httpd.conf
RUN echo "Listen 443" >> /usr/local/apache2/conf/httpd.conf



COPY default.conf /usr/local/apache2/conf/extra/default.conf
RUN echo "Include /usr/local/apache2/conf/extra/default.conf" >> /usr/local/apache2/conf/httpd.conf
COPY ssl/server.crt /usr/local/apache2/conf/server.crt
COPY ssl/server.key /usr/local/apache2/conf/server.key
