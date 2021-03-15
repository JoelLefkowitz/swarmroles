# Swarm initiator

Initialises a docker swarm

## Extends

- docker

## Sets facts

- swarm_join_addr
- swarm_manager_token
- swarm_worker_token

## Variables

- swarm_advertise_addr - You can set the value to something like "{{ hostvars[groups['manager'][0]].ansible_host }}"