def process_line(line):
    numbers = line.split(",")
    remaining_numbers = '|'.join(numbers[1:])
    return f'{numbers[0]},{remaining_numbers}'

input_file = "/home/liu3529/Tigergraph/data/data/sift/sift_query.csv"
output_file = "/home/liu3529/Tigergraph/data/data/sift/sift_query_parse.csv"

with open(input_file, "r") as csv_infile:
    with open(output_file, "w") as csv_outfile:
        for line in csv_infile:
            modified_row = process_line(line.strip())  # strip() removes the newline character at the end
            csv_outfile.write(modified_row + "\n")  # Write the modified row to the output file
