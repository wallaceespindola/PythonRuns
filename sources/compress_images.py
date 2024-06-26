import os
import subprocess

from resize_images import resize_image


def compress_jpeg(input_path, max_size_kb):
    """
    Compress images files to a defined size/quality.

    Run as:
    python compress_images.py /path/to/folder --max_size_kb 100

    """

    print(f"####### JPG: Image file [{input_path}] #######")

    img_size = os.path.getsize(input_path) / 1024  # Get image size in KB

    if img_size <= max_size_kb:
        return

    output_path = input_path + ".tmp.jpg"

    # Compress using mozjpeg
    subprocess.run(["cjpeg", "-quality", "85", "-outfile", output_path, input_path])

    # Check the size of the new file
    new_size = os.path.getsize(output_path) / 1024  # Size in KB

    # If the new file is smaller, replace the original file
    if new_size <= max_size_kb:
        print(f"----> Final size for file [{input_path}] - [{round(new_size,2)}] Kb.")
        os.replace(output_path, input_path)
    else:
        os.remove(output_path)
        # Reduce quality step by step
        quality = 80
        while new_size > max_size_kb and quality > 10:
            subprocess.run(["cjpeg", "-quality", str(quality), "-outfile", output_path, input_path])
            new_size = os.path.getsize(output_path) / 1024  # Size in KB
            quality -= 5

        if new_size <= max_size_kb:
            print(f"----> Final size for file [{input_path}] - [{round(new_size,2)}] Kb - quality [{quality}].")
            os.replace(output_path, input_path)
        else:
            os.remove(output_path)


def compress_png(input_path, max_size_kb):
    # Currently no advanced PNG compression here, but could use pngquant or optipng in a similar way to mozjpeg
    resize_image(input_path, max_size_kb)


def process_images(folder, max_size_kb=100):
    print(f"========== Resizing images... ==========")
    for root, dirs, files in os.walk(folder):
        for file in files:
            file_path = os.path.join(root, file)
            if file.lower().endswith((".jpg", ".jpeg")):
                compress_jpeg(file_path, max_size_kb)
            elif file.lower().endswith(".png"):
                compress_png(file_path, max_size_kb)


if __name__ == "__main__":
    # parser = argparse.ArgumentParser(
    #     description="Compress images to meet the specified size in KB without losing quality.")
    # parser.add_argument("folder", type=str, help="Folder to search for images")
    # parser.add_argument("--max_size_kb", type=int, default=100,
    #                     help="Maximum image size in KB (default: 100KB)")
    # args = parser.parse_args()
    #
    # process_images(args.folder, args.max_size_kb)
    process_images("/home/aiyrh/Pictures/Webcam/", 75)
