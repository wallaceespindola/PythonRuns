import qrcode


def generate_qr_code():
    """
    Generate a QR code and save it as an image.
    :return:
    """
    print("####### Create a QR-Code with python #######")

    # qr = _qrcode.QRCode(
    #     version=1,
    #     error_correction=_qrcode.constants.ERROR_CORRECT_L,
    #     box_size=10,
    #     border=4
    # )

    # Data to encode
    data = "http://wtechitsolutions.com/"

    # Creating an instance of QRCode class
    qr = qrcode.QRCode(version=1, box_size=10, border=5)

    # Adding data to the instance 'qr'
    qr.add_data(data)

    qr.make(fit=True)
    img = qr.make_image(fill_color="black", back_color="white")

    # Save the image
    file_path = "../output/MyQRCode.png"
    img.save(file_path)

    print(f"QR code generated and saved to {file_path}")
    img.show()  # This will open the image using the default image viewer


if __name__ == "__main__":
    generate_qr_code()
