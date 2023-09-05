import qrcode as _qrcode

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
qr = _qrcode.QRCode(version=1, box_size=10, border=5)

# Adding data to the instance 'qr'
qr.add_data(data)

qr.make(fit=True)
img = qr.make_image(fill_color='black', back_color='white')

img.save('../output/MyQRCode.png')
img.open('../output/MyQRCode.png')

# TODO fix bug
