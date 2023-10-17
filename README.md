# RADIUSS Spack Testing

The RADIUSS project promotes and supports key High Performance Computing (HPC) open-source software developed at the LLNL. These tools and libraries cover a wide range of features a team would need to develop a modern simulation code targeting HPC plaftorms.

RADIUSS Spack Testing is a sub-project from the RADIUSS initiative providing a
testing infrastructure to test Spack Packages automatically in GitLab while
tracking changes in Spack.

Access the [documentation](https://radiuss-spack-testing.readthedocs.io/).

## Getting Started

The primary goal of this repo is to be used in Gitlab. The Gitlab CI configuration is such that it will use Spack pipeline feature to generate and run a pipeline that builds one of the environments in the `spack-environments` directory.

The specific environment to be built is controlled by the CI variable `MY_ENV_NAME`.

### Installing

This project requires no installation.

## Contributing

Please read [CONTRIBUTING.md](https://github.com/LLNL/radiuss-spack-testing/CONTRIBUTING.md) for details on our code of conduct, and the process for submitting pull requests to us.

## Versioning

version: 1.0.0

TODO: Not even sure how to handle versioning here.

## Authors

Adrien M Bernede

See also the list of [contributors](https://github.com/LLNL/radiuss-spack-testing/contributors) who participated in this project.

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details

All new contributions must be made under the MIT License.

See [LICENSE](https://github.com/LLNL/radiuss-spack-testing/blob/master/LICENSE),
[COPYRIGHT](https://github.com/LLNL/radiuss-spack-testing/blob/master/COPYRIGHT), and
[NOTICE](https://github.com/LLNL/radiuss-spack-testing/blob/master/NOTICE) for details.

SPDX-License-Identifier: (MIT)

LLNL-CODE-793462


## Acknowledgments


