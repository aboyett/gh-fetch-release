#!/usr/bin/env python

# gh-fetch-requests takes a github releaes asset url and performs the proper API
# calls to actually download the file

import os
import sys
import urlparse

from collections import namedtuple

import requests

GITHUB_API = "https://api.github.com"

ReleaseTuple = namedtuple("ReleaseTuple", ["owner", "repo", "version", "filename"])

def parse_url(url):
    """
    Parses url, validates it is a github release asset url and returns a ReleaseTuple
    """

    parsed_url = urlparse.urlparse(url)

    assert parsed_url.netloc == "github.com"

    path = parsed_url.path.split('/')

    assert (path[0], path[3], path[4]) == ('', 'releases', 'download')

    return ReleaseTuple(path[1], path[2], path[5], path[6])

def main():
    """
    program main. reads in the url and parses it
    """
    url = sys.argv[1]

    print parse_url(url)

if __name__ == '__main__':
    main()
