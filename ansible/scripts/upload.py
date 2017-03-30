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


def pushy_galore(bucket, key_name, filename):
    """
    Given a bucket nane, key_name and filename will upload the referenced file
    to the given bucket against the provided key_name.
    """
    connection = boto.connect_s3()
    bucket = connection.get_bucket(bucket)
    key = Key(bucket)
    key.key = key_name
    key.set_contents_from_filename(filename)


def upload(filename):
    config = ConfigParser.ConfigParser()
    config.read('.s3.ini')
    bucket = config.get('Credentials', 'bucket')
    hostname = gethostname()
    if os.path.exists(filename):
        pushy_galore(bucket, hostname, filename)
        print "Uploaded backups to S3: %s %s" % (bucket, hostname)
    else:
        raise "No such file for upload'"


if __name__ == '__main__':
    """
    Lots of checks that allow the script to be informative if/when things go
    wrong.
    """
    if len(sys.argv) < 2:
        sys.stderr.write('Supply a filename')
        sys.exit(1)

    filename = sys.argv[1]
    upload(filename)
