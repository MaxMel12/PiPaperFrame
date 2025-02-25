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
    img_buffer = io.BytesIO(img_data)
    epd.display(epd.getbuffer(img_buffer))

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8000)

