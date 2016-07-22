#!/bin/sh
# python -c `cat $1 | sed 's/\$\([a-zA-Z]\{1,\}\)[ ]\{0,\}=[ ]\{0,\}\(.\{1,\}\)/\1 = subjectivity.Subjective\(\2, "\1"\)/'`

function transpile {
    printf 'import subjectivity\n'
    cat $1 | sed 's/\$\([a-zA-Z]\{1,\}\)[ ]\{0,\}=[ ]\{0,\}\(.\{1,\}\)/\1 = subjectivity.Subjective\(\2, "\1"\)/'
}

transpile $1 | python
