import qrcode
from PIL import Image, ImageDraw


def generate_qr_with_hole(data: str, hole_size_ratio=0.25, qr_size=400, save_path="../output/qr_with_hole.png") -> None:
    """
    Generate a QR code with a transparent hole in the center for adding a logo.
    :param data: url or text to encode in the QR code
    :param hole_size_ratio: the size of the hole as a ratio of the QR code size
    :param qr_size: the size of the QR code in pixels
    :param save_path: path to save the generated QR code image
    :return: None
    """
    # Generate QR code
    qr = qrcode.QRCode(
        error_correction=qrcode.constants.ERROR_CORRECT_H  # High error correction to tolerate logo overlay
    )
    qr.add_data(data)
    qr.make(fit=True)
    img_qr = qr.make_image(fill_color="black", back_color="white").convert("RGB")

    # Resize QR to desired size
    img_qr = img_qr.resize((qr_size, qr_size), Image.LANCZOS)

    # Create a mask with a transparent hole in the center
    mask = Image.new("L", (qr_size, qr_size), 255)  # Fully opaque
    draw = ImageDraw.Draw(mask)

    hole_size = int(qr_size * hole_size_ratio)
    top_left = ((qr_size - hole_size) // 2, (qr_size - hole_size) // 2)
    bottom_right = (top_left[0] + hole_size, top_left[1] + hole_size)

    draw.rectangle([top_left, bottom_right], fill=0)  # Transparent hole

    # Apply the mask to make the center transparent
    img_with_hole = img_qr.copy()
    img_with_hole.putalpha(mask)

    # Save the result
    img_with_hole.save(save_path)
    print(f"QR code generated and saved to {save_path}")

    img_with_hole.show()  # This will open the image using the default image viewer


# Example usage
# generate_qr_with_hole("https://example.com", hole_size_ratio=0.25)

if __name__ == "__main__":
    generate_qr_with_hole("https://www.skipy.online/", hole_size_ratio=0.25)
