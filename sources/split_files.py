import argparse
import datetime
import logging
import os


def split_file(file_path, num_chunks) -> None:
    """
    Splits a text input file (like a log) into a given number of chunks.
    Example: 1 big file split into 10 small ones.
    Use: python split_file.py path_to_your_log_file.log 10
    :param file_path: Path to the file to be split
    :param num_chunks: Number of chunks to split the file into
    :return: None
    """
    # Set up logging to file and console
    date_format = "%Y-%m-%d_%H:%M:%S"
    log_file = f"split_file_{datetime.datetime.now().strftime(date_format)}.log"
    logging.basicConfig(
        filename=log_file,
        level=logging.INFO,
        format="%(asctime)s - %(message)s",
    )
    console = logging.StreamHandler()
    console.setLevel(logging.INFO)
    formatter = logging.Formatter("%(asctime)s - %(message)s")
    console.setFormatter(formatter)
    root_logger = logging.getLogger()
    root_logger.addHandler(console)

    logging.info(f"Starting to split file: {file_path} into {num_chunks} chunks.")

    file_name, file_extension = os.path.splitext(file_path)

    with open(file_path, "r") as file:
        lines = file.readlines()
        chunk_size = len(lines) // num_chunks
        for i in range(num_chunks):
            start = i * chunk_size
            end = start + chunk_size if i < num_chunks - 1 else None
            output_file_name = f"{file_name}_part_{i + 1}{file_extension}"
            with open(output_file_name, "w") as output_file:
                output_file.writelines(lines[start:end])

            # Log the output file name
            # format to 2 decimal digits
            logging.info(f"Split file created: {output_file_name}: {(os.path.getsize(output_file_name)/1024/1024):.2f} MB")

    logging.info(f"Finished splitting file: {file_path}")
    logging.info(f"Logs available at: {log_file}")


# Parsing command line arguments
parser = argparse.ArgumentParser(description="Split a large log file into smaller chunks.")
parser.add_argument("file_path", type=str, help="Path to the log file to be split.")
parser.add_argument("num_chunks", type=int, help="Number of chunks to split the file into.")

args = parser.parse_args()

if __name__ == "__main__":
    #split_file("/home/user/sessions/session_1.json", 5)
    #split_file("/home/user/logs/log_2024-09-25.log", 7)
    split_file(args.file_path, args.num_chunks)
