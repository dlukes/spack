"""(De)activate Python and Perl bindings for manatee-open.

Usage: bin/spack python activate_manatee_bindings.py (activate|deactivate)

`activate` creates symlinks for Manatee's Python and Perl modules under the
prefixes of the versions of Python and Perl that were used as dependencies
during installation of Manatee. `deactivate` removes them.

"""
from __future__ import print_function

import sys


def die_usage():
    print(__doc__.strip())
    sys.exit(1)


try:
    import spack
    import llnl
except ImportError:
    die_usage()


def parse_argv(argv=None):
    argv = argv or sys.argv[1:]
    commands = {"activate", "deactivate"}
    if len(argv) != 1 or argv[0] not in commands:
        die_usage()
    return argv[0] == "activate"


def main(activate):
    manatee = spack.cmd.disambiguate_spec("manatee-open")
    deps = manatee.dependencies_dict()
    lib_paths = {
        "python": ("lib", "python2.7"),
        "perl": ("lib", "site_perl"),
    }
    for pack, args in manatee.package.extendees.values():
        lib_path = lib_paths[pack.name]
        manatee_path = spack.join_path(manatee.prefix, *lib_path)
        manatee_tree = llnl.util.link_tree.LinkTree(manatee_path)
        extendee = deps[pack.name].spec.package
        extendee_path = spack.join_path(extendee.prefix, *lib_path)
        msg = "{} {} {} bindings in {}.".format(
            "Activated" if activate else "Deactivated",
            manatee.name, extendee.name, extendee.prefix)
        if activate:
            manatee_tree.merge(extendee_path)
        else:
            manatee_tree.unmerge(extendee_path)
        llnl.util.tty.info(msg)


if __name__ == "__main__":
    activate = parse_argv()
    main(activate)
