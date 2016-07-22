#!/bin/sh
function transpile {
    printf 'import subjectivity\n'
    cat $1 | sed 's/[ ]\{0,]}\$\([a-zA-Z0-9]\{1,\}\)[ ]\{0,\}=[ ]\{0,\}\(.\{1,\}\)/\1 = subjectivity.Subjective\(\2, "\1"\)/'
}

transpile $1 | python
