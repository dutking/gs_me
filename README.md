# GS-ME

## Description

The tool scans provided folder for json files with valid GenomeSpy schema, runs a GenomeSpy web server with all found genomespy spec json files available in select menu so that you can observe multiple files in one session.

## Installation

```sh
uv tool install gs-me
```

## Usage

```sh
gs-me --input /path/to/directory/with/genomespy/json/files
```

## Notes

- The tool saves container with selector in window.customSelect
- The tool saves current spec path in window.currentPath
- The tool saves GenomeSpy API object in window.GSAPI
