#!/bin/bash

# Script to rename all .out files in the current directory to .log

echo "Renaming .out files to .log in: $(pwd)"

shopt -s nullglob  # Prevents error if no .out files are present

for f in *.out; do
  new="${f%.out}.log"
  echo "Renaming '$f' → '$new'"
  mv -- "$f" "$new"
done

echo "Done."
