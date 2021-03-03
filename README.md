# Swarmroles

Ansible roles for deploying a docker swarm.

## Status

| Source     | Shields                                                                                                            |
| ---------- | ------------------------------------------------------------------------------------------------------------------ |
| Project    | ![release][release_shield] ![license][license_shield] ![dependents][dependents_shield]                             |
| Health     | ![travis][travis_shield] ![codacy][codacy_shield] ![coverage][coverage_shield] ![readthedocs][readthedocs_shield]  |
| Repository | ![issues][issues_shield] ![pulls][pulls_shield]                                                                    |
| Activity   | ![contributors][contributors_shield] ![monthly_commits][monthly_commits_shield] ![last_commit][last_commit_shield] |

## Installation

```bash
ansible-galaxy collection install joellefkowitz.swarmroles
```

## Motivating example

Select the first member of the manager group and have them initiate a swarm and perform the certbot authentication.

```yml
- hosts: &swarm_initiator manager[0]
  user: root
  vars: 
    - domains: example.com
  roles:
    - joellefkowitz.swarmroles.swarm_initiator
    - joellefkowitz.swarmroles.certbot
```

Register the first member of the manager group as the swarm_initiator and pass the swarm tokens to the rest of the manager group. Provide a list of images to pull and a docker username if the images require a login for access. An access token can be issued under the environemnt variable name DOCKER_ACCESS_TOKEN.

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

## Tests

To run unit tests:

```bash
grunt tests:unit
```

To generate a coverage report:

```bash
grunt tests:coverage
```

## Documentation

This repository's documentation is hosted on [readthedocs][readthedocs].

To generate the sphinx configuration:

```bash
grunt docs:generate
```

Then build the documentation:

```bash
grunt docs:build
```

## Tooling

To run linters:

```bash
grunt lint
```

To run formatters:

```bash
grunt format
```

Before commiting new code:

```bash
grunt precommit
```

This will run linters, formaters, generate a test coverage report and the sphinx configuration.

## Versioning

This repository adheres to semantic versioning standards.
For more inforamtion on semantic versioning visit [SemVer][semver].

Bump2version is used to version and tag changes.
For example:

```bash
bump2version patch
```

## Changelog

Please read this repository's [CHANGELOG](CHANGELOG.md) for details on changes that have been made.

## Contributing

Please read this repository's guidelines on [CONTRIBUTING](CONTRIBUTING.md) for details on our code of conduct and the process for submitting pull requests.

## Contributors

- **Joel Lefkowitz** - _Initial work_ - [Joel Lefkowitz][joellefkowitz]

[![Buy Me A Coffee][coffee_button]][coffee]

## Remarks

Lots of love to the open source community!

![Be kind][be_kind]

<!-- Github links -->

[pulls]: https://github.com/JoelLefkowitz/swarmroles/pulls
[issues]: https://github.com/JoelLefkowitz/swarmroles/issues

<!-- External links -->

[readthedocs]: https://swarmroles.readthedocs.io/en/latest/
[semver]: http://semver.org/
[coffee]: https://www.buymeacoffee.com/joellefkowitz
[coffee_button]: https://cdn.buymeacoffee.com/buttons/default-blue.png
[be_kind]: https://media.giphy.com/media/osAcIGTSyeovPq6Xph/giphy.gif

<!-- Acknowledgments -->

[joellefkowitz]: https://github.com/JoelLefkowitz

<!-- Project shields -->

[release_shield]: https://img.shields.io/github/v/tag/joellefkowitz/swarmroles
[license_shield]: https://img.shields.io/github/license/joellefkowitz/swarmroles
[dependents_shield]: https://img.shields.io/librariesio/dependent-repos/pypi/swarmroles

<!-- Health shields -->

[travis_shield]: https://img.shields.io/travis/joellefkowitz/swarmroles
[codacy_shield]: https://img.shields.io/codacy/coverage/swarmroles
[coverage_shield]: https://img.shields.io/codacy/grade/swarmroles
[readthedocs_shield]: https://img.shields.io/readthedocs/swarmroles

<!-- Repository shields -->

[issues_shield]: https://img.shields.io/github/issues/joellefkowitz/swarmroles
[pulls_shield]: https://img.shields.io/github/issues-pr/joellefkowitz/swarmroles

<!-- Activity shields -->

[contributors_shield]: https://img.shields.io/github/contributors/joellefkowitz/swarmroles
[monthly_commits_shield]: https://img.shields.io/github/commit-activity/m/joellefkowitz/swarmroles
[last_commit_shield]: https://img.shields.io/github/last-commit/joellefkowitz/swarmroles
