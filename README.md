
Simple Shibboleth SP
====================

A shibboleth SP (apache 2.4 on ubuntu) docker-image pre-configured for SWAMID login. To trigger 
login redirect the browser to "/Shibboleth.sso/Login?targt=$application-session-handler" where
$application-session-handler is the URL context where your application establishes an internal
session.  The apache is setup with a single default vhost setup to serve $SP_HOSTNAME only 
on TLS (http traffic is redirected)

Typical Use
-----------

Extend this docker image with your own Dockerfile (FROM swamid-shibsp) where you COPY and 
ADD your own application. To add configuration to the Apache the suggested approach is to
COPY something into /etc/apache2/conf.d (and any other data/code you need) and run a2enconf
from the Dockerfile. An example might look something like this:

```
FROM swamid-shibsp
COPY myapp /var/www/
COPY myconf.conf /etc/apache2/conf.d
RUN a2enconf myconf
```

Your application should provide a /about URL - the Shibboleth module may redirect the user
to this URL for addl info about the application.

Environment variables and mounts
----------------

Stuff you must set:

* SP_HOSTNAME (localhost): set to the public hostname of the application (eg foo.example.com)
* SP_CONTACT (info@${SP_HOSTNAME}): set to the "webmaster" email of the application

Volyme to mount:

* /etc/ssl

This should contain a standard ubuntu/debian layout (/etc/ssl/certs, /etc/ssl/private etc).
Unless found, private/${SP_HOSTNAME}.key, certs/${SP_HOSTNAME}.crt and certs/${SP_HOSTNAME-chain.crt
will be generated (you will want to replace these with "real" certs btw) along with a keypair
for use by Shibboleth to sign SAML messages. This last keypair you will probably not need 
to replace or override but it is in private/shibsp.key and certs/shibsp.crt.

Advanced Config
---------------

By default the NORDUnet DS is uses and SWAMID transitive metadata (includes all of edugain
etc) is loaded. You can override these defaults by setting METADATA_URL and DISCO_URL to 
point to alternative metadata and discovery service URLs respectively.

You can also override the METADATA_SIGNER but that cert needs to be COPY:ed into the 
/etc/shibboleth directory in your own Docker file.
