# Madeline

> a novel approach to directory syncing.

<a href="https://www.instagram.com/theounderstars/">
<img src="/img/madeline.jpg" alt="Madeline cooking" width="250px" />
</a>

<!-- use 'markdown-toc -i README.md' to generate table of contents -->

<!-- toc -->

- [Motivation](#motivation)
- [Tutorial](#tutorial)
- [Installation](#installation)
- [Basic usage](#basic-usage)
- [SSH configuration](#ssh-configuration)
- [Development and debugging](#development-and-debugging)

<!-- tocstop -->

## Motivation

Let's say you have lots of files in your `~/files` directory. So many
files, in fact, that your backups take forever and you are running out
of disk space. So you buy a cheap laptop to use as a server, and put
some of your files on there where there is more disk space and backups
aren't being run on your CPU. However, now you have an organization
problem: when you take things out of `~/files`, you have to decide
where to put them on your server. Plus, you have to remember that
they're there: if you accidentally re-clone a Git repository that you
moved over to the server, then you are going to have to figure out how
to merge the two later. Most likely, you'll just end up moving only a
couple of the biggest things over, rather than all the things you can.
Otherwise, it's a maintenance nightmare.

Madeline solves this problem with a novel approach to directory
syncing which I call *complementary mirroring*. With a traditional
file sync (Dropbox, Resilio Sync, Syncthing), both machines have
exactly the same directory tree. The idea is to sync changes fast
enough that you never end up having two different versions of the same
file on the two machines. But complementary mirroring, each machine
has a *sparse subtree* of the directory contents: each file exists on
one and only one machine; the other machine has a *stub* (a special
symbolic link) to indicate that the file exists on the other machine.

This way, you can maintain a single, hierarchical organizational
structure for your files. Furthermore, the stubs prevent you from
accidentally duplicating content on both machines and later having to
deal with merges. The command-line interface of Madeline is rather
foolproof, so you can easily move files and directories back and forth
with reckless abandon.

## Tutorial

Madeline operates on a *source* and a *target* directory tree. We'll
assume these are just directories named `source` and `target` next to
each other. We'll start out as follows:

    .
    └── source
       ├── emacs
       │  ├── docs
       │  │  ├── patterns.md
       │  │  └── style.md
       │  ├── init.el
       │  ├── templates
       │  │  ├── init-profile-post.el
       │  │  └── init-profile-pre.el
       │  └── versions.el
       ├── git
       │  ├── .gitconfig
       │  └── .gitexclude
       ├── LICENSE.md
       └── README.md

Note that the `target` directory doesn't exist yet. Now, we can tell
Madeline to mirror the `emacs/docs` subdirectory from `source` to
`target`:

    $ madeline ... put source/emacs/docs

    .
    ├── source
    │  ├── emacs
    │  │  ├── docs -> |madeline:dir
    │  │  ├── init.el
    │  │  ├── templates
    │  │  │  ├── init-profile-post.el
    │  │  │  └── init-profile-pre.el
    │  │  └── versions.el
    │  ├── git
    │  │  ├── .gitconfig
    │  │  └── .gitexclude
    │  ├── LICENSE.md
    │  └── README.md
    └── target
       ├── emacs
       │  ├── docs
       │  │  ├── patterns.md
       │  │  └── style.md
       │  ├── init.el -> |madeline:file
       │  ├── templates -> |madeline:dir
       │  └── versions.el -> |madeline:file
       ├── git -> |madeline:dir
       ├── LICENSE.md -> |madeline:file
       └── README.md -> |madeline:file

As you can see, the `emacs/docs` subdirectory has been moved, just
like we asked. But what are all these symbolic links? They are
*stubs*: when you see a symbolic link pointing to `|madeline:file`,
`|madeline:dir`, or `|madeline:link`, it means that there is content
in the other directory tree that hasn't been mirrored over.

If you look at the two directory trees, you'll notice that they can be
unambiguously merged. Any given path will have content in one tree and
a stub in the other tree. Merging the trees by discarding the stubs
and keeping the content will *always* return you to the original
state, before you mirrored anything.

We can mirror multiple paths at once; both files and directories are
supported.

    $ madeline ... put source/LICENSE.md source/emacs/templates

    .
    ├── source
    │  ├── emacs
    │  │  ├── docs -> |madeline:dir
    │  │  ├── init.el
    │  │  ├── templates -> |madeline:dir
    │  │  └── versions.el
    │  ├── git
    │  │  ├── .gitconfig
    │  │  └── .gitexclude
    │  ├── LICENSE.md -> |madeline:file
    │  └── README.md
    └── target
       ├── emacs
       │  ├── docs
       │  │  ├── patterns.md
       │  │  └── style.md
       │  ├── init.el -> |madeline:file
       │  ├── templates
       │  │  ├── init-profile-post.el
       │  │  └── init-profile-pre.el
       │  └── versions.el -> |madeline:file
       ├── git -> |madeline:dir
       ├── LICENSE.md
       └── README.md -> |madeline:file

In fact, all possible mirroring options are perfectly safe: Madeline
figures out exactly what should be moved, and never runs the risk of
accidentally deleting or duplicating data. The complementarity of the
trees will always be maintained, and if you break it by creating or
deleting files on either side, then stubs will automatically be
created or deleted to account for that the next time you mirror the
relevant paths. For example, we can move the rest of the content from
the `emacs` subdirectory over to `target`:

    $ madeline ... put source/emacs

    .
    ├── source
    │  ├── emacs -> |madeline:dir
    │  ├── git
    │  │  ├── .gitconfig
    │  │  └── .gitexclude
    │  ├── LICENSE.md -> |madeline:file
    │  └── README.md
    └── target
       ├── emacs
       │  ├── docs
       │  │  ├── patterns.md
       │  │  └── style.md
       │  ├── init.el
       │  ├── templates
       │  │  ├── init-profile-post.el
       │  │  └── init-profile-pre.el
       │  └── versions.el
       ├── git -> |madeline:dir
       ├── LICENSE.md
       └── README.md -> |madeline:file

Or even move everything:

    $ madeline ... put source

    .
    ├── source -> |madeline:dir
    └── target
       ├── emacs
       │  ├── docs
       │  │  ├── patterns.md
       │  │  └── style.md
       │  ├── init.el
       │  ├── templates
       │  │  ├── init-profile-post.el
       │  │  └── init-profile-pre.el
       │  └── versions.el
       ├── git
       │  ├── .gitconfig
       │  └── .gitexclude
       ├── LICENSE.md
       └── README.md

To move content from `target` to `source`, we just use `get` instead
of `put`:

    $ madeline ... get source/README.md

    .
    ├── source
    │  ├── emacs -> |madeline:dir
    │  ├── git -> |madeline:dir
    │  ├── LICENSE.md -> |madeline:file
    │  └── README.md
    └── target
       ├── emacs
       │  ├── docs
       │  │  ├── patterns.md
       │  │  └── style.md
       │  ├── init.el
       │  ├── templates
       │  │  ├── init-profile-post.el
       │  │  └── init-profile-pre.el
       │  └── versions.el
       ├── git
       │  ├── .gitconfig
       │  └── .gitexclude
       ├── LICENSE.md
       └── README.md -> |madeline:file

Note that we still specified a path into `source`. Actually, we could
have given a path into `target` instead; Madeline doesn't care. The
meaning is the same; you are specifying which subpath to mirror, and
the direction is determined by your choice of `put` or `get`.

Madeline has a few additional features. Firstly, by appending a
trailing slash to your path, you can ask Madeline to only create stubs
on the other side, rather than copying over the contents:

    $ madeline ... get source/emacs/

    .
    ├── source
    │  ├── emacs
    │  │  ├── docs -> |madeline:dir
    │  │  ├── init.el -> |madeline:file
    │  │  ├── templates -> |madeline:dir
    │  │  └── versions.el -> |madeline:file
    │  ├── git -> |madeline:dir
    │  ├── LICENSE.md -> |madeline:file
    │  └── README.md
    └── target
       ├── emacs
       │  ├── docs
       │  │  ├── patterns.md
       │  │  └── style.md
       │  ├── init.el
       │  ├── templates
       │  │  ├── init-profile-post.el
       │  │  └── init-profile-pre.el
       │  └── versions.el
       ├── git
       │  ├── .gitconfig
       │  └── .gitexclude
       ├── LICENSE.md
       └── README.md -> |madeline:file

You can also exclude subpaths of the paths you are mirroring:

    $ madeline ... get source --exclude source/git

    .
    ├── source
    │  ├── emacs
    │  │  ├── docs
    │  │  │  ├── patterns.md
    │  │  │  └── style.md
    │  │  ├── init.el
    │  │  ├── templates
    │  │  │  ├── init-profile-post.el
    │  │  │  └── init-profile-pre.el
    │  │  └── versions.el
    │  ├── git -> |madeline:dir
    │  ├── LICENSE.md
    │  └── README.md
    └── target
       ├── emacs -> |madeline:dir
       ├── git
       │  ├── .gitconfig
       │  └── .gitexclude
       ├── LICENSE.md -> |madeline:file
       └── README.md -> |madeline:file

## Installation

On any platform, you may install Madeline using [Pip]:

    $ pip3 install git+https://github.com/raxod502/madeline.git

You may wish to perform a user-local installation by passing the
`--user` flag.

## Basic usage

In basic usage, Madeline is invoked as follows:

    $ madeline --source <source> --target <target> (put | get) <args>...

The `<source>` and `<target>` are paths to directories. These paths
need not exist, but their parent directories should exist. They may
also be remote paths in the format accepted by `scp` (although if you
provide a protocol, it should be `ssh://` rather than `scp://`). More
configuration may be necessary for this to work correctly; see the
next section.

To transfer content from the source directory to the target directory,
use `put`. To transfer content the other way, use `get`.

The remaining `<args>` are paths. These are resolved to absolute paths
as usual, except that symbolic links are *not* followed. Each path
should be contained in either the source or target directory;
otherwise, an error is issued. Internally, these paths are used to
identify a subpath inside either the source or target directory, so it
doesn't actually matter whether you specify a path within the source
or the target directory.

If a path ends with a trailing slash and is a directory, then only
stubs and not its contents are copied. Otherwise, copying is
recursive. However, you can exclude a path and its children from being
copied by passing `--exclude <path>` as one of the arguments.

To allow specifying path names that look like options, the special
argument `--` is supported.

You may also provide the option `--verbose` to have Madeline display
its mirroring progress. The option `--no-verbose` may be used to
override `--verbose`.

## SSH configuration

Unfortunately, the standard Python SSH library, [Paramiko], has some
shortcomings:

* It does not support the `IdentitiesOnly` option in `~/.ssh/config`
  ([paramiko#1216]).
  If you rely on this option, then Paramiko may connect with the wrong
  SSH key or make too many connection attempts for some servers.
* It does not support the `AddKeysToAgent` option in `~/.ssh/config`
  ([paramiko#778]). If you rely on this option, then Paramiko will not
  correctly cache keys in the agent when you authenticate them.

To work around these problems, Madeline provides additional
command-line arguments:

* If you provide the path to an SSH private key using the `--identity
  <identity-file>` option, then Madeline will force Paramiko to
  connect using that identity. This works around the lack of support
  for `IdentitiesOnly`. The option `--no-identity` (which takes no
  argument) may be used to override `--identity`.
* If you additionally provide the option `--ssh-add`, then Madeline
  will manually add the relevant private key to the agent if it is not
  there already. This works around the lack of support for
  `AddKeysToAgent`. Note that this option has no effect if
  `--identity` is not given, and note also that using `--ssh-add`
  requires access to the `ssh-add(1)` utility. The option
  `--no-ssh-add` may be used to override `--ssh-add`.

## Development and debugging

For local development, you should first clone this repository and then
issue `pip3 install -e <path-to-repo>`, optionally inside a
[virtualenv]. This will install a `madeline(1)` binary which
automatically reflects changes made to the `madeline` Python script in
the source directory.

To receive a stack trace when Madeline invokes `sys.exit`, export the
environment variable `MADELINE_DEBUG` to a non-empty value.

[paramiko]: https://github.com/paramiko/paramiko
[paramiko#778]: https://github.com/paramiko/paramiko/issues/778
[paramiko#1216]: https://github.com/paramiko/paramiko/issues/1216
[pip]: https://pypi.org/project/pip/
[virtualenv]: https://docs.python.org/3/tutorial/venv.html
