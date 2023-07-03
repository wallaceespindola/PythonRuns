import argparse

# split a text input file (like a log) into a given number of chunks (ex: 1 big file split into 10 small ones)
def split_file(file_path, num_chunks):
    with open(file_path, 'r') as file:
        lines = file.readlines()
        chunk_size = len(lines) // num_chunks
        for i in range(num_chunks):
            start = i * chunk_size
            end = start + chunk_size if i < num_chunks - 1 else None
            with open(f"{file_path}_part_{i + 1}.log", 'w') as output_file:
                output_file.writelines(lines[start:end])

# Parsing command line arguments
parser = argparse.ArgumentParser(description='Split a large log file into smaller chunks.')
parser.add_argument('file_path', type=str, help='Path to the log file to be split.')
parser.add_argument('num_chunks', type=int, help='Number of chunks to split the file into.')

args = parser.parse_args()

# Example usage:
split_file(args.file_path, args.num_chunks)
