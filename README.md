# Swarmroles

Roles for deploying a docker swarm.

## Status

| Source     | Shields                                                        |
| ---------- | -------------------------------------------------------------- |
| Project    | ![license][license] ![release][release]                        |
| Raised     | [![issues][issues]][issues_link] [![pulls][pulls]][pulls_link] |

## Installation

```bash
ansible-galaxy collection install joellefkowitz.swarmroles
```

## Motivating example

Select the first member of the manager group and have them initiate a swarm and perform the certbot authentication.

```yml
- hosts: &swarm_initiator manager[0]
  vars: 
    - domains: example.com
  roles:
    - joellefkowitz.swarmroles.swarm_initiator
    - joellefkowitz.swarmroles.certbot
```

Register the first member of the manager group as the swarm_initiator and pass the swarm tokens to the rest of the manager group. Provide a list of images to pull and a docker username if the images require a login for access. An access token can be issued under the environemnt variable name DOCKER_ACCESS_TOKEN.

```yml
- hosts: manager
  vars:
  - docker_username: joellefkowitz
  - pull_images:
    - joellefkowitz/example:0.1.0_prod
  pre_tasks: &register_swarm_initiator
    - name: Fetch the swarm initiator host
      set_fact:
        swarm_initiator: "{{groups['manager'][0]}}"
  roles:
    - role: joellefkowitz.swarmroles.swarm_manager
      swarm_join_addr: "{{ hostvars[swarm_initiator]['swarm_join_addr'] }}"
      swarm_manager_token: "{{ hostvars[swarm_initiator]['swarm_manager_token'] }}"
```

Perform the same registration for all members of the worker group.

```yml
- hosts: worker
  pre_tasks: *register_swarm_initiator
  roles:
    - role: joellefkowitz.swarmroles.swarm_worker
      swarm_join_addr: "{{ hostvars[swarm_initiator]['swarm_join_addr'] }}"
      swarm_worker_token: "{{ hostvars[swarm_initiator]['swarm_worker_token'] }}"
```

Have a manager deploy the swarm. Copy over the compose file and any environment files required.

```yml
- hosts: *swarm_initiator
  vars:
    - stack_name: prod
    - compose_file: docker-compose.yml
    - env_files:
        - prod.example.env
  roles:
    - joellefkowitz.swarmroles.stack_deployer
```

## Roles

### base

Installs python and setuptools

---

### docker

Installs the docker engine for Ubuntu

#### Extends

* base

---

### swarm_initiator

Initialises a docker swarm

#### Extends

* docker

#### Sets facts

* swarm_join_addr
* swarm_manager_token
* swarm_worker_token

---

### swarm_manager

Joins a docker swarm as a manager and pulls a list of images.

#### Extends

* docker

#### Variables

* swarm_join_addr
* swarm_manager_token
* docker_username
* pull_images (List of strings)

#### Environment

* DOCKER_ACCESS_TOKEN

#### Notes

* Docker login will only be attempted when docker_username is defined

---

### swarm_worker

Joins a docker swarm as a worker

#### Extends

* docker

#### Variables

* swarm_join_addr
* swarm_worker_token

---

### stack_deployer

Deploys a stack to a docker swarm

#### Extends

* docker

#### Variables

* deploy_dir (Defaults to 'deploy')
* compose_file
* env_files (List of strings)
* stack_name

---

### certbot

Performs certbot authentication

#### Variables

* domains (Space separated strings)

#### Notes

* Certbot authentication will be skipped if domains is undefined

* Nginx will be signalled to stop in order to reclaim ports. This will fail softly and be ignored.

### Versioning

[SemVer](http://semver.org/) is used for versioning. For a list of versions available, see the tags on this repository.

Bump2version is used to version and tag changes.
For example:

```bash
bump2version patch
```

Releases are made on every major change.

### Author

- **Joel Lefkowitz** - _Initial work_ - [Joel Lefkowitz][joel_lefkowitz]

See also the list of contributors who participated in this project.

### License

This project is licensed under the MIT License - see the [LICENSE.md](LICENSE.md) file for details

### Acknowledgments

None yet!

[license]: https://img.shields.io/github/license/joellefkowitz/swarmroles
[release]: https://img.shields.io/github/v/tag/joellefkowitz/swarmroles
[issues]: https://img.shields.io/github/issues/joellefkowitz/swarmroles "Issues"
[issues_link]: https://github.com/JoelLefkowitz/swarmroles/issues
[pulls]: https://img.shields.io/github/issues-pr/joellefkowitz/swarmroles "Pull requests"
[pulls_link]: https://github.com/JoelLefkowitz/swarmroles/pulls
[joel_lefkowitz]: https://github.com/JoelLefkowitz