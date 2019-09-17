# Gridfont - Grid-based Drawing


**NOTE: this code is incomplete, and it is not very likely to work at the
moment.**

Simple system for describing drawings/symbols on a regular grid. Including a
simple single-line font with a few of the basic ascii characters.

The symbol descriptions look like this:

    S4,9:DS6|S3DtRqS2eLp

The first section (left of `:`) is the `info` section. Which currently contains
the size of the grid. Here the width is 4 and the height is 9. In time this
section might contain other things.

The next section is one or more paths, separated by the pipe symbol `|`.

Specifically, the above example should result in the two paths of the letter
`b`:


    |   <-- p1
    |
    |/-\   <-- p2
    |   |
    |   |
    |\-/


## Paths

When drawing a new path the cursor is always reset to the `origin`, which is in
the upper left corner. The coordinate system is rotated like this:

        -
        |
    - --o-- x+
        |
        y+

From there you can perform relative and absolute moves. Once the command `D` is
entered the path will start being drawn. Which means you can move the cursor
into position before starting each path.


### Relative Moves

The following commands are allowed:

     p   N   t
       \ | /
     L - o - R    <-- o is the current position of the cursor
       / | \
     e   S   q

Any integer after a direction command is interpreted as the length of the step,
otherwise the step size is 1. You can also use two integers separated by a
comma. For instance `q2,3` will move the cursor two steps to the right, and
three steps down. Similarly `p2,3` will move the cursor two steps left, and
three steps up.


### Absolute Moves

The following absolute moves are allowed

  - `Mx,y` to move to position `x,y` relative to the `origin`.
  - `W` to move to move out to the right hand side of the drawing.
  - `w` to move to the left side of the drawing.
  - `H` to move to the top of the drawing.
  - `h` to move to the bottom of the drawing.


## Font

The font (as it were) is included in `out/res.json`. The raw descriptions are
in `dat/font.json`


## Running the Code

In order to parse a `json` file such as `dat/font.json` you can install
the this library.

    python3 setup.py install --user

Then run the following to output the results to the directory `out`

    gridfont dat/font.json out


## Todo

 - groups/pre-defined shapes?
 - finish more common symbols ()[]#@ ...
 - use python Pathlib for paths
 - simple pair kerning instructions?
 - some ligatures?


## References

This is very similar to the Hershey fonts:
https://en.wikipedia.org/wiki/Hershey_fonts which you probably should use, as
they have been around for some time

This method is also similar to drawing in Logo:
https://en.wikipedia.org/wiki/Logo_(programming_language)

The path definitions are also similar to the SVG format (but simpler):
https://en.wikipedia.org/wiki/Scalable_Vector_Graphics

If you find this interesting, you might also like Recursive Radical Packing
Language: https://github.com/LingDong-/rrpl

