# Copyright 2013-2021 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

import os
import socket
from os.path import join as pjoin

from spack import *


def get_spec_path(spec, package_name, path_replacements={}, use_bin=False):
    """Extracts the prefix path for the given spack package
       path_replacements is a dictionary with string replacements for the path.
    """

    if not use_bin:
        path = spec[package_name].prefix
    else:
        path = spec[package_name].prefix.bin

    path = os.path.realpath(path)

    for key in path_replacements:
        path = path.replace(key, path_replacements[key])

    return path


class Blt-test(CachedCMakePackage, CudaPackage, ROCmPackage):
    """This is a package meant to test out basic Spack environments
       against BLT's smoke and internal tests"""

    maintainers = ['white238']

    homepage = "https://github.com/LLNL/blt"
    url      = "https://github.com/LLNL/blt/archive/v0.4.0.tar.gz"
    git      = "https://github.com/LLNL/blt.git"
    tags     = ['radiuss']

    maintainers = ['white238', 'davidbeckingsale']

    version('develop', branch='develop')
    version('main', branch='main')
    # Note: 0.4.0+ contains a breaking change to BLT created targets
    #  if you export targets this could cause problems in downstream
    #  projects if not handled properly. More info here:
    #  https://llnl-blt.readthedocs.io/en/develop/tutorial/exporting_targets.html
    version('0.4.1', sha256='16cc3e067ddcf48b99358107e5035a17549f52dcc701a35cd18a9d9f536826c1')
    version('0.4.0', sha256='f3bc45d28b9b2eb6df43b75d4f6f89a1557d73d012da7b75bac1be0574767193')
    version('0.3.6', sha256='6276317c29e7ff8524fbea47d9288ddb40ac06e9f9da5e878bf9011e2c99bf71')
    version('0.3.5', sha256='68a1c224bb9203461ae6f5ab0ff3c50b4a58dcce6c2d2799489a1811f425fb84')
    version('0.3.0', sha256='bb917a67cb7335d6721c997ba9c5dca70506006d7bba5e0e50033dd0836481a5')
    version('0.2.5', sha256='3a000f60194e47b3e5623cc528cbcaf88f7fea4d9620b3c7446ff6658dc582a5')
    version('0.2.0', sha256='c0cadf1269c2feb189e398a356e3c49170bc832df95e5564e32bdbb1eb0fa1b3')

    root_cmakelists_dir = 'tests/internal'

    # -----------------------------------------------------------------------
    # Variants
    # -----------------------------------------------------------------------
    variant('shared',   default=True,
            description='Enable build of shared libraries')
    variant('debug',    default=False,
            description='Build debug instead of optimized version')

    # TODO: change this to a variant with options (cpp11, cpp14, etc...)
    #variant('cpp14',    default=True, description="Build with C++14 support")

    variant('fortran',  default=True, description="Build with Fortran support")

    variant("mpi",      default=True, description="Build MPI support")
    variant('openmp',   default=True, description='Turn on OpenMP support.')

    # -----------------------------------------------------------------------
    # Dependencies
    # -----------------------------------------------------------------------
    # Basics
    depends_on("cmake@3.8.2:", type='build')
    depends_on("mpi", when="+mpi")

    def flag_handler(self, name, flags):
        if self.spec.satisfies('%cce') and name == 'fflags':
            flags.append('-ef')

        if name in ('cflags', 'cxxflags', 'cppflags', 'fflags'):
            return (None, None, None)  # handled in the cmake cache
        return (flags, None, None)

    def _get_sys_type(self, spec):
        sys_type = spec.architecture
        # if on llnl systems, we can use the SYS_TYPE
        if "SYS_TYPE" in env:
            sys_type = env["SYS_TYPE"]
        return sys_type

    @property
    def cache_name(self):
        hostname = socket.gethostname()
        if "SYS_TYPE" in env:
            # Are we on a LLNL system then strip node number
            hostname = hostname.rstrip('1234567890')
        return "{0}-{1}-{2}@{3}.cmake".format(
            hostname,
            self._get_sys_type(self.spec),
            self.spec.compiler.name,
            self.spec.compiler.version
        )

    def initconfig_compiler_entries(self):
        spec = self.spec
        entries = super(Axom, self).initconfig_compiler_entries()

        if "+fortran" in spec or self.compiler.fc is not None:
            entries.append(cmake_cache_option("ENABLE_FORTRAN", True))
        else:
            entries.append(cmake_cache_option("ENABLE_FORTRAN", False))

        if ((self.compiler.fc is not None)
           and ("gfortran" in self.compiler.fc)
           and ("clang" in self.compiler.cxx)):
            libdir = pjoin(os.path.dirname(
                           os.path.dirname(self.compiler.cxx)), "lib")
            flags = ""
            for _libpath in [libdir, libdir + "64"]:
                if os.path.exists(_libpath):
                    flags += " -Wl,-rpath,{0}".format(_libpath)
            description = ("Adds a missing libstdc++ rpath")
            if flags:
                entries.append(cmake_cache_string("BLT_EXE_LINKER_FLAGS", flags,
                                                  description))

        # TODO: reenable when multi-variable variant is made
        # if "+cpp14" in spec:
        #     entries.append(cmake_cache_string("BLT_CXX_STD", "c++14", ""))

        return entries

    def initconfig_hardware_entries(self):
        spec = self.spec
        entries = super(Blt-test, self).initconfig_hardware_entries()

        if "+cuda" in spec:
            entries.append(cmake_cache_option("ENABLE_CUDA", True))

            # CUDA_FLAGS
            cudaflags  = "-restrict --expt-extended-lambda "

            if not spec.satisfies('cuda_arch=none'):
                cuda_arch = spec.variants['cuda_arch'].value[0]
                entries.append(cmake_cache_string(
                    "CMAKE_CUDA_ARCHITECTURES",
                    cuda_arch))
                cudaflags += '-arch sm_${CMAKE_CUDA_ARCHITECTURES} '
            else:
                entries.append(
                    "# cuda_arch could not be determined\n\n")

            # TODO: reenable when multi-variable variant is made
            # if "+cpp14" in spec:
            #     cudaflags += " -std=c++14"
            # else:
            #     cudaflags += " -std=c++11"
            entries.append(
                cmake_cache_string("CMAKE_CUDA_FLAGS", cudaflags))

            entries.append(
                "# nvcc does not like gtest's 'pthreads' flag\n")
            entries.append(
                cmake_cache_option("gtest_disable_pthreads", True))

        entries.append("#------------------{0}".format("-" * 30))
        entries.append("# Hardware Specifics")
        entries.append("#------------------{0}\n".format("-" * 30))

        # OpenMP
        entries.append(cmake_cache_option("ENABLE_OPENMP",
                                          spec.satisfies('+openmp')))

        # Enable death tests
        entries.append(cmake_cache_option(
            "ENABLE_GTEST_DEATH_TESTS",
            not spec.satisfies('+cuda target=ppc64le:')
        ))

        if (self.compiler.fc is not None) and ("xlf" in self.compiler.fc):
            # Grab lib directory for the current fortran compiler
            libdir = pjoin(os.path.dirname(
                           os.path.dirname(self.compiler.fc)),
                           "lib")
            description = ("Adds a missing rpath for libraries "
                           "associated with the fortran compiler")

            linker_flags = "${BLT_EXE_LINKER_FLAGS} -Wl,-rpath," + libdir

            entries.append(cmake_cache_string("BLT_EXE_LINKER_FLAGS",
                                              linker_flags, description))

            if "+shared" in spec:
                linker_flags = "${CMAKE_SHARED_LINKER_FLAGS} -Wl,-rpath," \
                               + libdir
                entries.append(cmake_cache_string(
                    "CMAKE_SHARED_LINKER_FLAGS",
                    linker_flags, description))

            description = ("Converts C-style comments to Fortran style "
                           "in preprocessed files")
            entries.append(cmake_cache_string(
                "BLT_FORTRAN_FLAGS",
                "-WF,-C!  -qxlf2003=polymorphic",
                description))

            if spec.satisfies('target=ppc64le:'):
                # Fix for working around CMake adding implicit link directories
                # returned by the BlueOS compilers to link executables with
                # non-system default stdlib
                _roots = ["/usr/tce/packages/gcc/gcc-4.9.3",
                          "/usr/tce/packages/gcc/gcc-4.9.3/gnu"]
                _subdirs = ["lib64",
                            "lib64/gcc/powerpc64le-unknown-linux-gnu/4.9.3"]
                _existing_paths = []
                for root in _roots:
                    for subdir in _subdirs:
                        _curr_path = pjoin(root, subdir)
                        if os.path.exists(_curr_path):
                            _existing_paths.append(_curr_path)
                if _existing_paths:
                    entries.append(cmake_cache_string(
                        "BLT_CMAKE_IMPLICIT_LINK_DIRECTORIES_EXCLUDE",
                        ";".join(_existing_paths)))

        return entries

    def initconfig_mpi_entries(self):
        spec = self.spec
        entries = super(Blt-test, self).initconfig_mpi_entries()

        if "+mpi" in spec:
            entries.append(cmake_cache_option("ENABLE_MPI", True))
            if spec['mpi'].name == 'spectrum-mpi':
                entries.append(cmake_cache_string("BLT_MPI_COMMAND_APPEND",
                                                  "mpibind"))
        else:
            entries.append(cmake_cache_option("ENABLE_MPI", False))

        return entries


    def cmake_args(self):
        options = []

        if self.run_tests is False:
            options.append('-DENABLE_TESTS=OFF')
        else:
            options.append('-DENABLE_TESTS=ON')

        options.append(self.define_from_variant(
            'BUILD_SHARED_LIBS', 'shared'))

        return options
