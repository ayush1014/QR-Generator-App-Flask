from flask import Flask, render_template, request
from PIL import Image
import qrcode
import io
import base64

app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def home():
    img_data_url = None
    filename = None
    if request.method == 'POST':
        link = request.form.get('link')
        filename = request.form.get('filename')
        fill = request.form.get('fill')
        back = request.form.get('back')
        box_size = int(request.form.get('box_size'))
        border = int(request.form.get('border'))
        logo_file = request.files.get('logo')  # Assuming the input field in the form is named 'logo'

        qr = qrcode.QRCode(
            version=1,
            error_correction=qrcode.constants.ERROR_CORRECT_H,
            box_size=box_size,
            border=border,
        )
        qr.add_data(link)
        qr.make(fit=True)
        img = qr.make_image(fill_color=fill, back_color=back)

        if logo_file:
            logo = Image.open(logo_file)
            basewidth = int(img.size[0] * 0.2)  # Resize logo to be 20% of the QR code size
            wpercent = (basewidth / float(logo.size[0]))
            hsize = int((float(logo.size[1]) * float(wpercent)))
            logo = logo.resize((basewidth, hsize), Image.Resampling.LANCZOS)

            # Calculate position to paste the logo (center of the QR code)
            pos = ((img.size[0] - logo.size[0]) // 2, (img.size[1] - logo.size[1]) // 2)
            img.paste(logo, pos)

        # Convert to data URL for displaying in browser
        img_byte_arr = io.BytesIO()
        img.save(img_byte_arr, format='PNG')
        encoded_img_data = base64.b64encode(img_byte_arr.getvalue()).decode('utf-8')
        img_data_url = f"data:image/png;base64,{encoded_img_data}"

        return render_template('index.html', img_data_url=img_data_url, filename=filename)

    return render_template('index.html', img_data_url=None, filename=None)

if __name__ == '__main__':
    app.run(debug=True)
