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


class Finlib(AutotoolsPackage):
    """Fast indexing library for Manatee corpus query engine."""

    homepage = "https://nlp.fi.muni.cz/trac/noske"

    # older versions are in the archive/ subdirectory; indicate this by adding
    # an archive=True kwarg to the version directive
    version("2.36.5", "53d78ba6641d47ed1f63f80b677e093e")
    version("2.35.2", "3ad8e989a013959d60fca018164edb49", archive=True)

    variant("pcre", default=True, description="Build with PCRE.")

    depends_on("pcre +utf", when="+pcre")

    def url_for_version(self, version):
        dirpath = "http://corpora.fi.muni.cz/noske/src/finlib"
        fpath = "finlib-{}.tar.gz".format(version)
        if self.versions[version].get("archive", False):
            return "/".join([dirpath, "archive", fpath.format(version[1])])
        else:
            return "/".join([dirpath, fpath.format(version[0])])

    def configure_args(self):
        args = []

        if "+pcre" in self.spec:
            args.append("--with-pcre")

        return args
