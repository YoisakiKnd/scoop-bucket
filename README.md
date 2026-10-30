# Yoisaki Scoop bucket

Scoop manifests for [Teleaf](https://github.com/YoisakiKnd/teleaf) [NakuruMusic](https://github.com/YoisakiKnd/NakuruMusic), and [congminal](https://github.com/YoisakiKnd/congminal). Application binaries are hosted in each project's GitHub Releases.

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

[NotionQuill](https://github.com/YoisakiKnd/NotionQuill) (轻羽) is a thin shell around Notion's own web app: the window is ours, the page inside is Notion's, so every feature is present because none of them are reimplemented. What is left out is the outer layer — no bundled browser engine, no Node, no updater.

```powershell
scoop bucket add yoisaki https://github.com/YoisakiKnd/scoop-bucket
scoop install yoisaki/notionquill
```

The manifest installs the portable `notionquill.exe` from `notionquill-<version>-windows-x86_64.zip` and adds a Start Menu shortcut. The same release also carries a normal NSIS installer (`NotionQuill_<version>_x64-setup.exe`) for people who prefer that; Scoop does not use it. NotionQuill runs on the Microsoft Edge WebView2 runtime, which ships with Windows 10 and 11 by default.

`checkver` / `autoupdate` read the new version's hash from the release's `SHA256SUMS`, the same way `teleaf.json` and `nakuru-music.json` do. The **Test NotionQuill manifest** workflow installs it on Windows whenever the manifest changes.

## congminal

A native Windows terminal emulator with tabs, split panes, SSH/SFTP, Git, monitoring, and notifications.

```powershell
scoop bucket add yoisaki https://github.com/YoisakiKnd/scoop-bucket
scoop install yoisaki/congminal
congminal --version
```

Windows x86_64, Windows 10 1809+. The manifest extracts the versioned release directory, creates a command shim and Start Menu shortcut, and keeps `congminal-ssh-helper.exe` beside the main executable. No Rust toolchain or extra runtime package is installed. SSH requires a separately available system client; SFTP needs OpenSSH 8.7+ with askpass support. User configuration remains in `%APPDATA%\congminal`, outside Scoop's version directories.

`checkver` follows stable GitHub Releases. `autoupdate` updates both the archive URL and extraction directory and reads the hash from that archive's `.sha256` asset. This is maintainer update metadata, not an hourly synchronization job. The **Test congminal manifest** workflow performs a real Scoop install, checks the main executable and helper, tests the command shim and checksum, and uninstalls it. congminal uses GPL-3.0-only; its third-party font retains SIL OFL 1.1.
