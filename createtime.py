from PIL import Image
from PIL import ImageFont
from PIL import ImageDraw 
from datetime import datetime
import os

folder = os.environ.get("HASH_HOME")
if not folder:
	print "Please set HASH_HOME"
	sys.exit(0)

img = Image.open(HASH_HOME+"templates/time.jpg")

currently = datetime.now()
draw = ImageDraw.Draw(img)
font = ImageFont.truetype(HASH_HOME+fonts/ruben.ttf", 60)

draw.text((360, 40), currently.strftime("%H:%M:%S"), (0,0,0), font=font)
draw.text((330, 120), currently.strftime("%d/%m/%Y"), (0,0,0), font=font)
img.save(HASH_HOME+'images/time.jpg')
