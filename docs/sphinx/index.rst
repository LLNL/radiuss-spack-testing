.. ## Copyright (c) 2019-2021, Lawrence Livermore National Security, LLC and
.. ## other RADIUSS Project Developers. See the top-level COPYRIGHT file for details.
.. ##
.. ## SPDX-License-Identifier: (MIT)

Welcome to Radiuss Spack Testing!
=================================

RADIUSS Spack Testing is a sub-project from the RADIUSS initiative providing a
testing infrastructure to test Spack Packages automatically in GitLab while
tracking changes in Spack.

LLNL's RADIUSS project (Rapid Application Development via an Institutional
Universal Software Stack) aims to broaden usage across LLNL and the open source
community of a set of libraries and tools used for HPC scientific application
development.


What exactly is this repo about?
================================

In this repo, we configured Gitlab CI to generate CI pipelines that build any
spack environement we were provided with.

We rely on `Spack Pipeline feature <https://spack.readthedocs.io/en/latest/pipelines.html>`_
to generate the CI pipeline.

In each pipeline we only will build one of the Spack environments that can be
found in the ``spack_environments`` directory.

The intended use is to setup schedules to build those environments individually,
on a regular basis, and to report the results to the interested people.

This can also be used to populate and update a Spack build cache with specs
that have be selected and gathered in a Spack environment.


How to submit a new environment?
================================

We will use Pull Requests (PRs) to accept new environments. Any environment
that is of interest for the RADIUSS project could be candidate. But some
changes are required to make those usable in this context.

Also, we share in <recommendations for environment configuration> what we
consider good practices.


Notes on Spack Pipeline Feature
===============================

Interested in how this repo works? It is a good idea to first read the
`Spack documentation about the pipeline feature <https://spack.readthedocs.io/en/latest/pipelines.html>`_.

Then, the <spack-pipeline-feature> section aims at complementing the above
documentation with on details that may differ from the initially intended use.


Table of Contents
=================

.. toctree::
   :maxdepth: 2

   structure
   add-environment
   spack-pipeline-feature

Indices and tables
==================

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`
