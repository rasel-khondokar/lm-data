#!/bin/bash
start_line=10001  # Starting line number
end_line=12000   # Ending line number
input_file="REPORT/books_url"  # Name of the input file
output_file="REPORT/books_url_s_{$start_line}_e_{$end_line}.txt"  # Name of the output file
# Extract the desired range of lines using head and tail commands
head -n "$end_line" "$input_file" | tail -n +"$start_line" > "$output_file"
echo "New file created: $output_file"
