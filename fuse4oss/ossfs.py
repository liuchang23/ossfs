# -*- coding:utf-8 -*-

 
from collections import defaultdict
from errno import ENOENT, EACCES
from stat import S_IFDIR, S_IFLNK, S_IFREG
from sys import argv, exit
from time import time
from os import path
from os import mkdir
import os
from fuse import FUSE, FuseOSError, Operations 

if not hasattr(__builtins__, 'bytes'):
    bytes = str


class ReadOnlyFileSystem(Operations):
    'Example memory filesystem. Supports only one level of files.'
 
    def __init__(self, cache_dir='/tmp/fuse'):
        self.files = {}
        self.data = defaultdict(bytes)
        self.fd = 0
        now = time()
        self._cache_dir = cache_dir
        if not path.exists(self._cache_dir):
            mkdir(self._cache_dir)


    def __call__(self, op, path, *args):
        print op, ':', path, '-->', self._cache_dir + path
        self.__real_path = path
        return super(ReadOnlyFileSystem, self).__call__(op, self._cache_dir + path, *args)

    def access(self, path, mode):
        return 0
    chmod = os.chmod
    chown = os.chown

    def getattr(self, path, fh=None):
        if os.path.exists(path):
            st = os.lstat(path)
            return dict((key, getattr(st, key)) for key in ('st_atime', 'st_ctime',
                        'st_gid', 'st_mode', 'st_mtime', 'st_nlink', 'st_size', 'st_uid'))
        else:
            st = dict(st_mode=(S_IFREG | 0755), st_size=1000)
            st['st_ctime'] = st['st_mtime'] = st['st_atime'] = time()
            return st

    getxattr = None

    def link(self, target, source):
        return os.link(source, target)

    listxattr = None
    mkdir = os.mkdir
    mknod = os.mknod

    def open(self, path, flags):
        if not os.path.exists(path):
            # download file from oss, should use a mutex to protect __read_path.
            print 'open path for ', self.__real_path
            self.download_file(self.__real_path, path)

        return os.open(path, flags)

    def readdir(self, path, fh):
        return ['.', '..'] + os.listdir(path)

    def read(self, path, size, offset, fh):
        os.lseek(fh, offset, 0)
        return os.read(fh, size)

    readlink = os.readlink

    def release(self, path, fh):
        return os.close(fh)

    def rename(self, old, new):
        return os.rename(old, self._cache_dir+new)

    rmdir = os.rmdir

    def statfs(self, path):
        stv = os.statvfs(path)
        return dict((key, getattr(stv, key)) for key in ('f_bavail', 'f_bfree',
            'f_blocks', 'f_bsize', 'f_favail', 'f_ffree', 'f_files', 'f_flag',
            'f_frsize', 'f_namemax'))

    def symlink(self, target, source):
        return os.symlink(source, target)

    def truncate(self, path, length, fh=None):
        with open(path, 'r+') as f:
            f.truncate(length)

    unlink = os.unlink
    utimens = os.utime

    def write(self, path, data, offset, fh):
        os.lseek(fh, offset, 0)
        return os.write(fh, data)

    def download_file(self, filename):
        with open(path, 'w') as f:
            f.writelines(["hello", "world"])
            f.flush()


if __name__ == '__main__':
    if len(argv) != 3:
        print('usage: %s <cache-root> <mountpoint>' % argv[0])
        exit(1)
 
    fuse = FUSE(ReadOnlyFileSystem(argv[1]), argv[2], foreground=True)
