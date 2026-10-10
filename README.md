# Yoisaki Scoop bucket

Scoop manifests for [Teleaf](https://github.com/YoisakiKnd/teleaf) and [NakuruMusic](https://github.com/YoisakiKnd/NakuruMusic). Application binaries are hosted in each project's GitHub Releases.

## NakuruMusic

NakuruMusic is a YouTube Music terminal client. Its built-in audio player is the default; mpv is optional and can be selected in the app's Settings page.

```powershell
scoop bucket add yoisaki https://github.com/YoisakiKnd/scoop-bucket
scoop install yoisaki/nakuru-music
nakuru-music
```

To use mpv, install it separately and press `,` in NakuruMusic to open Settings:

```powershell
scoop install mpv
```

The `nakuru-music.json` manifest includes Scoop version checking and update metadata. Each published version must use the verified release hash.

## Teleaf

Lightweight Scoop metadata for [Teleaf](https://github.com/YoisakiKnd/teleaf), a Telegram terminal client. Application binaries and source code live in the main project; this repository contains only the manifest, documentation and its update workflow.

## Install

```powershell
scoop bucket add teleaf https://github.com/YoisakiKnd/scoop-bucket
scoop install teleaf/teleaf
teleaf --check
```

## Update

```powershell
scoop update
scoop update teleaf
```

If you previously added the main `YoisakiKnd/teleaf` repository as the `teleaf` bucket, switch its URL without uninstalling the app:

```powershell
scoop bucket rm teleaf
scoop bucket add teleaf https://github.com/YoisakiKnd/scoop-bucket
scoop update teleaf
```

Removing a bucket does not remove installed applications or Telegram account data.

## Automatic manifest updates

The **Sync Teleaf release** workflow checks the main project's latest stable GitHub Release hourly. It verifies the Windows archive URL and SHA-256 against `SHA256SUMS` and the GitHub asset digest, then commits the published `teleaf.json` if changed. Prereleases are excluded. No personal access token is required: the workflow writes only to this repository with its own `GITHUB_TOKEN`.

GitHub may delay scheduled runs or disable schedules for inactive repositories. Maintainers can enable and manually run the workflow from **Actions → Sync Teleaf release → Run workflow** after a new release.

## Release maintenance policy

Every stable Teleaf release must update the main project and this bucket using the verified release manifest. Since 2026-10-04, the publisher's policy no longer requires creating or updating release pull requests in Mythos-404/eimer; existing pull requests remain unchanged unless separately requested. Record release and bucket synchronization results in the main project's release report.

This repository was renamed from `YoisakiKnd/scoop-teleaf` to `YoisakiKnd/scoop-bucket`. The old URL redirects; existing buckets continue to work.

Teleaf and this bucket's update scripts use the MIT license. Bundled third-party libraries retain their own licenses.

## NotionQuill

[NotionQuill](https://github.com/YoisakiKnd/NotionQuill) (轻羽) is a lightweight writing client that keeps article drafts in Notion and writes them back to the same page.

```powershell
scoop bucket add yoisaki https://github.com/YoisakiKnd/scoop-bucket
scoop install yoisaki/notionquill
```

The manifest installs the portable `notionquill.exe` from `notionquill-<version>-windows-x86_64.zip` and adds a Start Menu shortcut. The same release also carries a normal NSIS installer (`NotionQuill_<version>_x64-setup.exe`) for people who prefer that; Scoop does not use it. NotionQuill runs on the Microsoft Edge WebView2 runtime, which ships with Windows 10 and 11 by default.

`checkver` / `autoupdate` read the new version's hash from the release's `SHA256SUMS`, the same way `teleaf.json` and `nakuru-music.json` do. The **Test NotionQuill manifest** workflow installs it on Windows whenever the manifest changes.
