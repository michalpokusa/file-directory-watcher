# 📁🔍 fdw - CLI tool for watching files and directories changes

Command line tool for monitoring changes, additions and removals in files and directories.
It also offers the option to run commands on specified operations.

![Screenshot of fdw program running](images/fdw-running-normal.jpg)


- [Instalation](#instalation)
- [Usage](#usage)
  - [Examples](#examples)
    - [Simple](#simple)
    - [Advanced](#advanced)
  - [Options](#options)
    - [Patterns for files and directories](#patterns-for-files-and-directories)
    - [Configuration options](#configuration-options)
    - [Commands to run on specified operations](#commands-to-run-on-specified-operations)
    - [Other options](#other-options)


## Instalation

No external dependecies required! 🚫🧰

```bash
$ pip3 install file-directory-watcher
```
[![PyPI](https://img.shields.io/pypi/v/file-directory-watcher?color=0073b7&style=for-the-badge)](https://pypi.org/project/file-directory-watcher/)

Tips:
- 💡 It is recommended to install it globally, so you can use it from anywhere.

## Usage

`fdw` is a command-line tool and **does not** provide any importable modules.

```bash
$ fdw pattern [pattern ...] [--exclude pattern ...] [options]
```

### Examples
#### Simple
```bash
$ fdw "**/*.py" --interval 1s --on-file-change "echo Python file changed"
```

Tips:
- 💡 Surround patterns with quotes to prevent shell expansion.
- 💡 You can use short versions of options. e.g. `-i` instead of `--interval`.

#### Advanced
```bash
$ fdw \
"src/**/*.py" \
--exclude "/home/username/project/src/**/__pycache__/**/*" \
--interval 1s \
--background \
--only file_added \
--on-file-add "git add %relative_path" \
--verbosity full \
```

Tips:
- 💡 Instead of exluding a folder with large number of files, try including only the files you are interested in.
  This will improve the performance and reduce CPU usage.

### Options

#### Patterns for files and directories

<table>
    <tr>
        <th>Option</th>
        <th>Value</th>
        <th>Description</th>
    </tr>
    <tr>
        <td>(positional)</td>
        <td rowspan=2><code>pattern</code></td>
        <td>Glob pattern to watch for changes. You can specify one or more patterns.</td>
    </tr>
    <tr>
        <td><code>--exclude</code></td>
        <td>Glob patterns to exclude from watching. You can specify one or more exclusion patterns.</td>
    </tr>
</table>


#### Configuration options

<table>
    <tr>
        <th>Option</th>
        <th>Value</th>
        <th>Description</th>
    </tr>
    <tr>
        <td>
            <code>-i</code>,
            </br>
            <code>--interval</code>
        </td>
        <td rowspan=2>e.g. <code>0.5s</code>, <code>1m</code>, <code>2h30m</code>, <code>1d12h</code></td>
        <td>Interval between running the watcher. Default: <code>1s</code>.</td>
    </tr>
    <tr>
        <td>
            <code>-d</code>,
            </br>
            <code>--delay</code>
        </td>
        <td>Delay between files. Default: <code>0s</code>.</td>
    </tr>
    <tr>
        <td>
            <code>-b</code>,
            </br>
            <code>--background</code>
        </td>
        <td>-</td>
        <td>
            Run commands in the background as non-blocking processes.
            The <code>fdw</code> process itself is stil in foreground.
        </td>
    </tr>
    <tr>
        <td><code>--only</code></td>
        <td rowspan=2>
            <code>file_changed</code>,
            <code>file_added</code>,
            <code>file_modified</code>,
            <code>file_removed</code>,
            <code>directory_changed</code>,
            <code>directory_added</code>,
            <code>directory_modified</code>,
            <code>directory_removed</code>
            <br>
            or short versions
            <br>
            <code>fc</code>,
            <code>fa</code>,
            <code>fm</code>,
            <code>fr</code>,
            <code>dc</code>,
            <code>da</code>,
            <code>dm</code>,
            <code>dr</code>
        </td>
        <td>Operations to watch for. Default: <code>all</code>.</td>
    </tr>
    <tr>
        <td><code>--ignore</code></td>
        <td>Operations to ignore. Default: <code>none</code>.</td>
    </tr>
    <tr>
        <td>
            <code>--fcm</code>,
            </br>
            <code>--file-compare-method</code>
        </td>
        <td>
            <code>mtime</code>,
            <code>size</code>,
            <code>md5</code>,
            <code>mode</code>,
            <code>uid</code>,
            <code>gid</code>
        </td>
        <td>Methods to compare files. Default: <code>mtime</code></td>
    </tr>
    <tr>
        <td>
            <code>--dcm</code>,
            </br>
            <code>--directory-compare-method</code>
        </td>
        <td>
            <code>mtime</code>,
            <code>mode</code>,
            <code>uid</code>,
            <code>gid</code>
        </td>
        <td>Methods to compare directories. Default: <code>mtime</code></td>
    </tr>
    <tr>
        <td>
            <code>-v</code>,
            </br>
            <code>--verbosity</code>
        </td>
        <td>
            <code>limited</code>,
            <code>normal</code>,
            <code>full</code>
        </td>
        <td>Set output verbosity. Default: <code>normal</code>.</td>
    </tr>
    <tr>
        <td>
            <code>--nc</code>,
            </br>
            <code>--no-color</code>
        </td>
        <td>-</td>
        <td>Disable colored output.</td>
    </tr>
</table>

#### Commands to run on specified operations

<table>
    <tr>
        <th>Option</th>
        <th>Value</th>
        <th>Description</th>
    </tr>
    <tr>
        <td>
            <code>--oc</code>,
            </br>
            <code>--on-change</code>
        </td>
        <td rowspan=12><code>command</code></td>
        <td>Commands to run when a file or directory is added, modified, or removed.</td>
    </tr>
    <tr>
        <td>
            <code>--oa</code>,
            </br>
            <code>--on-add</code>
        </td>
        <td>Commands to run when a file or directory is added.</td>
    </tr>
    <tr>
        <td>
            <code>--om</code>,
            </br>
            <code>--on-modify</code>
        </td>
        <td>Commands to run when a file or directory is modified.</td>
    </tr>
    <tr>
        <td>
            <code>--or</code>,
            </br>
            <code>--on-remove</code>
        </td>
        <td>Commands to run when a file or directory is removed.</td>
    </tr>
    <tr>
        <td>
            <code>--ofc</code>,
            </br>
            <code>--on-file-change</code>
        </td>
        <td>Commands to run when a file is added, modified, or removed.</td>
    </tr>
    <tr>
        <td>
            <code>--ofa</code>,
            </br>
            <code>--on-file-add</code>
        </td>
        <td>Commands to run when a file is added.</td>
    </tr>
    <tr>
        <td>
            <code>--ofm</code>,
            </br>
            <code>--on-file-modify</code>
        </td>
        <td>Commands to run when a file is modified.</td>
    </tr>
    <tr>
        <td>
            <code>--ofr</code>,
            </br>
            <code>--on-file-remove</code>
        </td>
        <td>Commands to run when a file is removed.</td>
    </tr>
    <tr>
        <td>
            <code>--odc</code>,
            </br>
            <code>--on-directory-change</code>
        </td>
        <td>Commands to run when a directory is added, modified, or removed.</td>
    </tr>
    <tr>
        <td>
            <code>--oda</code>,
            </br>
            <code>--on-directory-add</code>
        </td>
        <td>Commands to run when a directory is added.</td>
    </tr>
    <tr>
        <td>
            <code>--odm</code>,
            </br>
            <code>--on-directory-modify</code>
        </td>
        <td>Commands to run when a directory is modified.</td>
    </tr>
    <tr>
        <td>
            <code>--odr</code>,
            </br>
            <code>--on-directory-remove</code>
        </td>
        <td>Commands to run when a directory is removed.</td>
    </tr>
</table>

For all commands, you can use the following variable expansions:

<table>
    <tr>
        <th>Variable</th>
        <th>Expanded value</th>
        <th>Description</th>
    </tr>
    <tr>
        <td><code>%name</code></td>
        <td>e.g. <code>README.md</code></td>
        <td>The name of the file or directory.</td>
    </tr>
    <tr>
        <td><code>%relative_path</code></td>
        <td>e.g. <code>../../files/README.md</code></td>
        <td>The relative path of the file or directory.</td>
    </tr>
    <tr>
        <td><code>%absolute_path</code></td>
        <td>e.g. <code>/home/user/files/README.md</code></td>
        <td>The absolute path of the file or directory.</td>
    </tr>
</table>

#### Other options

<table>
    <tr>
        <th>Option</th>
        <th>Value</th>
        <th>Description</th>
    </tr>
    <tr>
        <td><code>--version</code></td>
        <td>-</td>
        <td>Shows program's version number and exit.</td>
    </tr>
    <tr>
        <td><code>-h</code>, <code>--help</code></td>
        <td>-</td>
        <td>Show help message and exit.</td>
    </tr>
</table>
