from PIL import Image


def parse_xy(xy_string: str):
    x, y = xy_string.split(",")
    xy_array = [int(x), int(y)]
    return xy_array


def parse_coordinate(coord_string: str):
    coord_dict = {}
    coord_string = coord_string.split("i:")[1]
    lu, coord_string = coord_string.split("+")
    rb, trans = coord_string.split(">")
    coord_dict["lu"] = parse_xy(lu)
    coord_dict["rb"] = parse_xy(rb)
    coord_dict["trans"] = parse_xy(trans)
    return coord_dict


def descramble(scrambled_image: Image.Image, data_json: dict):

    image_fragments = []
    coord_strings = data_json["views"][0]["coords"]
    parsed_coords = []

    for coord in coord_strings:
        coord_dict = parse_coordinate(coord)
        parsed_coords.append(coord_dict)
        box = (coord_dict["lu"] + coord_dict["rb"])
        box[2] += box[0]
        box[3] += box[1]
        split_image = scrambled_image.crop(box)
        image_fragments.append(split_image)

    descrambled_image = Image.new("RGB", (data_json["views"][0]["width"], data_json["views"][0]["height"]))

    for i in range(0, len(image_fragments)):
        current_coords = parsed_coords[i]
        current_image = image_fragments[i]
        transform = current_coords["trans"]
        box = (transform + [current_image.width + transform[0], current_image.height + transform[1]])
        descrambled_image.paste(current_image, box)

    return descrambled_image
