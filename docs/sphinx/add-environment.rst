.. ## other RADIUSS Project Developers. See the top-level COPYRIGHT file for
.. ## details.
.. ##
.. ## SPDX-License-Identifier: (MIT)

.. _add-environment:

================================
Process to add a new environment
================================

The goal of this project is to be able to build any environment of interest for
RADIUSS, independently, and in a reproducible manner. We aim in particular at
building those environments against Spack develop branch to check that RADIUSS
packages do not get broken by recent changes in Spack.

Pre-requisite
=============

To be used in CI, we need to  make sure your environment can be built
completely isolated of any personnal Spack configuration on LC systems.
All the required configuration needs to be embedded in the environment
directory.

**Note**

You may use this CI to effectively iterate over builds of an environment to fix
it. That's part of the purpose of this repo.

Required adds-on
================

Gitlab section in spack config
------------------------------

Spack will use the ``gitlab-ci`` section to the ``spack.yaml`` file to
generate the pipeline for you environment. In particular, this is where we
map runners to specs. Adding this section should be doable by inspecting
the existing radiuss environement. Create a Pull Request and ask for help
if needed.

CI variables
------------

There are three (3) variables that need to be defined in the CI YAML
configuration in order to make it work.

* `ENV_NAME`: the name of the environment, which must match one of the
  directories under `spack_environments`.

* `SPACK_REPO`: the URL where to clone Spack from.

* `SPACK_REF`: the ref to checkout in Spack repo.

The CI is configured to generate a subpipeline using the environment under the
`spack_environments/<ENV_NAME>`. The two other variables will be retrieved in
this same directory, but GitLab needs an hint.

First, create a file named `ci-variables.yml` in
`spack_environments/<ENV_NAME>`. In this file, add the definition of the
missing variables:

.. code-block:: yaml

  variables:
    SPACK_REPO: <the url to you spack clone or upstream spack>
    SPACK_REF: <the ref (branch, tag) to use in checkout in spack>

Then edit the `.gitlab-ci.yml` file to add a conditional inclusion of you ci
variable file:

.. code-block:: yaml

  include:
    - local: spack-environments/<env_name>/ci-variables.yml
      rules:
        - if: '$ENV_NAME == "<env_name>"'
    - local: spack-environments/radiuss/ci-variables.yml
      rules:
        - if: '$ENV_NAME == "radiuss"'

This simply means that each time the CI runs with `ENV_NAME=<env_name>` it will
include the appropriate variable file. All you need to do to run your
environment pipeline is to set your environement name.

Pull Request worflow
--------------------

We recommend setting your environment name globally in `.gitlab-ci.yml`

Recommended adds-on
===================

Although you may use radiuss-spack-testing to play solo − even clone it in
another GitLab repo − we see it as an opportunity to gather various Spack
environments useful for LLNL.

In particular, we provide a preferred location to create your `install_tree`,
`mirror` (build-cache) and `store` (for concretizer bootstrap).

.. note::

  The following recommendation applies to those belonging to the RADIUSS
  group only. We could workaround that using the radiuss service user in
  the future.

Getting Started configuration
-----------------------------

As a getting started recommendation, and if you belong to RADIUSS group, we
recommend creating a directory with you `ENV_NAME` in:

* `/usr/workspace/radiuss/installs/<env_name>`
* `/usr/workspace/radiuss/mirrors/<env_name>`
* `/usr/workspace/radiuss/stores/<env_name>`

.. note::

  Immediately addapt the permissions so that the RADIUSS group has write
  access on those:

.. code-block:: bash

  chmod -R g+rwX /usr/workspace/radiuss/installs/<env_name>
  chmod -R g+rwX /usr/workspace/radiuss/mirrors/<env_name>
  chmod -R g+rwX /usr/workspace/radiuss/stores/<env_name>

Then, point your environment configuration to those locations. For install
tree, use:

.. code-block:: yaml

  config:
    install_tree:
      root: /usr/workspace/radiuss/install/radiuss
      padded_length: 128
      projections:
        all: '{architecture}/{compiler.name}-{compiler.version}/{name}-{version}-{hash}'

For the mirror location, use:

.. code-block:: yaml

  mirrors:
    mirror: file:///usr/workspace/radiuss/mirrors/radiuss

For the store location, use:

.. code-block:: yaml

  bootstrap:
    root: /usr/workspace/radiuss/store/radiuss
