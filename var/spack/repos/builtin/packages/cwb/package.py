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
from spack import architecture


class Cwb(Package):
    """The IMS Open Corpus Workbench (CWB) is a collection of open-source tools
    for managing and querying large text corpora (ranging from 10 million to 2
    billion words) with linguistic annotations. Its central component is the
    flexible and efficient query processor CQP.

    """
    homepage = "http://cwb.sourceforge.net/"
    url      = "http://svn.code.sf.net/p/cwb/code/cwb/trunk"

    version("daily", svn=url)

    depends_on("binutils", type="build")
    depends_on("bison", type="build")
    depends_on("flex", type="build")
    depends_on("pkg-config", type="build")
    depends_on("ncurses")
    depends_on("pcre")
    depends_on("glib")
    depends_on("readline")
    depends_on("perl", type="build")

    def install(self, spec, prefix):
        p = architecture.platform()
        platform = "PLATFORM=" + p.name
        if p.name in {"linux", "darwin"} and p.back_end.endswith("64"):
            platform = platform + "-64"
        prefix = "PREFIX=" + prefix
        # when overriding flags, we need to account for settings made in the
        # CWB distribution under config/
        cppflags = []
        ldflags = ["-lm"]
        for dep in ["ncurses", "pcre", "glib", "readline"]:
            cppflags.append("-I{}/include".format(spec[dep].prefix))
            ldflags.append("-L{0}/lib -Wl,-rpath,{0}/lib".format(spec[dep].prefix))
        cppflags = "CPPFLAGS=" + " ".join(cppflags)
        ldflags = "LDFLAGS=" + " ".join(ldflags)
        make("clean", platform, prefix, cppflags, ldflags)
        make("depend", platform, prefix, cppflags, ldflags)
        make("all", platform, prefix, cppflags, ldflags)
        make("install", platform, prefix, cppflags, ldflags)
