import qrcode

def gen_qr(text = "https://linklerz.xyz/"):
    qr = qrcode.QRCode(version=1,
    error_correction=qrcode.constants.ERROR_CORRECT_L,
    box_size=10,
    border=2)
    qr.add_data(text)
    qr.make(fit=True)
    img = qr.make_image(fill_color="black", back_color="white")
    img.save("./qr_code/qr.png")

gen_qr("https://linklerz.xyz/")