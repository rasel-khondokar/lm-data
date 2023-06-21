#!/bin/bash
first_page=`cat REPORT/page_scraped.txt`
last_page=30

for i in $(seq $first_page $last_page); do
    source venv/bin/activate
    python run_bdebooks.py --start_page $i --end_page $i
    deactivate
done