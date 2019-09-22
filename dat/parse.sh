#/bin/bash

gridfont parse original.json original --svg && \
gridfont write original/res.json original/img.svg \
"abcdefghijklmnopqr
stuvwxyz1234567890
*+()/\[]^=-\!.,<>'#|_%?~\"
the quick (brown) fox
jumps over the lazy dog\!"

gridfont parse smooth.json smooth --svg && \
gridfont write smooth/res.json smooth/img.svg \
"abcdefghijklmnopqr
stuvwxyz1234567890
*+()/\[]^=-\!.,<>'#|_%?~\"
the quick (brown) fox
jumps over the lazy dog\!"
