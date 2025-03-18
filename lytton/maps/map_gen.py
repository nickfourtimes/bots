import io
import random

randint = random.randint

from PIL import Image

# Constants

IMG_PATH = "./lytton/maps/components/"
MAP_WIDTH = 320
MAP_HEIGHT = 168
NUM_HIGHWAY_COMPS = 8
LONG_BLOCK_CHANCE = 0.2


def create_city_image_list(args):
    """
    Return a list of PNG path names in the order in which they should be drawn.
    """

    list = []

    # draw a basic, random city
    # the other components, if selected, can just draw right on top of these
    list.append(f"{IMG_PATH}TLL-0{randint(1, 4)}.png")
    list.append(f"{IMG_PATH}TL-0{randint(1, 6)}.png")
    list.append(f"{IMG_PATH}TR-0{randint(1, 7)}.png")
    list.append(f"{IMG_PATH}TRR-0{randint(1, 5)}.png")
    list.append(f"{IMG_PATH}LL-0{randint(1, 6)}.png")
    list.append(f"{IMG_PATH}L-0{randint(1, 6)}.png")
    list.append(f"{IMG_PATH}R-0{randint(1, 6)}.png")
    list.append(f"{IMG_PATH}RR-0{randint(1, 7)}.png")
    list.append(f"{IMG_PATH}BLL-0{randint(1, 6)}.png")
    list.append(f"{IMG_PATH}BL-0{randint(1, 7)}.png")
    list.append(f"{IMG_PATH}BR-0{randint(1, 8)}.png")
    list.append(f"{IMG_PATH}BRR-0{randint(1, 7)}.png")

    # if there's a highway, it supercedes any other drawing
    if "highway" in args:
        list.append(f"{IMG_PATH}Highway-Base.png")

        # the little bits & bobs surrounding the highways
        for i in range(NUM_HIGHWAY_COMPS):
            list.append(f"{IMG_PATH}Highway-01-0{randint(1, 3)}.png")
            list.append(f"{IMG_PATH}Highway-02-0{randint(1, 3)}.png")
            list.append(f"{IMG_PATH}Highway-03-0{randint(1, 4)}.png")
            list.append(f"{IMG_PATH}Highway-04-0{randint(1, 4)}.png")
            list.append(f"{IMG_PATH}Highway-05-0{randint(1, 3)}.png")
            list.append(f"{IMG_PATH}Highway-06-0{randint(1, 4)}.png")
            list.append(f"{IMG_PATH}Highway-07-0{randint(1, 3)}.png")
            list.append(f"{IMG_PATH}Highway-08-0{randint(1, 3)}.png")

        # ...and then, we might have one of the highways that leads out of the city
        if "tr" in args["highway"]:
            list.append(f"{IMG_PATH}Highway-TR.png")
        elif "bl" in args["highway"]:
            list.append(f"{IMG_PATH}Highway-BL.png")
    else:
        if "cityLimit" in args:
            if "tl" in args["cityLimit"]:
                list.append(f"{IMG_PATH}Special-TL-CityLimit-01.png")
            elif "t" in args["cityLimit"]:
                list.append(f"{IMG_PATH}Special-T-CityLimit-0{randint(1, 2)}.png")
            elif "l" in args["cityLimit"]:
                list.append(f"{IMG_PATH}Special-L-CityLimit-01.png")
            elif "r" in args["cityLimit"]:
                list.append(f"{IMG_PATH}Special-R-CityLimit-0{randint(1, 2)}.png")
            elif "b" in args["cityLimit"]:
                list.append(f"{IMG_PATH}Special-B-CityLimit-0{randint(1, 2)}.png")
        else:
            # some of the specials prevent us from drawing longer blocks on the sides
            canDoLongBlockL = True
            canDoLongBlockR = True

            if "special" in args:
                # these two should be mutually exclusive
                if "cottonCove" in args["special"]:
                    canDoLongBlockR = False
                    list.append(f"{IMG_PATH}Special-BR-CottonCove.png")
                elif "lyttonPark" in args["special"]:
                    canDoLongBlockL = False
                    list.append(f"{IMG_PATH}Special-L-LyttonPark.png")

                # specials on the right can overlap, tho you'll only see one
                if "bertsPark" in args["special"]:
                    list.append(f"{IMG_PATH}Special-R-BertsPark.png")
                if "jail" in args["special"]:
                    list.append(f"{IMG_PATH}Special-R-Jail.png")

                # ...and likewise for specials on the left
                if "blueRoom" in args["special"]:
                    list.append(f"{IMG_PATH}Special-L-BlueRoom.png")
                if "caffeineWino" in args["special"]:
                    list.append(f"{IMG_PATH}Special-L-CaffeineWino.png")
                if "commBldg" in args["special"]:
                    list.append(f"{IMG_PATH}Special-L-CommBldg.png")
                if "courthouse" in args["special"]:
                    list.append(f"{IMG_PATH}Special-L-Courthouse.png")
                if "hotel" in args["special"]:
                    list.append(f"{IMG_PATH}Special-L-HotelDelphoria.png")
                if "police" in args["special"]:
                    list.append(f"{IMG_PATH}Special-L-PoliceHQ.png")

            # random chance of drawing one of the long-blocks on the sides
            if canDoLongBlockL and random.random() < LONG_BLOCK_CHANCE:
                list.append(f"{IMG_PATH}LL-Block-0{randint(1, 3)}.png")
            if canDoLongBlockR and random.random() < LONG_BLOCK_CHANCE:
                list.append(f"{IMG_PATH}RR-Block-0{randint(1, 2)}.png")

    return list


def get_image(city_params):
    img_list = create_city_image_list(city_params)

    # create the basic background image
    image = Image.open(f"{IMG_PATH}Main-Street-Pattern.png")

    for img_path in img_list:
        i = Image.open(img_path)
        image.paste(i, i)
        
    image.save("new_image.png")

    imgByteArr = io.BytesIO()
    image.save(imgByteArr, format=image.format)
    imgByteArr = imgByteArr.getvalue()
    return imgByteArr
