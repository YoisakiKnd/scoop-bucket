#!/usr/bin/env python3
"""Point the congminal manifest at the latest stable release after checking its checksum."""
import hashlib
import json
import os
import re
import urllib.request
from pathlib import Path

REPOSITORY = 'YoisakiKnd/congminal'
BASE = f'https://github.com/{REPOSITORY}'
LATEST = f'https://api.github.com/repos/{REPOSITORY}/releases/latest'
TARGET = Path(__file__).resolve().parents[1] / 'bucket/congminal.json'


def fetch(url):
    headers = {'User-Agent': 'congminal-scoop-bucket'}
    # Authenticate only the fixed API endpoint, never redirected asset downloads.
    if url == LATEST and os.environ.get('GH_TOKEN'):
        headers['Authorization'] = 'Bearer ' + os.environ['GH_TOKEN']
    with urllib.request.urlopen(urllib.request.Request(url, headers=headers), timeout=60) as response:
        return response.read()


def parse_version(text):
    return tuple(int(part) for part in text.split('.'))


def verified_package(release, fetcher):
    tag = release['tag_name']
    if release['draft'] or release['prerelease'] or not re.fullmatch(r'v\d+\.\d+\.\d+', tag):
        raise ValueError('Expected a stable congminal release')
    version = tag[1:]
    assets = {asset['name']: asset for asset in release['assets']}
    if len(assets) != len(release['assets']):
        raise ValueError('Duplicate release asset names')
    filename = f'congminal-{version}-windows-x86_64.zip'
    for name in (filename, filename + '.sha256'):
        if name not in assets:
            raise ValueError(f'Missing release asset {name}')
        if assets[name]['browser_download_url'] != f'{BASE}/releases/download/{tag}/{name}':
            raise ValueError(f'Unexpected {name} download URL')
    sidecar = fetcher(assets[filename + '.sha256']['browser_download_url'])
    if assets[filename + '.sha256'].get('digest') != 'sha256:' + hashlib.sha256(sidecar).hexdigest():
        raise ValueError('Missing or inconsistent GitHub digest for the .sha256 asset')
    # sha256sum writes ' *' before the name in binary mode, as the Windows build does.
    match = re.fullmatch(r'([a-f0-9]{64}) [ *]' + re.escape(filename) + r'\s*', sidecar.decode('utf-8'))
    if not match:
        raise ValueError('Invalid .sha256 asset')
    if assets[filename].get('digest') != 'sha256:' + match[1]:
        raise ValueError('Missing or inconsistent GitHub digest for the Windows package')
    return version, match[1]


def expand(template, version):
    return template.replace('$version', version)


def update(manifest, version, digest):
    current = manifest['version']
    architecture = manifest['architecture']['64bit']
    autoupdate = manifest['autoupdate']
    # Only the versioned fields are rewritten; the autoupdate templates define their shape.
    if (manifest['homepage'] != BASE or manifest['bin'] != 'congminal.exe'
            or architecture['url'] != expand(autoupdate['architecture']['64bit']['url'], current)
            or manifest['extract_dir'] != expand(autoupdate['extract_dir'], current)
            or manifest['license']['url'] != f'{BASE}/blob/v{current}/LICENSE'):
        raise ValueError('Manifest is not in the expected form')
    if parse_version(version) < parse_version(current):
        raise ValueError(f'Latest release {version} is older than the manifest version {current}')
    if version == current and digest != architecture['hash']:
        raise ValueError(f'Published checksum for {version} differs from the manifest')
    url = expand(autoupdate['architecture']['64bit']['url'], version)
    if url != f'{BASE}/releases/download/v{version}/congminal-{version}-windows-x86_64.zip':
        raise ValueError('Autoupdate URL template does not name the published package')
    manifest['version'] = version
    manifest['license']['url'] = f'{BASE}/blob/v{version}/LICENSE'
    architecture['url'] = url
    architecture['hash'] = digest
    manifest['extract_dir'] = expand(autoupdate['extract_dir'], version)
    return manifest


def sync(fetcher=fetch, target=TARGET):
    version, digest = verified_package(json.loads(fetcher(LATEST)), fetcher)
    text = target.read_text(encoding='utf-8')
    updated = json.dumps(update(json.loads(text), version, digest), indent=4) + '\n'
    if updated == text:
        print(f'congminal {version} is already current')
        return False
    temporary = target.with_suffix('.json.tmp')
    try:
        temporary.write_text(updated, encoding='utf-8')
        temporary.replace(target)
    finally:
        temporary.unlink(missing_ok=True)
    print(f'Updated congminal to {version} (GitHub digest and .sha256 asset agree)')
    return True


if __name__ == '__main__':
    sync()
