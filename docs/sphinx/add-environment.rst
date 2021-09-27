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

The very first step is to make sure your environment can be built completely
isolated of any personnal Spack configuration, on LC systems. All the required
configuration needs to be embedded in the environment directory.

Then you need to add the ``gitlab-ci`` section to the ``spack.yaml`` file. This
should be doable by inspecting the existing radiuss environement. Create a Pull
Request and ask for help if needed.

Finally, adding an environment to the CI is easy. Most of the work being to
update in the UI the environment variables mentioned above.
