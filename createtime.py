from PIL import Image
from PIL import ImageFont
from PIL import ImageDraw 
from datetime import datetime

img = Image.open("templates/time.jpg")

currently = datetime.now()
 
draw = ImageDraw.Draw(img)

font = ImageFont.truetype("fonts/ruben.ttf", 60)

draw.text((360, 40), currently.strftime("%H:%M:%S"), (0,0,0), font=font)
draw.text((330, 120), currently.strftime("%d/%m/%Y"), (0,0,0), font=font)

img.save('images/time.jpg')