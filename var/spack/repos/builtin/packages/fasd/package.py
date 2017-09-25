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
#
# This is a template package file for Spack.  We've put "FIXME"
# next to all the things you'll want to change. Once you've handled
# them, you can save this file and test your package like this:
#
#     spack install fasd
#
# You can edit this file again by typing:
#
#     spack edit fasd
#
# See the Spack documentation for more information on packaging.
# If you submit this package back to Spack as a pull request,
# please first remove this boilerplate and all FIXME comments.
#
from spack import *


class Fasd(MakefilePackage):
    """Fasd (pronounced similar to "fast") is a command-line productivity
    booster. Fasd offers quick access to files and directories for POSIX
    shells. It is inspired by tools like autojump, z and v. Fasd keeps track of
    files and directories you have accessed, so that you can quickly reference
    them in the command line.

    The name fasd comes from the default suggested aliases f(files),
    a(files/directories), s(show/search/select), d(directories).

    Fasd ranks files and directories by "frecency," that is, by both
    "frequency" and "recency." The term "frecency" was first coined by Mozilla
    and used in Firefox.)

    """
    # FIXME: Add a proper url for your package's homepage here.
    homepage = "https://github.com/clvv/fasd"
    url      = "https://github.com/clvv/fasd/archive/1.0.1.tar.gz"

    version('1.0.1', 'cab27fecedefbbec667b621985ce786b')

    # FIXME: Add dependencies if required.
    # depends_on('foo')

    # def edit(self, spec, prefix):
        # FIXME: Edit the Makefile if necessary
        # FIXME: If not needed delete this function
        # makefile = FileFilter('Makefile')
        # makefile.filter('CC = .*', 'CC = cc')

    def setup_environment(self, spack_env, run_env):
        spack_env.set("PREFIX", self.prefix)
