import argparse
import io
import os

from PIL import Image


def resize_image(input_path, max_size_kb):
    """
    Resize images files to a defined size

    Run as:
    python resize_images.py /path/to/folder --max_size_kb 100

    """

    print(f"####### Resizing images in path [{input_path}] to [{max_size_kb}] Kb #######")

    with Image.open(input_path) as img:
        img_format = img.format
        img_size = os.path.getsize(input_path) / 1024  # Get image size in KB

        if img_size <= max_size_kb:
            return

        print(f">>>>> Processing file [{input_path}] - [{img_size}] Kb #######")

        # Reduce quality step by step to meet the size requirement
        quality = 95
        while img_size > max_size_kb and quality > 10:
            buffer = io.BytesIO()
            img.save(buffer, format=img_format, quality=quality)
            img_size = buffer.tell() / 1024  # Size in KB
            quality -= 5

        if img_size > max_size_kb:
            img.thumbnail((img.width // 2, img.height // 2))
            img.save(input_path, format=img_format, quality=quality)
        else:
            print(f">>>>> Final size for file [{input_path}] - [{img_size}] Kb #######")
            # with open(input_path, 'wb') as f:
            #     f.write(buffer.getvalue())


def process_images(folder, max_size_kb=100):
    for root, dirs, files in os.walk(folder):
        for file in files:
            if file.lower().endswith((".jpg", ".jpeg", ".png")):
                file_path = os.path.join(root, file)
                resize_image(file_path, max_size_kb)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Resize images larger than specified size in KB.")
    parser.add_argument("folder", type=str, help="Folder to search for images")
    parser.add_argument(
        "--max_size_kb",
        type=int,
        default=100,
        help="Max image size in KB (default: 100KB)",
    )
    args = parser.parse_args()

    process_images(args.folder, args.max_size_kb)
