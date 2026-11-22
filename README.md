# standard-ebooks-to-kindle
Copy [Standard eBooks](https://standardebooks.org) to Kindle

# Acquire Books

Download Kindle-format files (`.azw3`) and thumbnails (`.jpg`) for the cover art.

## Bulk

Download Kindle-format zip files from [bulk-downloads](https://standardebooks.org/bulk-downloads). You need to be a [patron](https://standardebooks.org/donations/new) to do this.

# Install

```shell
uv tool install https://github.com/riklopfer/standard-ebooks-to-kindle.git
```

# Execute

```shell
# standard-ebooks-to-kindle /path/to/ebooks-download-dir
standard-ebooks-to-kindle ~/Documents/Standard-eBooks
```

# Update

```shell
uv tool update --all
```
