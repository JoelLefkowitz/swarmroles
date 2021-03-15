# Certbot

Performs certbot authentication

## Variables

- domains (Space separated strings)

## Notes

- Certbot authentication will be skipped if domains is undefined

- Nginx will be signalled to stop in order to reclaim ports. This will fail softly and be ignored.

## Explanation

When deploying a webapp to a swarm I often have an nginx service that exposes an https endpoint. In the docker-compose file I bind the certificate on the swarm node to the service.

```yml
volumes:
  - type: bind
    source: /etc/letsencrypt/live/joellefkowitz.co.uk/fullchain.pem
    target: /etc/nginx/joellefkowitz.co.uk.crt
  - type: bind
    source: /etc/letsencrypt/live/joellefkowitz.co.uk/privkey.pem
    target: /etc/nginx/joellefkowitz.co.uk.key
```

So in the same way that pulling images and copying necessary files must happen on every manager node, we may also need to fetch certificates from an external source so that the services have everything they need in order to launch.
