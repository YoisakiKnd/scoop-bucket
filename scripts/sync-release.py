#!/usr/bin/env python3
"""Copy the latest stable Teleaf manifest after checking the release checksum."""
import json
import re
import urllib.request
from pathlib import Path

REPOSITORY = 'YoisakiKnd/teleaf'
BASE = f'https://github.com/{REPOSITORY}'


def fetch(url):
    request = urllib.request.Request(url, headers={'User-Agent': 'teleaf-scoop-bucket'})
    with urllib.request.urlopen(request, timeout=60) as response:
        return response.read().decode('utf-8')


def sync():
    release = json.loads(fetch(f'https://api.github.com/repos/{REPOSITORY}/releases/latest'))
    tag = release['tag_name']
    if release['draft'] or release['prerelease'] or not re.fullmatch(r'v\d+\.\d+\.\d+', tag):
        raise ValueError('Expected a stable version release')
    assets = {asset['name']: asset for asset in release['assets']}
    filename = f'teleaf-{tag[1:]}-windows-x86_64.zip'
    package = assets[filename]
    manifest = json.loads(fetch(assets['teleaf.json']['browser_download_url']))
    checksums = fetch(assets['SHA256SUMS']['browser_download_url'])
    match = re.search(r'^([a-f0-9]{64})\s+' + re.escape(filename) + r'$', checksums, re.MULTILINE)
    if not match:
        raise ValueError('Windows package is missing from SHA256SUMS')
    digest = match[1]
    if package.get('digest') and package['digest'] != 'sha256:' + digest:
        raise ValueError('SHA256SUMS differs from the GitHub asset digest')
    architecture = manifest['architecture']['64bit']
    expected_url = f'{BASE}/releases/download/{tag}/{filename}'
    if (manifest['version'] != tag[1:] or manifest['homepage'] != BASE
            or manifest['bin'] != 'teleaf.exe'
            or architecture['url'] != expected_url or architecture['hash'] != digest
            or package['browser_download_url'] != expected_url):
        raise ValueError('Manifest does not match the published Windows package')
    target = Path(__file__).resolve().parents[1] / 'bucket/teleaf.json'
    content = json.dumps(manifest, indent=4) + '\n'
    if target.exists() and target.read_text(encoding='utf-8') == content:
        print(f'Teleaf {tag[1:]} is already current')
        return
    target.parent.mkdir(parents=True, exist_ok=True)
    target.write_text(content, encoding='utf-8')
    print(f'Updated Teleaf to {tag[1:]}')


if __name__ == '__main__':
    sync()
