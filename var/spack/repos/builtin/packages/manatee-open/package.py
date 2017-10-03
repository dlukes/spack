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


class ManateeOpen(AutotoolsPackage):
    """Manatee corpus management system and query engine.

    Python and Perl bindings are installed into *Manatee's* prefix. To symlink
    them into Python's and Perl's prefixes, run the following:

      $ spack python activate_manatee_bindings.py activate

    To remove the symlinks, run:

      $ spack python activate_manatee_bindings.py deactivate

    ===========================================================================

    If you can't use the above solution for some reason, here are some tips on
    alternative ways to set things up.

    To use the Python module, either add the appropriate directory to your
    PYTHONPATH or create a hardlinked view:

      $ spack view --verbose hardlink path/to/view python manatee-open

    The hardlink solution doesn't work for Perl because it seems to hardcode
    the paths in @@INC upon install. So with Perl, just change PERL5LIB (for
    interactive use) or add the directory to @@INC in your script.

    """
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

    depends_on("bison@3:", type="build")
    depends_on("swig", type="build", when="+python")
    depends_on("swig", type="build", when="+perl")
    depends_on("finlib +pcre", when="+pcre")
    depends_on("finlib -pcre", when="-pcre")
    # always at least depends on python (sbangs must be patched)
    depends_on("python@2.6:2.99")
    # TODO: activating multiple extendees currently doesn't work, see TODOs in
    # spack.package
    extends("python", when="+python", ignore=r"(bin|lib/(lib.*?|.*?perl.*?))/.*")
    extends("perl", when="+perl", ignore=r"(bin|lib/(lib.*?|.*?python.*?))/.*")

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

    def configure_args(self):
        args = []

        if "+pcre" in self.spec:
            args.append("--with-pcre")

        if "-python" in self.spec:
            args.append("--disable-python")

        if "+perl" in self.spec:
            args.append("--enable-perl")

        return args

    @run_before("install")
    def filter_sbang(self):
        # replace system Python with Spack's in sbang before install so
        # Spack's sbang hook can fix it up if it's too long
        files = [f for f in find("api", "*", recurse=False) if is_exe(f)]
        python = join_path(self.spec["python"].prefix.bin, "python")
        filter_file(r"^#!\s*/usr/bin.*python", r"#!{}".format(python), *files)
