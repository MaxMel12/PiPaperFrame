from waveshare import epd7in5_V2
from PIL import Image
from flask import Flask, request
import io

app = Flask(__name__)

epd = epd7in5_V2.EPD()
epd.init()

@app.route("/test")
def test():
    print("worked")

@app.route("/display",methods=['POST'])
def display_image():
    img_data = request.files['image'].read()
    img_buffer = io.BytesIO(img_data)
    img_buffer.seek(0)
    img = Image.open(img_buffer)
    epd.display(epd.getbuffer(img))
    return {},200

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8000)

