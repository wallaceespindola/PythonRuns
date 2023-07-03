import argparse
import logging

# split a text input file (like a log) into a given number of chunks.
# Example: 1 big file split into 10 small ones.
# Use: python split_script.py path_to_your_log_file.log 10
def split_file(file_path, num_chunks):
    # Set up logging to file and console
    logging.basicConfig(filename='split_file_log.log', level=logging.INFO, format='%(asctime)s - %(message)s')
    console = logging.StreamHandler()
    console.setLevel(logging.INFO)
    formatter = logging.Formatter('%(asctime)s - %(message)s')
    console.setFormatter(formatter)
    logging.getLogger('').addHandler(console)

    logging.info(f'Starting to split file: {file_path} into {num_chunks} chunks.')

    with open(file_path, 'r') as file:
        lines = file.readlines()
        chunk_size = len(lines) // num_chunks
        for i in range(num_chunks):
            start = i * chunk_size
            end = start + chunk_size if i < num_chunks - 1 else None
            output_file_name = f"{file_path}_part_{i + 1}.log"
            with open(output_file_name, 'w') as output_file:
                output_file.writelines(lines[start:end])

            # Log the output file name
            logging.info(f'Split file created: {output_file_name}')

    logging.info(f'Finished splitting file: {file_path}')

# Parsing command line arguments
parser = argparse.ArgumentParser(description='Split a large log file into smaller chunks.')
parser.add_argument('file_path', type=str, help='Path to the log file to be split.')
parser.add_argument('num_chunks', type=int, help='Number of chunks to split the file into.')

args = parser.parse_args()

# Call the split_file function
split_file(args.file_path, args.num_chunks)
