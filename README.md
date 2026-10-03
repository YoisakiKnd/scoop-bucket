# Teleaf Scoop bucket

Lightweight Scoop metadata for [Teleaf](https://github.com/YoisakiKnd/teleaf), a Telegram terminal client. Application binaries and source code live in the main project; this repository contains only the manifest, documentation and its update workflow.

## Install

```powershell
scoop bucket add teleaf https://github.com/YoisakiKnd/scoop-teleaf
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
scoop bucket add teleaf https://github.com/YoisakiKnd/scoop-teleaf
scoop update teleaf
```

Removing a bucket does not remove installed applications or Telegram account data.

## Automatic manifest updates

The **Sync Teleaf release** workflow checks the main project's latest stable GitHub Release hourly. It verifies the Windows archive URL and SHA-256 against `SHA256SUMS` and the GitHub asset digest, then commits the published `teleaf.json` if changed. Prereleases are excluded. No personal access token is required: the workflow writes only to this repository with its own `GITHUB_TOKEN`.

GitHub may delay scheduled runs or disable schedules for inactive repositories. Maintainers can enable and manually run the workflow from **Actions → Sync Teleaf release → Run workflow** after a new release.
