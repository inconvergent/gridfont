#/bin/bash

set -e

TXT="abcdefghijklmnopqr
stuvwxyz1234567890
*&+\${}()/\[]^=-\!.,<>'#|_:;@%?~\"
the quick (brown) fox?
jumps over the lazy dog.
d6304fd7 #1/2"

gridfont parse original.json original --svg
gridfont write original/res.json original/img.svg "$TXT"

gridfont parse smooth.json smooth --svg
gridfont write smooth/res.json smooth/img.svg "$TXT"

