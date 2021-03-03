# Swarm manager

Joins a docker swarm as a manager and pulls a list of images.

## Extends

- docker

## Variables

- swarm_join_addr
- swarm_manager_token
- docker_username
- pull_images (List of strings)

## Environment

- DOCKER_ACCESS_TOKEN

## Notes

- Docker login will only be attempted when docker_username is defined
