from waveshare import epd7in5_V2
from PIL import Image, ImageDraw, ImageFont
from flask import Flask, request
import io
import utils
import datetime
import time
import threading

app = Flask(__name__)

epd = epd7in5_V2.EPD()
epd.init()

class Screen():
    def __init__(self,epd):
        self.thread = threading.Thread(target=self.run_clock)
        self.message = ''
        self.epd = epd
        self.stop_event = threading.Event()
    
    def run_clock(self):
        i = 0
        t = ''
        while not self.stop_event.is_set():
            now = datetime.datetime.now()
            seconds_till_next_minute = 60 - now.second
            #time.sleep(seconds_till_next_minute)
            time.sleep(1)
            current_time = now.strftime("%I:%M %p")
            if current_time != t:
                self.epd.init_part()
                t = current_time
                text_im = Image.new("1",(800,480),1)
                draw = ImageDraw.Draw(text_im)
                font=ImageFont.truetype("./magicsummer.otf",200)
                font2=ImageFont.truetype("./arial.ttf",50)
                text_width, text_height = draw.textsize(current_time, font=font)
                x = (800 - text_width) // 2
                y = (480 - text_height) // 2 - 100
                draw.text((x,y),current_time,fill=(0),font = font)
                text_width, text_height = draw.textsize(self.message, font=font2)
                x = (800 - text_width) // 2
                y = 300
                draw.text((x,y),self.message,fill=(0),font = font2)
                if i%10 == 0:
                    self.epd.display(self.epd.getbuffer(text_im))
                else:
                    self.epd.display_Partial(self.epd.getbuffer(text_im),0,0,800,480)
                self.epd.sleep()
                i += 1

    def set_message(self,message):
        self.message = message
    
    def start_clock(self):
        self.epd.Clear()
        self.epd.init_part()
        self.thread.start()
    
    def stop_clock(self):
        self.stop_event.set()
        self.thread.join()

screen = Screen(epd)

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

@app.route("/show_safezone",methods=['GET'])
def show_safezone():
    epd.Clear()
    epd.init_part()
    return {}, 200

#Update safezone by either increasing/decreasing width of the box
#Safezone 
@app.route("/adjust_safezone",methods=['POST'])
def adjust_safezone():
    req = request.get_json()
    xy = [(req['x0'],req['y0']),(req['x1'],req['y1'])]
    safezone_im = Image.new("1",(800,480),1)
    draw = ImageDraw.Draw(safezone_im)
    draw.rectangle(xy,width=3, outline=0)
    epd.display_Partial(epd.getbuffer(safezone_im),0,0,800,480)
    return {},200

#If in the safezone screen, save the current one and go back to whatever was displayed before
@app.route("/save_safezone",methods=['GET'])
def save_safezone():
    epd.sleep()
    return {},200

@app.route("/write_text",methods=['GET'])
def write_text():
    epd.init_part()
    font=ImageFont.truetype("arial.ttf",40)
    text = request.args.get('text')
    text_im = Image.new("1",(800,480),0)
    draw = ImageDraw.Draw(text_im)
    draw.text((100,100),text,fill=(1),font = font)
    epd.display_Partial(epd.getbuffer(text_im),0,0,800,480)
    #epd.display(epd.getbuffer(frame))
    return {},200

@app.route('/show_clock',methods=["POST"])
def show_clock():
    req = request.get_json()
    width = 760-60
    height = 460-35
    epd.Clear()
    screen.start_clock()
    return {},200

@app.route('/stop_clock',methods=["POST"])
def stop_clock():
    screen.stop_clock()
    return {},200

@app.route('/set_message',methods=["POST"])
def set_message():
    req = request.get_json()
    screen.set_message(req['message'])
    return {},200
        

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8000)

