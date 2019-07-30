#!/bin/sh

# My collection of packages to install on systems where they're missing
# or obsolete, in order to make working on them tolerable :)
#
# If a package fails to download automatically, download it manually and
# change the URL:
#
# version('8u181-b11', 'ef599e322eee42f6769991dd3e3b1a31', curl_options=curl_options,
#         url='file://%s/jdk-8u172-b11-linux-x64.tar.gz' % os.getcwd())
#
# And possibly comment out url_for_version() to rule out any additional
# attempts at URL manipulation.

scriptdir="$( cd "$( dirname "${BASH_SOURCE[0]}" )" >/dev/null && pwd )"
PATH="$scriptdir/bin:$PATH"

bootstrap="
  gcc@6.4.0
  binutils
"
packages="
  zsh
  tmux
  neovim
  git
  fasd
  the-silver-searcher
  python@3.6.5
  r
  sqlite
  sox
  ffmpeg
"

# if gcc is really old (< 5), we need to install our own
if ! spack compilers | grep -qP 'gcc@([5-9]|\d{2,})\.\d+\.\d+'; then
  >&2 echo 'GCC is too old, installing a newer version before installing packages.'
  spack install $bootstrap
  spack compiler find "$(spack find -p gcc | grep -oP '/.*/opt/spack/.*$')"
  # and that's it, this compiler will be given priority when installing
  # new packages because of the settings in etc/spack/packages.yaml
  view="$bootstrap $packages"
else
  view="$packages"
fi

# if you want environment modules
# https://spack.readthedocs.io/en/latest/getting_started.html#installenvironmentmodules
# uncomment the following line
# spack bootstrap
spack install $packages
spack view --verbose -d no symlink --ignore-conflicts "$HOME/.linuxbrew" $view
