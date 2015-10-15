__author__ = 'liuchang'
from fuse4oss.oss.oss_api import OssAPI
from fuse4oss.ossfs import ReadOnlyFileSystem
import os


class OssMixin(object):
    def __init__(self, host, a_id, a_key, bucket = None, server_path = ''):
        self._host = host
        self._a_id = a_id
        self._a_key = a_key
        self._oss_api = OssAPI(self._host, self._a_id, self._a_key)
        assert bucket is not None
        self._bucket  = bucket
        self._server_path = server_path

    def download_file(self, read_path, path):
        if read_path.startswith('/'):
            read_path = read_path[1:]
        print 'download ', read_path, path, os.path.join(self._server_path, read_path)
        res = self._oss_api.get_object_to_file(self._bucket, os.path.join(self._server_path, read_path), path)
        # print res.status, res.getheaders()
        return res.status


class OssFuse(OssMixin, ReadOnlyFileSystem):
    def __init__(self, cache_path, host, a_id, a_key, bucket, server_path):
        ReadOnlyFileSystem.__init__(self, cache_path)
        OssMixin.__init__(self, host, a_id, a_key, bucket, server_path)


if __name__ == "__main__":

    oss = OssMixin('oss-cn-beijing.aliyuncs.com', '0VrTwySLmETO7V71', 'VZeRKdKJSCjGSzwVZUhjEQOwUkQjqi', 'lclclclc', server_path='abc')
    print oss.download_file('1904306.jpg', '/tmp/foo.jpg')
