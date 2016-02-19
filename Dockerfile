FROM ubuntu
MAINTAINER leifj@sunet.se
RUN apt-get -q update
RUN apt-get -y upgrade
RUN apt-get -y install apache2 libapache2-mod-shib2 ssl-cert augeas-tools
RUN a2enmod rewrite
RUN a2enmod shib2
RUN a2enmod proxy
RUN a2enmod proxy_http
RUN a2enmod ssl
ENV SP_HOSTNAME localhost
ENV SP_CONTACT root@localhost
ENV SP_ABOUT /about
ENV DISCO_URL https://md.nordu.net/role/idp.ds
ENV METADATA_URL http://md.swamid.se/md/swamid-idp-transitive.xml
ENV METADATA_SIGNER md-signer.crt
RUN rm -f /etc/apache2/sites-available/*
ADD config /etc/apache2/sites-available/default.conf
RUN rm -f /etc/apache2/sites-enabled/*
RUN a2ensite default
COPY start.sh /
RUN chmod a+rx /start.sh
COPY md-signer.crt /etc/shibboleth/
RUN cp /etc/apache2/sites-available/default.conf /etc/apache2/sites-available/default.conf.ORIG
RUN cp /etc/shibboleth/shibboleth2.xml /etc/shibboleth/shibboleth2.xml.ORIG
COPY attribute-map.xml /etc/shibboleth/
COPY apache2.conf /etc/apache2/
EXPOSE 80
VOLUME /credentials
ENTRYPOINT ["/start.sh"]
