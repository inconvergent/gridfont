# Gridfont - grid-based font for (pen) plotting


Simple system for describing drawings/symbols on a regular grid. Including a
simple single-line font with a few of the basic ascii characters.

The symbol descriptions look like this:

    S4,9:Dn6|n3DERqn2er

The first section (left of `:`) is the `info` section. Which currently contains
the size of the grid. Here the width is 4 and the height is 9.

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


### Relative motions

The following commands are allowed:

     Q   N   E
       \ | /
     r - o - R    <-- o is the current position of the cursor
       / | \
     e   n   q

Any integer after a direction command is interpreted as the length of the step,
otherwise the step size is 1.


### Absolute moves

The following absolute moves are allowed

  - `Mx,y` to move to position `x,y` relative to the `origin`.
  - W to move to move out to the right hand side of the drawing.
  - w to move to the left.
  - H to move to the top of the drawing.
  - h to move to the bottom of the drawing.


*(The following is incomplete. For this to work the spec requires grouping
commands to avoid accumulating the path for individual commands.)*

As an example, you can use `hW` to move to the lower right hand corner from any
position.


## Font

The font (as it were) is (will be, once I finish it) included in
`dat/font-parsed.json`. The raw descriptions are in `dat/font.json`


## TODO

    groups/pre-defined shapes?
    group individual moves (to allow complex moves)
    draw paths as svg (for debug etc.)
    add W/w/H/h commands
    finish a-z characters
    finish 0-9 characters
    finish some common symbols .,;:?/!+-= etc,

    simple pair kerning instructions?
    some ligatures?


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

