import math
import random

#   Canvas = require("canvas"),
#   loadImage = Canvas.loadImage,
#   img_path_png = "./.data/temp.png"

# ************************************************************************* CONSTS &

IMG_PATH = "./maps/components/"

MAP_WIDTH = 320
MAP_HEIGHT = 168

NUM_HIGHWAY_COMPS = 8
LONG_BLOCK_CHANCE = 0.2

# ************************************************************************* DRAWING


def load_image(path):
    print("hello")


def rand_comp(maxNum):
    return math.floor(random.random() * maxNum) + 1


def create_city_image_list(args):
    """
    Return a list of PNG path names in the order in which they should be drawn.
    """

    list = []

    # the street background
    list.append(f"{IMG_PATH}Main-Street-Pattern.png")

    # draw a basic, random city
    # the other components, if selected, can just draw right on top of these
    list.append(f"{IMG_PATH}TLL-0{rand_comp(4)}.png")
    list.append(f"{IMG_PATH}TL-0{rand_comp(6)}.png")
    list.append(f"{IMG_PATH}TR-0{rand_comp(7)}.png")
    list.append(f"{IMG_PATH}TRR-0{rand_comp(5)}.png")
    list.append(f"{IMG_PATH}LL-0{rand_comp(6)}.png")
    list.append(f"{IMG_PATH}L-0{rand_comp(6)}.png")
    list.append(f"{IMG_PATH}R-0{rand_comp(6)}.png")
    list.append(f"{IMG_PATH}RR-0{rand_comp(7)}.png")
    list.append(f"{IMG_PATH}BLL-0{rand_comp(6)}.png")
    list.append(f"{IMG_PATH}BL-0{rand_comp(7)}.png")
    list.append(f"{IMG_PATH}BR-0{rand_comp(8)}.png")
    list.append(f"{IMG_PATH}BRR-0{rand_comp(7)}.png")

    # if there's a highway, it supercedes any other drawing
    if "highway" in args:
        list.append(f"{IMG_PATH}Highway-Base.png")

        # the little bits & bobs surrounding the highways
        for i in (0.0).NUM_HIGHWAY_COMPS:
            list.append(f"{IMG_PATH}Highway-01-0{rand_comp(3)}.png")
            list.append(f"{IMG_PATH}Highway-02-0{rand_comp(3)}.png")
            list.append(f"{IMG_PATH}Highway-03-0{rand_comp(4)}.png")
            list.append(f"{IMG_PATH}Highway-04-0{rand_comp(4)}.png")
            list.append(f"{IMG_PATH}Highway-05-0{rand_comp(3)}.png")
            list.append(f"{IMG_PATH}Highway-06-0{rand_comp(4)}.png")
            list.append(f"{IMG_PATH}Highway-07-0{rand_comp(3)}.png")
            list.append(f"{IMG_PATH}Highway-08-0{rand_comp(3)}.png")

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
                list.append(f"{IMG_PATH}Special-T-CityLimit-0{rand_comp(2)}.png")
            elif "l" in args["cityLimit"]:
                list.append(f"{IMG_PATH}Special-L-CityLimit-01.png")
            elif "r" in args["cityLimit"]:
                list.append(f"{IMG_PATH}Special-R-CityLimit-0{rand_comp(2)}.png")
            elif "b" in args["cityLimit"]:
                list.append(f"{IMG_PATH}Special-B-CityLimit-0{rand_comp(2)}.png")
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
                list.append(f"{IMG_PATH}LL-Block-0{rand_comp(3)}.png")
            if canDoLongBlockR and random.random() < LONG_BLOCK_CHANCE:
                list.append(f"{IMG_PATH}RR-Block-0{rand_comp(2)}.png")

    return list


def get_image(city_params):
    img_list = create_city_image_list(city_params)
    for img_path in img_list:
        print(f"{img_path}")

# module.exports = async function (cityParams, res, cb) {
#   canvas = Canvas.createCanvas(MAP_WIDTH, MAP_HEIGHT),
#     ctx = canvas.getContext("2d")

#   imgList = await createCityImageList(cityParams)
#   for (i = 0 i < imgList.length ++i) {
#     ctx.drawImage(imgList[i], 0, 0)
#   }

#   out = fs.createWriteStream(img_path_png)
#   stream = canvas.createPNGStream()
#   stream.pipe(out)

#   # # uncomment this if we're just outputting the image directly in a browser
#   # stream.pipe(res)
#   # stream.end()

#   # send the buffered image back to server.js for posting
#   out.on("finish", function () {
#     if (cb) {
#       cb(null, {
#         path: img_path_png,
#         data: canvas.toBuffer().toString("base64"),
#       })
#     }
#   })
# }
