from waveshare import epd7in5_V2
from PIL import Image, ImageDraw, ImageFont
from flask import Flask, request
import io
import utils

app = Flask(__name__)

epd = epd7in5_V2.EPD()
epd.init()

@app.route("/test")
def test():
    print("worked")

@app.route("/display",methods=['POST'])
def display_image():
    epd.init()
    img_data = request.files['image'].read()
    img_buffer = io.BytesIO(img_data)
    img_buffer.seek(0)
    img = Image.open(img_buffer)
    epd.display(epd.getbuffer(img))
    epd.sleep()
    return {},200

#All rendered frames need to be stored in a 2d binary array
#All apps have to render frames
#Centralized handling of apps
    #Need to run one app at a time only
    #Each app needs kill method
    #Jobs are pushed to queue (probably just size 1 tbh)
    #When current job is killed, pop queued app. Queue can be updated any time while app is being killed
#One interface to handle drawing frames
    #Updates should do a partial update on the pixels that differ from the previous frame
    #Queue frames if needed
    #Only job is to receive rendered frames and draw them
    #Full refresh of screen when necessary
#Lib with helpful functions
    #Turning images into the proper format

#Opens the safezone config screen on the device
#Blank screen with safezone drawn on
@app.route("/set_safezone",methods=['POST'])
def display_set_safezone():
    return {},501

#Update safezone by either increasing/decreasing width of the box
#Safezone 
@app.route("/adjust_safezone",methods=['POST'])
def adjust_safezone():
    return {},501

#If in the safezone screen, save the current one and go back to whatever was displayed before
@app.route("/save_safezone",methods=['POST'])
def save_safezone():
    return {}, 501

@app.route("/write_text",methods=['GET'])
def write_text():
    font=ImageFont.truetype("arial.ttf",40)
    text = request.args.get('text')
    text_im = Image.new("1",(800,480),0)
    draw = ImageDraw.Draw(text_im)
    draw.text((100,100),text,fill=(1),font = font)
    epd.display_Partial(epd.getbuffer(text_im),0,0,800,480)
    #epd.display(epd.getbuffer(frame))
    return {},200

if __name__ == "__main__":
    epd.init_part()
    app.run(host="0.0.0.0", port=8000)

