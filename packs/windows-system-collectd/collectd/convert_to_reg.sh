#!/bin/bash

for i in `ls *.reg`
do
    echo ${i}
    echo -e "Windows Registry Editor Version 5.00\n" > ${i}.tmp
    cat ${i} >> ${i}.tmp
    todos ${i}.tmp
    iconv -f UTF-8 -t UTF-16 ${i}.tmp > ${i}
    rm -f ${i}.tmp
done