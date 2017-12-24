#! /usr/bin/env bash

# This file converts all of the Markdown files to HTML.

OUT_DIR=`readlink -f ../data/html-documents`
cd ../data/api-documents/api
mkdir -p $OUT_DIR
for f in *.md
do
    echo Converting $f
    pandoc -f markdown -t html5 $f > "$OUT_DIR/${f%.*}.html"
done


