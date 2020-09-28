#!/usr/bin/python3
# Partially mirror 'Cygwin' distribution for offline installation
# (C)Copyright 2009-2020, RW Penney <rwpenney@users.sourceforge.net>

#   This program is free software: you can redistribute it and/or modify
#   it under the terms of the GNU General Public License as published by
#   the Free Software Foundation, either version 3 of the License, or
#   (at your option) any later version.
#
#   This program is distributed in the hope that it will be useful,
#   but WITHOUT ANY WARRANTY; without even the implied warranty of
#   MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#   GNU General Public License for more details.
#
#   You should have received a copy of the GNU General Public License
#   along with this program.  If not, see <http://www.gnu.org/licenses/>.

import argparse, os.path, re, sys
import pmcyg, pmcyg.gui


def getDefaultCacheDir():
    """Attempt to find safe location for local cache of Cygwin downloads"""
    re_syspath = re.compile(r'^ ( /usr | [a-z]:\\windows\\system )',
                            re.VERBOSE | re.IGNORECASE)

    topdir = os.getcwd()

    if re_syspath.match(topdir):
        topdir = os.path.expanduser('~')

    return os.path.join(topdir, 'cygwin')


def ProcessPackageFiles(builder, pkgfiles):
    """Subsidiary program entry-point if used as command-line application"""
    try:
        pmcyg.ProcessPackageFiles(builder, pkgfiles)
    except Exception as ex:
        print('Fatal error during mirroring [{0}]'.format(str(ex)),
              file=sys.stderr)
        #import traceback; traceback.print_exc()


def TemplateMain(builder, outfile, pkgfiles, cygwinReplica=False):
    """Subsidiary program entry-point for command-line list generation"""

    builder.TemplateFromLists(outfile, pkgfiles, cygwinReplica)


def GUImain(builder, pkgfiles):
    """Subsidiary program entry-point if used as GUI application"""

    gui = pmcyg.gui.TKgui(builder, pkgfiles=pkgfiles)
    gui.Run()


def main():
    builder = pmcyg.PMbuilder()

    # Process command-line options:
    parser = argparse.ArgumentParser(
                usage='%(prog)s [options] [package_file...]',
                description='pmcyg is a tool for generating'
                            ' customized Cygwin(TM) installers')
    parser.add_argument('--version', action='version',
            version=pmcyg.PMCYG_VERSION)

    bscopts = parser.add_argument_group('Basic options')
    bscopts.add_argument('-a', '--all', action='store_true',
            help='Include all available Cygwin packages'
                 ' (default=%(default)s)')
    bscopts.add_argument('-d', '--directory', type=str,
            default=getDefaultCacheDir(),
            help='Where to build local mirror (default=%(default)s)')
    bscopts.add_argument('-z', '--dry-run', action='store_true', dest='dummy',
            help='Do not actually download packages')
    bscopts.add_argument('-m', '--mirror', type=str,
            default=builder.mirror_url,
            help='URL of Cygwin archive or mirror site'
                 ' (default=%(default)s)')
    bscopts.add_argument('-c', '--nogui', action='store_true',
            help='Do not startup graphical user interface')
    bscopts.add_argument('-g', '--generate-template', type=str,
            dest='pkg_file', default=None,
            help='Generate template package-listing')
    bscopts.add_argument('-R', '--generate-replica', type=str,
            dest='cyg_list', default=None,
            help='Generate copy of existing Cygwin installation')
    bscopts.add_argument('package_files', nargs='*',
            help='Files containins list of Cygwin packages')

    advopts = parser.add_argument_group('Advanced options')
    advopts.add_argument('-A', '--cygwin-arch', type=str,
            default=builder.GetArch(),
            help='Target system architecture (default=%(default)s)')
    advopts.add_argument('-e', '--epochs', type=str,
            default=','.join(builder.GetEpochs()),
            help='Comma-separated list of epochs, e.g. "curr,prev"'
                ' (default=%(default)s)')
    advopts.add_argument('-x', '--exeurl', type=str,
            default=pmcyg.DEFAULT_INSTALLER_URL,
            help='URL of "setup.exe" Cygwin installer (default=%(default)s)')
    advopts.add_argument('-i', '--iniurl', type=str, default=None,
            help='URL of "setup.ini" Cygwin database (default=%(default)s)')
    advopts.add_argument('-B', '--nobase', action='store_true', default=False,
            help='Do not automatically include all base packages'
                ' (default=%(default)s)')
    advopts.add_argument('-r', '--with-autorun', action='store_true',
            help='Create autorun.inf file in build directory'
                ' (default=%(default)s)')
    advopts.add_argument('-s', '--with-sources',
            action='store_true', default=False,
            help='Include source-code for of each package'
                 ' (default=%(default)s)')
    advopts.add_argument('-o', '--remove-outdated', type=str,
            choices=('no', 'yes', 'ask'), default='no',
            help='Remove old versions of packages (default=%(default)s)')
    advopts.add_argument('-I', '--iso-filename', type=str, default=None,
            help='Filename for generating ISO image for burning to CD/DVD'
                ' (default=%(default)s)')

    args = parser.parse_args()

    builder.SetArch(args.cygwin_arch)
    builder.SetTargetDir(args.directory)
    builder.mirror_url = args.mirror
    builder.setup_ini_url = args.iniurl
    builder.setup_exe_url = args.exeurl
    builder.SetEpochs(args.epochs.split(','))
    builder.SetOption('DummyDownload', args.dummy)
    builder.SetOption('AllPackages', args.all)
    builder.SetOption('IncludeBase', not args.nobase)
    builder.SetOption('MakeAutorun', args.with_autorun)
    builder.SetOption('IncludeSources', args.with_sources)
    builder.SetOption('RemoveOutdated', args.remove_outdated)
    builder.SetOption('ISOfilename', args.iso_filename)

    if args.pkg_file:
        TemplateMain(builder, args.pkg_file, args.package_files)
    elif args.cyg_list:
        if not HOST_IS_CYGWIN:
            print('WARNING: pmcyg attempting to create replica of non-Cygwin host', file=sys.stderr)
        TemplateMain(builder, args.cyg_list,
                     args.package_files, cygwinReplica=True)
    elif pmcyg.gui.HASGUI and not args.nogui:
        GUImain(builder, args.package_files)
    else:
        ProcessPackageFiles(builder, args.package_files)


if __name__ == "__main__":
    main()

# vim: set ts=4 sw=4 et:
