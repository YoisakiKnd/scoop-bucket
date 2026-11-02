#!/usr/bin/env python3
"""Regression checks for congminal manifest synchronization."""
import hashlib
import importlib.util
import json
import tempfile
import unittest
from pathlib import Path

spec = importlib.util.spec_from_file_location('sync_congminal', Path(__file__).with_name('sync-congminal.py'))
sync = importlib.util.module_from_spec(spec)
spec.loader.exec_module(sync)

DIGEST = 'a' * 64


def current():
    manifest = json.loads(sync.TARGET.read_text(encoding='utf-8'))
    return manifest['version'], manifest['architecture']['64bit']['hash']


def fixture(version='9.8.7', digest=DIGEST, separator='  '):
    tag = 'v' + version
    name = f'congminal-{version}-windows-x86_64.zip'
    sidecar = f'{digest}{separator}{name}\n'.encode()
    url = f'{sync.BASE}/releases/download/{tag}/'
    release = {'tag_name': tag, 'draft': False, 'prerelease': False, 'assets': [
        {'name': name, 'browser_download_url': url + name, 'digest': 'sha256:' + digest},
        {'name': name + '.sha256', 'browser_download_url': url + name + '.sha256',
         'digest': 'sha256:' + hashlib.sha256(sidecar).hexdigest()},
    ]}
    return release, {url + name + '.sha256': sidecar}


def fetcher(release, data):
    data = dict(data)
    data[sync.LATEST] = json.dumps(release).encode()
    return data.__getitem__


class SyncTests(unittest.TestCase):
    def run_sync(self, release, data, manifest=None):
        with tempfile.TemporaryDirectory() as folder:
            target = Path(folder) / 'congminal.json'
            target.write_text(manifest or sync.TARGET.read_text(encoding='utf-8'), encoding='utf-8')
            before = target.read_text(encoding='utf-8')
            try:
                changed = sync.sync(fetcher(release, data), target)
            except ValueError:
                self.assertEqual(target.read_text(encoding='utf-8'), before)
                raise
            return changed, json.loads(before), json.loads(target.read_text(encoding='utf-8'))

    def test_newer_release_updates_only_versioned_fields(self):
        changed, before, after = self.run_sync(*fixture())
        self.assertTrue(changed)
        self.assertEqual(after['version'], '9.8.7')
        self.assertEqual(after['architecture']['64bit'], {
            'url': f'{sync.BASE}/releases/download/v9.8.7/congminal-9.8.7-windows-x86_64.zip',
            'hash': DIGEST,
        })
        self.assertEqual(after['extract_dir'], 'congminal-9.8.7-windows-x86_64')
        self.assertEqual(after['license']['url'], f'{sync.BASE}/blob/v9.8.7/LICENSE')
        for key in ('version', 'architecture', 'extract_dir', 'license'):
            del before[key], after[key]
        self.assertEqual(before, after)

    def test_binary_mode_checksum_line_is_accepted(self):
        changed, _, after = self.run_sync(*fixture(separator=' *'))
        self.assertTrue(changed)
        self.assertIn(DIGEST, str(after))

    def test_current_release_is_unchanged(self):
        changed, before, after = self.run_sync(*fixture(*current()))
        self.assertFalse(changed)
        self.assertEqual(before, after)

    def test_rejected_releases_keep_the_previous_manifest(self):
        cases = []
        release, data = fixture()
        release['draft'] = True
        cases.append((release, data))
        release, data = fixture()
        release['assets'][0]['digest'] = 'sha256:' + 'b' * 64
        cases.append((release, data))
        release, data = fixture()
        del release['assets'][0]['digest']
        cases.append((release, data))
        release, data = fixture()
        release['assets'][0]['browser_download_url'] += '?x'
        cases.append((release, data))
        release, data = fixture()
        release['assets'].pop()
        cases.append((release, data))
        cases.append(fixture('0.0.1'))
        cases.append(fixture(current()[0], 'c' * 64))
        for release, data in cases:
            with self.subTest(release=release['tag_name']), self.assertRaises(ValueError):
                self.run_sync(release, data)

    def test_tampered_sidecar_is_rejected(self):
        release, data = fixture()
        key = next(iter(data))
        data[key] = data[key].replace(b'a', b'b', 1)
        with self.assertRaises(ValueError):
            self.run_sync(release, data)

    def test_unexpected_manifest_layout_is_rejected(self):
        manifest = json.loads(sync.TARGET.read_text(encoding='utf-8'))
        manifest['extract_dir'] = 'congminal'
        with self.assertRaises(ValueError):
            self.run_sync(*fixture(), manifest=json.dumps(manifest, indent=4) + '\n')


if __name__ == '__main__':
    unittest.main()
