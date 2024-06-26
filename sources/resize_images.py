import io
import os

from PIL import Image


def resize_image(input_path, max_size_kb):
    """
    Resize images files to a defined size/quality.

    Run as:
    python resize_images.py /path/to/folder --max_size_kb 100

    """
    img_type = "PNG" if input_path.lower().endswith(".png") else "JPG"

    print(f"####### {img_type}: Image file [{input_path}] #######")

    with Image.open(input_path) as img:
        img_format = img.format
        img_size = os.path.getsize(input_path) / 1024  # Get image size in KB

        if img_size <= max_size_kb:
            return

        print(f">>>>> Processing file [{input_path}] - [{round(img_size, 2)}] Kb #######")

        if img_type == "PNG":
            compress_png(img, img_format, img_size, max_size_kb)
        else:
            compress_jpg(img, img_format, img_size, input_path, max_size_kb)


def compress_png(img, img_format, img_size, max_size_kb):
    if img_size <= max_size_kb:
        return
    buffer = io.BytesIO()
    print(f"----> Reducing PNG - [{round(img_size, 2)}] Kb.")
    img = img.convert("P", palette=Image.WEB, colors=256)
    img.save(buffer, format=img_format, optimize=True, compress_level=9)
    img_size = buffer.tell() / 1024  # Size in KB
    print(f"====> Reduced to size/quality - [{round(img_size, 2)}] Kb.")


def compress_jpg(img, img_format, img_size, input_path, max_size_kb):
    quality = 95
    while img_size > max_size_kb and quality > 10:
        print(f"----> Reducing JPG to - [{round(img_size, 2)}] Kb - quality [{quality}]")
        buffer = io.BytesIO()
        img.save(buffer, format=img_format, quality=quality, optimize=True, compress_level=9)
        img_size = buffer.tell() / 1024  # Size in KB
        print(f"----> Reducing to size/quality - [{round(img_size, 2)}] Kb - quality [{quality}]")
        quality -= 5
    # Save the final image with the reduced quality
    print(f"=====> Final size for file [{input_path}] - [{round(img_size, 2)}] Kb - quality [{quality}]")
    with open(input_path, "wb") as f:
        f.write(buffer.getvalue())


def process_images(folder, max_size_kb=100):
    print(f"========== Resizing images in folder [{folder}] to {max_size_kb} Kb... ==========")
    for root, dirs, files in os.walk(folder):
        for file in files:
            if file.lower().endswith((".jpg", ".jpeg", ".png")):
                file_path = os.path.join(root, file)
                resize_image(file_path, max_size_kb)


if __name__ == "__main__":
    # parser = argparse.ArgumentParser(description="Resize images larger than specified size in KB.")
    # parser.add_argument("folder", type=str, help="Folder to search for images")
    # parser.add_argument(
    #     "--max_size_kb",
    #     type=int,
    #     default=100,
    #     help="Max image size in KB (default: 100KB)",
    # )
    # args = parser.parse_args()
    #
    # process_images(args.folder, args.max_size_kb)
    process_images("/home/aiyrh/Pictures/Webcam/", 100)
