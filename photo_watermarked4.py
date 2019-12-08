from PIL import Image, ImageDraw, ImageFont
import glob
import time
import piexif
import json
import urllib.request
import util
import progressbar
from progressbar import AdaptiveETA, Bar, Percentage,SimpleProgress, Timer


bar = progressbar.ProgressBar(widgets=[Percentage()," ",
                                        "[",SimpleProgress(),"]",
                                        "  ",AdaptiveETA(), "  ",
                                        Bar(marker = '>')])


for img_file in bar(glob.glob("*.jpg")):
    addr, date = util.get_photo_addr_date(img_file)
    #打开图片
    im = Image.open(img_file)
    #字体颜色
    fillcolor = (255,255,255)
    #获取图片尺寸，依据图片大小来计算字号
    width,length = im.size
    mi = min(width,length)
    fontsize = int(mi/15)
    
    draw = ImageDraw.Draw(im)



    pos = (50,length-fontsize*2.5)

    myfont = ImageFont.truetype("NotoSansHans-Thin-Windows.otf", size=fontsize)

    draw.text(pos,addr+date , font=myfont, fill=fillcolor)

    im.save("wm-"+img_file, 'JPEG')


    

input('OK!')


