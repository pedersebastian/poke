import PIL, os, pytesseract, re
from PIL import Image, ImageDraw 
import pandas as pd
import numpy as np 
from PIL.ExifTags import TAGS


########################


#### Hjelpefunksjoner
def get_name(image):
    try:
        navn_coord = (50,150, 600,500)
        croped = image.crop(navn_coord)
        name = pytesseract.image_to_string(croped).split("\n")[0]
    except:
        name = ""
        print("Name faila")
    return name


def get_xp(image):
    try:
        xp_coord = (600,1500,1290,1800)
        croped = image.crop(xp_coord)
        xps = pytesseract.image_to_string(croped).replace(" ", "").replace("\n", "").split("/")
        xp, av = (int(xps[0]), int(xps[1]))
    except :
        xp, av = (-1, -1)
    return xp, av


def get_stats(image):
    try:
        battle_coord = (700,2300,1100, 2600)
        croped = image.crop(battle_coord)
        stats = [x.replace(",", ".").replace(" ", "") for x in pytesseract.image_to_string(croped).split("\n") if x != ""]
        stats = [int(stats[0]), float(stats[1]), int(stats[2])]
    except:
        stats = [-1, -1, -1]
    return stats


def get_buddy(image):
    try:
        buddy_coord = (10,300,500,450)
        croped = image.crop(buddy_coord)

        bud = list(filter(lambda x: ( "&" in x), pytesseract.image_to_string(croped).split("\n")))[0].replace("&", "").replace(" ", "")
        return bud
    except :
        return ""
    
    
def get_level(image):
    try:
        lvl_coord = (0,1500,220, 1620)
        croped = image.crop(lvl_coord)
        lvl = pytesseract.image_to_string(croped, config='outputbase digits').replace("\n", "")
        return int(lvl)
    except:
        return -1
    
    
def get_date(image):
    try:
        exif = {}

        # iterating over the dictionary 
        for tag, value in image._getexif().items():

        #extarcting all the metadata as key and value pairs and converting them from numerical value to string values
            if tag in TAGS:
                exif[TAGS[tag]] = value
        return exif["DateTimeOriginal"]
    except:
        return ""
    
def heart_fun(image):
    #
    try:
        im_gray = prep_gray(image, (60,380,370, 460))
        if pytesseract.image_to_string(im_gray) != "":
            raise RecursionError
        out = np.array(im_gray).mean()
        im_gray
    except RecursionError:
        try:
            im_gray = prep_gray(image, coord = (60,450,370, 530))
            out = np.array(im_gray).mean()
        except:
            pass
    except:
        pass
    return out

def prep_gray(image, coord):
    croped = image.crop(coord)

    gray = PIL.ImageOps.grayscale(croped) 
    return gray


var = 30
get_coord = lambda x, y: (x-var, y-var, x + var, y + var)


def heart_to_numeric(img, which,  nickname = False):
    hearts_coord_normal = {
                "one": get_coord(115, 419.3),
                "two": get_coord(186.5, 419.3), 
                "three": get_coord(258, 419.3), 
                "four": get_coord(330, 419.3)
            }

    
    hearts_coord_nick = {
                "one": get_coord(115, 491),
                "two": get_coord(186.5, 491), 
                "three": get_coord(258, 491), 
                "four": get_coord(330, 491)
            }




    if nickname: 
        coord = hearts_coord_nick[which]
    else:
        coord = hearts_coord_normal[which]


    croped = img.crop(coord)
    #croped.show()
    img = PIL.ImageOps.grayscale(croped) 
    #img.show()
    height,width = img.size 
    lum_img = Image.new('L', [height,width] , 0) 

    draw = ImageDraw.Draw(lum_img) 
    draw.pieslice([(0,0), (height,width)], 0, 360,  
                fill = 255, outline = "white") 
    img_arr =np.array(img) 
    lum_img_arr =np.array(lum_img) 

    final_img_arr = np.dstack((img_arr,lum_img_arr)) 
    #Image.fromarray(final_img_arr).show()

    return final_img_arr.mean()

def has_nickname(im):
    
    text =  pytesseract.image_to_string(im.crop((10,300,500,450)))
    try:
        find_in_first = re.search('"', text.split("\n")[0]).start()>0
    except:
        find_in_first = False

    if text.startswith('\"'):
        return True
    
    elif find_in_first:
        return True
    else:
        return False


def heat_fun_2(image):
    nickname = has_nickname(image)
    try:
         out = [
            heart_to_numeric(image, "one", nickname),
            heart_to_numeric(image, "two", nickname),
            heart_to_numeric(image, "three", nickname),
            heart_to_numeric(image, "four", nickname)
         ]
    except Exception as e:
        print(e)
        out = [-1, -1, -1, -1]
    
   
    return out


#### Hoved

def pokevenn(path):
    im = Image.open(path)
    
    username = get_name(im)
    xp, av = get_xp(im)
    stats = get_stats(im)
    buddy = get_buddy(im)
    lvl = get_level(im)
    date = get_date(im)
    hearts = heat_fun_2(im)
    nickname =  has_nickname(im)
    
    res = {
        "username": username, 
        "has_nickname": nickname, 
        "level": lvl,
        "path": path,
        "xp": xp, 
        "lvl_xp": av, 
        "battles_won": stats[0],
        "walked": stats[1], 
        "caught": stats[2], 
        "buddy": buddy, 
        "date": date, 
        "hearts_1": hearts[0], 
        "hearts_2": hearts[1], 
        "hearts_3": hearts[2], 
        "hearts_4": hearts[3], 
        "hearts": np.sum(hearts)
        
    }
    return res


