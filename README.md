# mondo

> it's got what plants crave

Mondo is a little monitoring/graphing utility.

## Notes on representation

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

## References

* <https://flask.palletsprojects.com/en/stable/tutorial/views/>
* <https://gist.github.com/mbostock/1642989>
