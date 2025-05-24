import os
import re

def is_printable_char(char_code):
    """Checks if a character code is printable or common whitespace."""
    # Allow ASCII printable (32-126) and common whitespace (tab, newline, carriage return)
    return (32 <= char_code <= 126) or (char_code in [9, 10, 13])

def sanitize_line(line):
    """Replaces non-printable characters in a line."""
    sanitized_chars = []
    for char in line:
        char_code = ord(char)
        if is_printable_char(char_code):
            sanitized_chars.append(char)
        else:
            sanitized_chars.append('.') # Replace non-printable with a dot
    return "".join(sanitized_chars)

def split_file(input_filepath, output_dir="split_output", lines_per_file=50000):
    """
    Splits a large text file into smaller, sanitized files.
    """
    if not os.path.exists(input_filepath):
        print(f"Error: Input file '{input_filepath}' not found.")
        return

    if not os.path.exists(output_dir):
        os.makedirs(output_dir)
        print(f"Created output directory: {output_dir}")

    file_count = 1
    line_count_current_file = 0
    output_file = None

    try:
        with open(input_filepath, 'r', encoding='utf-8', errors='replace') as infile:
            for line_number, raw_line in enumerate(infile):
                if line_count_current_file == 0: # Start a new output file
                    if output_file:
                        output_file.close()
                    output_filename = os.path.join(output_dir, f"chunk_{file_count:03d}.txt")
                    output_file = open(output_filename, 'w', encoding='utf-8')
                    print(f"Creating {output_filename}...")
                    file_count += 1

                sanitized = sanitize_line(raw_line)
                output_file.write(sanitized) # Write the (potentially modified) line
                
                line_count_current_file += 1
                if line_count_current_file >= lines_per_file:
                    line_count_current_file = 0 # Reset for next file

            if output_file:
                output_file.close()
        print(f"Successfully split and sanitized '{input_filepath}' into {file_count -1} files in '{output_dir}'.")

    except Exception as e:
        print(f"An error occurred: {e}")
        if output_file and not output_file.closed:
            output_file.close()

if __name__ == "__main__":
    input_file = "relevant_db_snippets.txt" # Make sure this file exists
    # Adjust lines_per_file based on how large you want each chunk.
    # 50,000 lines is a starting point. If chunks are still too big, reduce it.
    # If too many small files, increase it.
    split_file(input_file, lines_per_file=500)