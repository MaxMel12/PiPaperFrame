from waveshare import epd7in5_V2
from PIL import Image
from flask import Flask, request
import io

app = Flask(__name__)

@app.route("/test")
def test():
    epd = epd7in5_V2.EPD()
    epd.init()

@app.route("/display",methods=['POST'])
def display_image():
    epd = epd7in5_V2.EPD()
    epd.init()
    img_data = request.files['image'].read()
    img = Image.open(io.BytesIO(img_data).seek(0))
    img_buffer = epd.getbuffer(img)
    epd.display(img_buffer)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8000)

