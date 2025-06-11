import os

import cv2
from PIL import Image, ImageFile
from rembg import remove

ImageFile.LOAD_TRUNCATED_IMAGES = True


def remove_bg_pil_image(input_path: str, output_path: str):
    print(">> Input and output as a PIL image")
    img = Image.open(input_path)
    output = remove(img)
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    output.save(output_path)
    print(f"✅ Saved to: {output_path}")


def remove_bg_bytes(input_path: str, output_path: str):
    print(">> Input and output as bytes")
    with open(input_path, "rb") as i:
        input_bytes = i.read()
        output_bytes = remove(input_bytes)
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    with open(output_path, "wb") as o:
        o.write(output_bytes)
    print(f"✅ Saved to: {output_path}")


def remove_bg_numpy(input_path: str, output_path: str):
    print(">> Input and output as a numpy array")
    img = cv2.imread(input_path)
    if img is None:
        raise FileNotFoundError(f"Could not read image from {input_path}")
    output = remove(img)
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    cv2.imwrite(output_path, output)
    print(f"✅ Saved to: {output_path}")


if __name__ == "__main__":
    print("####### Test: remove background from image #######")
    file_name = "blue_banner"
    input_path = f"../resources/{file_name}.png"
    output_path = "../output/"
    remove_bg_pil_image(input_path, f"{output_path}{file_name}_1.png")
    print("-----------------------------")
    remove_bg_bytes(input_path, f"{output_path}{file_name}_2.png")
    print("-----------------------------")
    remove_bg_numpy(input_path, f"{output_path}{file_name}_3.png")
    print("-----------------------------")
