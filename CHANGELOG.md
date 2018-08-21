# Changelog

All notable changes to this project will be documented in this file.
The format is based (loosely) on [Keep a Changelog].

[keep a changelog]: http://keepachangelog.com/

## Unreleased
### Fixed
* Previously, if Madeline encountered an error or warning while
  mirroring verbosely, the error or warning message would be
  distastefully interspersed with the verbose status messages. This
  has been fixed, and acts the way you would expect.

## 1.0 (released 2018-08-01)
### Added
* Python package: `madeline`
* Binary: `madeline`
  * Command-line arguments:
    * `--source`
    * `--target`
    * `put | get`
    * `--exclude`
    * `--verbose | --no-verbose`
    * `--identity | --no-identity`
    * `--ssh-add | --no-ssh-add`
  * Environment variable: `MADELINE_DEBUG`
