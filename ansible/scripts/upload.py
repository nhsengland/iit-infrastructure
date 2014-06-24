#!/usr/bin/env python
"""
A very simple Python script that takes a target tgz file as an argument
(the target file should contain the backups of the databases and filestore)
and pushes it to the S3 bucket as an object with the hostname as its key.
"""
import sys
import os
import boto
import ConfigParser
from boto.s3.key import Key
from socket import gethostname


HOSTNAME = gethostname()


def pushy_galore(bucket, key_name, filename):
    """
    Given a bucket nane, key_name and filename will upload the referenced file
    to the given bucket against the provided key_name.
    """
    connection = boto.connect_s3()
    bucket = connection.get_bucket(bucket)
    key = Key(bucket)
    key.key = key_name
    # TODO: CHECK THIS TO SET ACLs on new key
    key.set_acl('authenticated-read')
    key.set_contents_from_filename(filename)


if __name__ == '__main__':
    """
    Lots of checks that allow the script to be informative if/when things go
    wrong.
    """
    config = ConfigParser.ConfigParser()
    config.read('.s3.ini')
    try:
        BUCKET = config.get('Credentials', 'bucket')
    except Exception, ex:
        sys.stderr.write('S3 Bucket not set')
        sys.exit(1)
    if len(sys.argv) < 2:
        sys.stderr.write('Supply a filename')
        sys.exit(1)
    else:
        filename = sys.argv[1]
        if os.path.exists(filename):
            try:
                pushy_galore(BUCKET, HOSTNAME, filename)
            except Exception, ex:
                sys.stderr.write(str(ex))
                sys.exit(1)
        else:
            sys.stderr.write('No such file for upload')
            sys.stderr.write(filename)
            sys.exit(1)
