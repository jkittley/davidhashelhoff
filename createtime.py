from PIL import Image
from PIL import ImageFont
from PIL import ImageDraw 
from datetime import datetime
import os
import shutil
import glob
from settings import HASH_HOME

# Directories
images_dir   = os.path.join(HASH_HOME,'images/')
template_dir = os.path.join(HASH_HOME,'templates/')

# Remove all previous time images
for filename in glob.glob(os.path.join(images_dir,'time_*')):
    os.remove(filename) 

# Load template image
tempalate_img = Image.open(os.path.join(template_dir,'time.jpg'))

# Add date and time to image
currently = datetime.now()
draw = ImageDraw.Draw(tempalate_img)
font = ImageFont.truetype(HASH_HOME+"/fonts/ruben.ttf", 60)
draw.text((360, 40), currently.strftime("%H:%M:%S"), (0,0,0), font=font)
draw.text((330, 120), currently.strftime("%d/%m/%Y"), (0,0,0), font=font)

# Save it
tmp = os.path.join(HASH_HOME,'tmp_time_image.jpg')
tempalate_img.save(tmp)
shutil.copyfile(tmp, os.path.join(images_dir, 'time_'+ currently.strftime("%H_%M_%S")+'.jpg'))
