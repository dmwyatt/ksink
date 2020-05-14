# ksink

`ksink` is simply a tool for copying directories with a nice progress
bar. It uses rsync in the background so you get the benefits of rsync
such as resumable copies.

Requires `rsync` on the system's `PATH`.

## Usage
```bash
ksink /the_source /the_destination
```
![demo.gif](https://raw.githubusercontent.com/dmwyatt/ksink/master/demo.gif)
