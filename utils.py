from PIL import Image

def get_blank_frame():
    return Image.new("1",(800,480),fill=(0))