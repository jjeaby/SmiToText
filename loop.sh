#!/bin/bash
for filename in ./*.hwp; do
    #./MyProgram.exe "$filename" "Logs/$(basename "$filename" .txt)_Log$i.txt"
    hwp5txt "./${filename}" > "./${filename}.txt"
done
