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


def list_gh_release_assets(release):
    """
    Takes a ReleaseTuple object and returns the list of assets returned by the
    Github API from "GET /repos/:owner/:repo/releases/tags/:tag"
    """
    query_url_fmt = urlparse.urljoin(GITHUB_API, '/repos/{owner}/{repo}/releases/tags/{version}')

    release_dict = release._asdict()
    print query_url_fmt.format(**release_dict)
    return requests.get(query_url_fmt.format(**release_dict)).json()['assets']


def select_gh_release_asset(assets, fname):
    """
    Returns the singular asset matching fname from the list of assets
    """
    matched_assets = [asset for asset in assets if fname == asset['name']]
    assert len(matched_assets) == 1

    return matched_assets[0]

def main():
    """
    program main. reads in the url and returns the desired asset for the given
    release.
    """
    url = sys.argv[1]

    release = parse_url(url)

    print select_gh_release_asset(list_gh_release_assets(release), release.filename)

if __name__ == '__main__':
    main()
