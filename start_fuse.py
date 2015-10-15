import logging
import fuse
from fuse import FUSE
from fuse4oss import OssFuse
from sys import argv

import argparse


__author__ = 'liuchang'



if __name__ == '__main__':

    # fuse = FUSE(OssFuse(argv[1], 'oss-cn-beijing.aliyuncs.com', '0VrTwySLmETO7V71', 'VZeRKdKJSCjGSzwVZUhjEQOwUkQjqi', 'lclclclc', server_path='abc'), argv[2], foreground=True)

    parser = argparse.ArgumentParser(epilog='liuchang@genedock.com')

    parser.add_argument('-c', '--cache', help='a directory used for cache files (default: /tmp/ossfs)', default='/tmp/ossfs')
    parser.add_argument('-m', '--mount', help='a directory which mounts the oss file system', required=True)
    parser.add_argument('-u', '--host', help='Oss host(default:oss-cn-beijing.aliyuncs.com', default='oss-cn-beijing.aliyuncs.com')
    parser.add_argument('-i', '--accessid', help='OSS Access ID', required=True)
    parser.add_argument('-k', '--accesskey', help='OSS Access Key', required=True)
    parser.add_argument('-b', '--bucket', help='OSS bucket', required=True)
    parser.add_argument('-s', '--serverpath', help='OSS server path(default: None)', default='')
    parser.add_argument('-f', '--foreground', help='enable foreground mode(default: False', default=False, action='store_true')

    args = parser.parse_args()

    fuse = FUSE(OssFuse(args.cache, args.host, args.accessid, args.accesskey, args.bucket, args.serverpath), args.mount, foreground=args.foreground)

