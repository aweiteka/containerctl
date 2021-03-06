#!/usr/bin/env python
# Copyright (C) 2014 Brent Baude <bbaude@redhat.com>, Aaron Weitekamp <aweiteka@redhat.com>
#
# This library is free software; you can redistribute it and/or
# modify it under the terms of the GNU Lesser General Public
# License as published by the Free Software Foundation; either
# version 2 of the License, or (at your option) any later version.
#
# This library is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU
# Lesser General Public License for more details.
#
# You should have received a copy of the GNU Lesser General Public
# License along with this library; if not, write to the
# Free Software Foundation, Inc., 59 Temple Place - Suite 330,
# Boston, MA 02111-1307, USA.

import argparse

def main():
    """Entrypoint for script"""

    parser = argparse.ArgumentParser()
    subparsers = parser.add_subparsers(help='sub-command help', dest='action')
    run_parser = subparsers.add_parser('run', help='Run a container from metadata file')
    run_parser.add_argument('json',
                       metavar='MYAPP.JSON',
                       help='JSON file')
    create_parser = subparsers.add_parser('create', help='Generate metadata based on a container')
    create_parser.add_argument('cuid',
                       metavar='CONTAINER_ID',
                       help='Container ID')
    create_parser.add_argument('-o', '--outfile',
                       help='Specify metadata output filename. Defaults to container ID.')
    create_parser.add_argument('-d', '--directory',
                       help='Override default directory')
    create_parser.add_argument('-f', '--force',
                       action='store_true',
                       help='Overwrite existing metadata file. Defaults to false.')
    list_parser = subparsers.add_parser('list', help='List template files on host')
    pull_parser = subparsers.add_parser('pull', help='Pull metadata files from a remote source')
    pull_parser.add_argument('url',
                       metavar='http://example.com/my-app.json',
                       help='Full URL of remote metadata file')
    pull_parser.add_argument('-o', '--outfile',
                       help='Specify metadata output filename')
    pull_parser.add_argument('-d', '--directory',
                       help='Override default directory')
    pull_parser.add_argument('-f', '--force',
                       action='store_true',
                       help='Overwrite existing metadata file. Defaults to false.')

    args = parser.parse_args()

    if args.action in "run":
        import docker_wrapper
        kwargs = {'command': args.action, 'jsonfile': args.json}
        run = docker_wrapper.Run(**kwargs)
        run.start_container()

    elif args.action in "create":
        import metadata
        kwargs = {'cuid': args.cuid,
                  'outfile': args.outfile,
                  'directory': args.directory,
                  'force': args.force}
        create = metadata.Create(**kwargs)
        create.write_files()
    elif args.action in "list":
        import metadata
        filelist = metadata.List()
        filelist.metadata_files()
    elif args.action in "pull":
        import metadata
        kwargs = {'outfile': args.outfile,
                  'directory': args.directory,
                  'force': args.force}
        fetch = metadata.Pull(**kwargs)
        fetch.pull_url(args.url)

if __name__ == '__main__':
    main()

