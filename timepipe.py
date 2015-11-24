from PIL import Image
from PIL import ImageFont
from PIL import ImageDraw 
from datetime import datetime

def child():
	pipeout = os.open('/tmp/image.jpg', os.O_WRONLY)
	
	img = Image.open("/home/david/davidhashelhoff/templates/time.jpg")

	currently = datetime.now()
	draw = ImageDraw.Draw(img)
	font = ImageFont.truetype("/home/david/davidhashelhoff/fonts/ruben.ttf", 60)

	draw.text((360, 40), currently.strftime("%H:%M:%S"), (0,0,0), font=font)
	draw.text((330, 120), currently.strftime("%d/%m/%Y"), (0,0,0), font=font)
	img.save(pipeout)
	

if not os.path.exists('/tmp/image.jpg'):
	os.mkfifo(pipe_name)
pid = os.fork()
if pid == 0:
	child()

