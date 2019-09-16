# Gridfont - grid-based font for (pen) plotting


Simple system for describing symbols/characters drawn on a regular grid.

The first section describes the width, and the height of the symbol. eg.

    S3,8

for `width=3` and `height=8`.

Paths are seperated by the `|` (`pipe`) symbol.

When drawing a new path the cursor is always reset to the origin (upper left).

use the command `D` to start the path after moving to the desired position.

The following directions are allowed. Any integer after a direction command
is interpretated as the length of the step, otherwise the step size is 1.


    Q   N   E
      \ | /
       \|/
    r --|-- R
       /|\
      / | \
    e   n   q


As an example, the letter `b` can be written like this:


    S3,8|Dn6|n3DERqn2er


Specifically, this should result in two paths:


    |   <-- p1
    |
    |/-\   <-- p2
    |   |
    |   |
    |\-/

## Font

The font (as it were) is (will be, once i finish it) included in
`dat/font-parsed.json`. The raw descriptions are in `dat/font.json`


## TODO

    add Mx,y cmd
    finish a-z
    finish 0-9
    finish common symbols .,;:?/!+-= etc,

## References

This is very similar to the Hershey fonts:
https://en.wikipedia.org/wiki/Hershey_fonts which you probably should use, as
they have been around for some time

This method is also similar to drawing in Logo:
https://en.wikipedia.org/wiki/Logo_(programming_language)

The path definitions are also similar to the SVG format (but simpler):
https://en.wikipedia.org/wiki/Scalable_Vector_Graphics

