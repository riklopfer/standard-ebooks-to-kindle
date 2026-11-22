# standard-ebooks-to-kindle
Simple Python CLI util that copies [Standard eBooks](https://standardebooks.org) files to the correct location on a Kindle mounted locally on MacOS.

# Acquire Books
Download Kindle-format files (`.azw3`) and thumbnails (`.jpg`) for the cover art to your computer (e.g. `~/Documents/Standard-eBooks`).

## Bulk
If you are a [patron](https://standardebooks.org/donations/new) you can download bulk zips from [bulk-downloads](https://standardebooks.org/bulk-downloads).

# Connect Kindle
Connect your Kindle to your Mac via USB.

# Install
Installs the CLI entry point with [uv](https://docs.astral.sh/uv/)
```shell
uv tool install https://github.com/riklopfer/standard-ebooks-to-kindle.git
```

# Copy Books
```shell
standard-ebooks-to-kindle ~/Documents/Standard-eBooks
```

```console
Usage: standard-ebooks-to-kindle [OPTIONS] {source} [kindle_root]

╭─ Arguments ─────────────────────────────────────────────────────────────────╮
│ *    source           <path>  Path containing downloaded ebooks [required]  │
│      kindle_root      <path>  Kindle mount point [default: /Volumes/Kindle] │
╰─────────────────────────────────────────────────────────────────────────────╯
╭─ Options ───────────────────────────────────────────────────────────────────╮
│ --force                 --no-force    <bool>  Force directory creation.     │
│                                               Will attempt to create        │
│                                               kindle_root if it doesn't     │
│                                               exist.                        │
│                                               [default: no-force]           │
│ --install-completion                  <bool>  Install completion for the    │
│                                               current shell.                │
│ --show-completion                     <bool>  Show completion for the       │
│                                               current shell, to copy it or  │
│                                               customize the installation.   │
│ --help                                <bool>  Show this message and exit.   │
╰─────────────────────────────────────────────────────────────────────────────╯
```

# Update uv tools
This will update this tool and any others you have installed via uv.
```shell
uv tool update --all
```
