# mondo

> _it's got what plants crave_

Mondo is a lightweight monitoring/graphing utility. It's meant for displaying
"live" system stats in a browser.

## Quickstart

Do `make serve`, and then take a peek at <http://localhost:2505>.

## Development

Take a look at `make help` for the various build targets.

[TODO.md](TODO.md) is where I've been trying to maintain a list of the things I'd like to
get TODONE.

## Notes

Suppose we have `n=8`. That means we want to show `n` units (default: seconds)
worth of data in the window. In order to smoothly transition from left-to-right
as time ticks by, we'll maintain two control points drawn outside the frame
(points 0 and 9 below, respectively):

```text
| | - - - - - - | |
0 1 2 3 4 5 6 7 8 9
```

In this example, time `t=9` (i.e., `now()`, drawn off to the right and then
transitioned into the frame), the window diplays time `[t-n..t-1]`, with time
`t-(n+1)` transitioned out of the frame to the left.

Note that there could be an arbitrary number of points outside of the frame.

## References

* <https://quart.palletsprojects.com/en/latest/index.html>
* <https://gist.github.com/mbostock/1642989>
