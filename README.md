# Swarmroles

Ansible roles for deploying a docker swarm.

![Review](https://img.shields.io/github/actions/workflow/status/JoelLefkowitz/swarmroles/review.yml)
![Version](https://img.shields.io/pypi/v/swarmroles)
![Downloads](https://img.shields.io/pypi/dw/swarmroles)

## Documentation

Documentation and more detailed examples are hosted on [Github Pages](https://joellefkowitz.github.io/swarmroles).

## Usage

Select the first member of the manager group and have them initiate a swarm.

```yml
- hosts: &swarm_initiator manager[0]
  user: root
  vars:
    - domains: example.com
  roles:
    - joellefkowitz.swarmroles.swarm_initiator
```

Register the first member of the manager group as the swarm_initiator and pass the swarm tokens to the rest of the manager group. Provide a list of images to pull and a docker username if the images require a login for access. An access token can be issued under the environment variable name DOCKER_ACCESS_TOKEN.

```yml
- hosts: manager
  user: root
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
  user: root
  pre_tasks: *register_swarm_initiator
  roles:
    - role: joellefkowitz.swarmroles.swarm_worker
      swarm_join_addr: "{{ hostvars[swarm_initiator]['swarm_join_addr'] }}"
      swarm_worker_token: "{{ hostvars[swarm_initiator]['swarm_worker_token'] }}"
```

Have a manager deploy the swarm. Copy over the compose file and any environment files required.

```yml
- hosts: *swarm_initiator
  user: root
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

### docker

Installs the docker engine for Ubuntu

#### Extends

- base

### swarm_initiator

Initializes a docker swarm

#### Extends

- docker

#### Sets facts

- swarm_join_addr
- swarm_manager_token
- swarm_worker_token

### swarm_manager

Joins a docker swarm as a manager and pulls a list of images.

#### Extends

- docker

#### Variables

- swarm_join_addr
- swarm_manager_token
- docker_username
- pull_images (List of strings)

#### Environment

- DOCKER_ACCESS_TOKEN

#### Notes

- Docker login will only be attempted when docker_username is defined

### swarm_worker

Joins a docker swarm as a worker

#### Extends

- docker

#### Variables

- swarm_join_addr
- swarm_worker_token

### stack_deployer

Deploys a stack to a docker swarm

#### Extends

- docker

#### Variables

- deploy_dir (Defaults to 'deploy')
- compose_file
- env_files (List of strings)
- stack_name

## Tooling

### Dependencies

To install dependencies:

```bash
yarn install
pip install .[all]
```

### Tests

To run tests:

```bash
thx test
```

### Documentation

To generate the documentation locally:

```bash
thx docs
```

### Linters

To run linters:

```bash
thx lint
```

### Formatters

To run formatters:

```bash
thx format
```

## Contributing

Please read this repository's [Code of Conduct](CODE_OF_CONDUCT.md) which outlines our collaboration standards and the [Changelog](CHANGELOG.md) for details on breaking changes that have been made.

This repository adheres to semantic versioning standards. For more information on semantic versioning visit [SemVer](https://semver.org).

Bump2version is used to version and tag changes. For example:

```bash
bump2version patch
```

### Contributors

- [Joel Lefkowitz](https://github.com/joellefkowitz) - Initial work

## Remarks

Lots of love to the open source community!

<div align='center'>
    <img width=200 height=200 src='https://media.giphy.com/media/osAcIGTSyeovPq6Xph/giphy.gif' alt='Be kind to your mind' />
    <img width=200 height=200 src='https://media.giphy.com/media/KEAAbQ5clGWJwuJuZB/giphy.gif' alt='Love each other' />
    <img width=200 height=200 src='https://media.giphy.com/media/WRWykrFkxJA6JJuTvc/giphy.gif' alt="It's ok to have a bad day" />
</div>
