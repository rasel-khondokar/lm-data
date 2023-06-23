#!/bin/bash
books_url=`cat REPORT/books_url`
IFS=$'\n'
read -r -d '' -a lines <<< "$books_url"
source venv/bin/activate
for line in "${lines[@]}"; do
    echo "$line"
    python download_single_book.py --book_url $line
done
deactivate