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


def randComp(maxNum):
    return Math.floor(Math.random() * maxNum) + 1


async def createCityImageList(args):
    list = []

    # the street background
    list.push(await loadImage(IMG_PATH + "Main-Street-Pattern.png"))

    # draw a basic, random city
    # the other components, if selected, can just draw right on top of these
    list.push(await loadImage(IMG_PATH + "TLL-0" + randComp(4) + ".png"))
    list.push(await loadImage(IMG_PATH + "TL-0" + randComp(6) + ".png"))
    list.push(await loadImage(IMG_PATH + "TR-0" + randComp(7) + ".png"))
    list.push(await loadImage(IMG_PATH + "TRR-0" + randComp(5) + ".png"))
    list.push(await loadImage(IMG_PATH + "LL-0" + randComp(6) + ".png"))
    list.push(await loadImage(IMG_PATH + "L-0" + randComp(6) + ".png"))
    list.push(await loadImage(IMG_PATH + "R-0" + randComp(6) + ".png"))
    list.push(await loadImage(IMG_PATH + "RR-0" + randComp(7) + ".png"))
    list.push(await loadImage(IMG_PATH + "BLL-0" + randComp(6) + ".png"))
    list.push(await loadImage(IMG_PATH + "BL-0" + randComp(7) + ".png"))
    list.push(await loadImage(IMG_PATH + "BR-0" + randComp(8) + ".png"))
    list.push(await loadImage(IMG_PATH + "BRR-0" + randComp(7) + ".png"))

    # if there's a highway, it supercedes any other drawing
    if "highway" in args:
        list.push(await loadImage(IMG_PATH + "Highway-Base.png"))

        # the little bits & bobs surrounding the highways
        for i in (0.0).NUM_HIGHWAY_COMPS:
            list.push(await loadImage(IMG_PATH + "Highway-01-0" + randComp(3) + ".png"))
            list.push(await loadImage(IMG_PATH + "Highway-02-0" + randComp(3) + ".png"))
            list.push(await loadImage(IMG_PATH + "Highway-03-0" + randComp(4) + ".png"))
            list.push(await loadImage(IMG_PATH + "Highway-04-0" + randComp(4) + ".png"))
            list.push(await loadImage(IMG_PATH + "Highway-05-0" + randComp(3) + ".png"))
            list.push(await loadImage(IMG_PATH + "Highway-06-0" + randComp(4) + ".png"))
            list.push(await loadImage(IMG_PATH + "Highway-07-0" + randComp(3) + ".png"))
            list.push(await loadImage(IMG_PATH + "Highway-08-0" + randComp(3) + ".png"))

        # ...and then, we might have one of the highways that leads out of the city
        if args.highway.includes("tr"):
            list.push(await loadImage(IMG_PATH + "Highway-TR.png"))
        elif args.highway.includes("bl"):
            list.push(await loadImage(IMG_PATH + "Highway-BL.png"))
    else:
        if "cityLimit" in args:
            if args.cityLimit.includes("tl"):
                list.push(await loadImage(IMG_PATH + "Special-TL-CityLimit-01.png"))
            elif args.cityLimit.includes("t"):
                list.push(
                    await loadImage(
                        IMG_PATH + "Special-T-CityLimit-0" + randComp(2) + ".png"
                    )
                )
            elif args.cityLimit.includes("l"):
                list.push(await loadImage(IMG_PATH + "Special-L-CityLimit-01.png"))
            elif args.cityLimit.includes("r"):
                list.push(
                    await loadImage(
                        IMG_PATH + "Special-R-CityLimit-0" + randComp(2) + ".png"
                    )
                )
            elif args.cityLimit.includes("b"):
                list.push(
                    await loadImage(
                        IMG_PATH + "Special-B-CityLimit-0" + randComp(2) + ".png"
                    )
                )
        else:
            # some of the specials prevent us from drawing longer blocks on the sides
            canDoLongBlockL = True
            canDoLongBlockR = True

            if "special" in args:
                # these two should be mutually exclusive
                if args.special.includes("cottonCove"):
                    canDoLongBlockR = false
                    list.push(await loadImage(IMG_PATH + "Special-BR-CottonCove.png"))
                elif args.special.includes("lyttonPark"):
                    canDoLongBlockL = false
                    list.push(await loadImage(IMG_PATH + "Special-L-LyttonPark.png"))

                # specials on the right can overlap, tho you'll only see one
                if args.special.includes("bertsPark"):
                    list.push(await loadImage(IMG_PATH + "Special-R-BertsPark.png"))
                if args.special.includes("jail"):
                    list.push(await loadImage(IMG_PATH + "Special-R-Jail.png"))

                # ...and likewise for specials on the left
                if args.special.includes("blueRoom"):
                    list.push(await loadImage(IMG_PATH + "Special-L-BlueRoom.png"))
                if args.special.includes("caffeineWino"):
                    list.push(await loadImage(IMG_PATH + "Special-L-CaffeineWino.png"))
                if args.special.includes("commBldg"):
                    list.push(await loadImage(IMG_PATH + "Special-L-CommBldg.png"))
                if args.special.includes("courthouse"):
                    list.push(await loadImage(IMG_PATH + "Special-L-Courthouse.png"))
                if args.special.includes("hotel"):
                    list.push(
                        await loadImage(IMG_PATH + "Special-L-HotelDelphoria.png")
                    )
                if args.special.includes("police"):
                    list.push(await loadImage(IMG_PATH + "Special-L-PoliceHQ.png"))

            # random chance of drawing one of the long-blocks on the sides
            if canDoLongBlockL and Math.random() < LONG_BLOCK_CHANCE:
                list.push(
                    await loadImage(IMG_PATH + "LL-Block-0" + randComp(3) + ".png")
                )
            if canDoLongBlockR and Math.random() < LONG_BLOCK_CHANCE:
                list.push(
                    await loadImage(IMG_PATH + "RR-Block-0" + randComp(2) + ".png")
                )

    return list


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
