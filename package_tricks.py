##############################################################################
# Copyright (c) 2013-2017, Lawrence Livermore National Security, LLC.
# Produced at the Lawrence Livermore National Laboratory.
#
# This file is part of Spack.
# Created by Todd Gamblin, tgamblin@llnl.gov, All rights reserved.
# LLNL-CODE-647188
#
# For details, see https://github.com/llnl/spack
# Please also see the NOTICE and LICENSE files for our notice and the LGPL.
#
# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU Lesser General Public License (as
# published by the Free Software Foundation) version 2.1, February 1999.
#
# This program is distributed in the hope that it will be useful, but
# WITHOUT ANY WARRANTY; without even the IMPLIED WARRANTY OF
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the terms and
# conditions of the GNU Lesser General Public License for more details.
#
# You should have received a copy of the GNU Lesser General Public
# License along with this program; if not, write to the Free Software
# Foundation, Inc., 59 Temple Place, Suite 330, Boston, MA 02111-1307 USA
##############################################################################
from spack import *

# NOTES: This is just a collection of tips on how to use and further explore
# Spack's API when creating packages. Get inspiration for building Spack
# packages with extensions here: https://github.com/LLNL/spack/pull/3644/files
# (and possibly other Spack packages which build bindings for Python and Perl).


class ManateeOpen(AutotoolsPackage):
    """Manatee corpus management system and query engine."""

    homepage = "https://nlp.fi.muni.cz/trac/noske"

    # older versions are in the archive/ subdirectory; indicate this by adding
    # an archive=True kwarg to the version directive
    version("2.151.5", "94aa86405de1038260a750269caebed9")
    version("2.150",   "8c143bfa6378cc0cccd7efad868f9040")
    version("2.139.3", "4a000d54ec3cfec7d6a77a3ff0f11ba9", archive=True)

    variant("pcre", default=True, description="Build with PCRE.")
    variant("python", default=True, description="Build Python bindings.")
    variant("perl", default=True, description="Build Perl bindings.")
    # ruby and java bindings are also supposedly available, but god knows which
    # versions of ruby and java are supported... also, I'd rather not have to
    # figure out how to hook up the bindings to two additional languages unless
    # absolutely necessary
    # variant("ruby", default=False, description="Build Ruby bindings.")
    # variant("java", default=False, description="Build Java bindings.")

    # available dependency types are build, link and run; the default is
    # ("build", "link")
    # cf. also http://spack.readthedocs.io/en/latest/packaging_guide.html#dependencies
    depends_on("bison@3:", type="build")
    depends_on("swig", type="build", when="+python")
    depends_on("swig", type="build", when="+perl")
    depends_on("finlib +pcre", when="+pcre")
    depends_on("finlib -pcre", when="-pcre")
    # always at least depends on python (sbangs must be patched)
    depends_on("python@2.6:2.10", when="-python")
    extends("python@2.6:2.10", when="+python")
    extends("perl", when="+perl")
    # depends_on("ruby", when="+ruby")
    # depends_on("jdk", when="+java")

    patch("configure.patch", when="+perl")

    # override docstring formatting
    def format_doc(self, **kwargs):
        return "    {}\n".format(self.__doc__.strip())

    def url_for_version(self, version):
        dirpath = "http://corpora.fi.muni.cz/noske/src/manatee-open"
        fpath = "manatee-open-{}.tar.gz".format(version)
        if self.versions[version].get("archive", False):
            return "/".join([dirpath, "archive", fpath.format(version[1])])
        else:
            return "/".join([dirpath, fpath.format(version[0])])

    # altering the environment: https://github.com/LLNL/spack/pull/1323/files
    # def setup_environment(self, spack_env, run_env):
    #     perl = self.spec["perl"]
    #     perl_site_pkg = join_path(self.prefix.lib.site_perl, perl.version, )
    #     spack_env.add("PERL_SITE_PKG", perl_site_pkg)

    def configure_args(self):
        # for attr in dir(self):
        #     if not attr.startswith("_"):
        #         try:
        #             print attr, "::", getattr(self, attr)
        #         except Exception:
        #             pass
        # assert 0
        # dep = self.spec["perl"]
        # for attrname in dir(dep):
        #     # if attrname == "libs":
        #     #     continue
        #     try:
        #         attr = getattr(dep, attrname)
        #     except:
        #         attr = "!!! Couldn't get attr value !!!"
        #     if not attrname.startswith("_") and not callable(attr):
        #         print("========================================================================")
        #         print(attrname)
        #         print(attr)
        # assert 0
        args = []

        if "+pcre" in self.spec:
            args.append("--with-pcre")

        if "-python" in self.spec:
            args.append("--disable-python")

        if "+perl" in self.spec:
            args.append("--enable-perl")

        # if "+ruby" in self.spec:
        #     args.append("--enable-ruby")
        #     args.append("LDFLAGS=-L{}".format(self.spec["ruby"].prefix.lib.ruby))
        #
        # if "+java" in self.spec:
        #     args.append("--enable-java")

        return args

    @run_before("install")
    def filter_sbang(self):
        # filter sbang before install so Spack's sbang hook can fix it up if
        # it's too long
        files = [f for f in find("api", "*", recurse=False) if is_exe(f)]
        python = join_path(self.spec["python"].prefix.bin, "python")
        filter_file(r"^#!\s*/usr/bin.*python", r"#!{}".format(python), *files)

    # @run_before("configure")
    # def check_python_and_perl(self):
    #     python = which("python")
    #     python("-c", "import sys; print sys.prefix")
    #     perl = which("perl")
    #     perl("-MConfig", "-e", r'print "$Config{installsitearch}\n"')
    #     assert 0


# this is what an ignore function should look like:
def ignore(filename):
    spec_ignore = args["ignore"]
    if spec_ignore:
        # this is what transforms a regex into a matching predicate
        spec_match = llnl.util.lang.match_predicate(spec_ignore)
    else:
        spec_match = lambda f: False
    # don't forget customarily ignored files
    return filename in spack.store.layout.hidden_file_paths or spec_match(filename)
