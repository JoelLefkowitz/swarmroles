# Certbot

Performs certbot authentication

## Variables

* domains (Space separated strings)

## Notes

* Certbot authentication will be skipped if domains is undefined

* Nginx will be signalled to stop in order to reclaim ports. This will fail softly and be ignored.
