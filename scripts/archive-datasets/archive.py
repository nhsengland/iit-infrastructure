import copy
import sys

import click
from furl import furl
import requests


def get_package(session, base_url, name):
    url = furl(base_url)
    url.path.segments += ['package_show']
    url = str(url)

    resp = session.get(url, params={'id': name})

    if not resp.ok:
        print(resp.url)
        print('Failed to find: {}'.format(name))
        print(resp.content)
        return None
    return resp.json()['result']


def flatten_extras(package):
    """
    Flatten extras dictionary so the plugin validation works correctly
    """
    extras = package.get('extras')

    if extras is None:
        return package

    del package['extras']
    for extra in extras:
        value = extra['value']
        if value.lower() in ('annual', 'yearly'):
            value = 'Annually'
        package[extra['key']] = value

    return package


def search(session, base_url, name):
    url = furl(base_url)
    url.path.segments += ['package_search']
    url = str(url)

    resp = session.get(url, params={'q': name})

    if not resp.ok:
        print(resp.url)
        print('Failed to find: {}'.format(name))
        print(resp.content)
        return None

    results = resp.json()['result']['results']
    for r in results:
        if r['title'].replace(u'\xa0', u' ') == name:
            return r

    return None


def set_tag(package, tag_name):
    tag = {
        'name': tag_name,
        'vocabulary_id': None,
        'state': 'active',
        'display_name': tag_name,
    }

    package = copy.deepcopy(package)

    if 'tags' not in package.keys():
        package['tags'] = [tag]
        return package

    if any(t['name'] == tag_name for t in package['tags']):
        return package

    package['tags'].append(tag)
    return package


def update(session, base_url, package):
    url = furl(base_url)
    url.path.segments += ['package_update']
    url = str(url)

    resp = session.post(url, params={'id': package['id']}, json=package)
    if resp.status_code == 504:
        print('Timed out')
        sys.exit(1)

    if not resp.ok:
        print(resp.status_code)

    try:
        data = resp.json()
    except ValueError:
        print(resp.content)
        return

    if not data['success']:
        print(data['error'])
        print(package['title'])


def update_package(session, base_url, package, name, tag):
    if package is None:
        click.echo(u'{:10} | {}'.format('not found', name), err=True)
        return

    new_package = set_tag(package, tag)

    if new_package == package:
        # click.echo(u'{:10} | {}'.format('no change', package['title']))
        return

    new_package = flatten_extras(new_package)
    update(session, base_url, new_package)
    # click.echo(u'{:10} | {}'.format('updated', name))


@click.command()
@click.argument('url', nargs=1, envvar='URL')
@click.argument('token', nargs=1, envvar='TOKEN')
@click.argument('datasets', nargs=1, envvar='DATASETS')
@click.argument('tag', nargs=1)
def run(url, token, datasets, tag):
    """
    This script adds the given TAG to each dataset defined in DATASETS
    """
    session = requests.Session()
    session.headers = {'Authorization': token}

    url = furl(url)
    url.path.segments += ['api', 'action']
    url = str(url)

    with open(datasets, 'r') as f:
        datasets = list(d.strip() for d in f.readlines())

    for name in datasets:
        name = name.decode('utf-8', 'ignore')
        package = search(session, url, name)
        update_package(session, url, package, name, tag)

    with open('dataset-ids.txt', 'r') as f:
        ids = list(d.strip() for d in f.readlines())

    for name in ids:
        package = get_package(session, url, name)
        update_package(session, url, package, name, tag)


if __name__ == '__main__':
    try:
        run()
    except KeyboardInterrupt:
        sys.exit(1)
