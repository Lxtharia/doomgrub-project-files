from math import ceil, log
from PIL import Image
from bitarray import bitarray



# open every symbol
# map it?
# read all of the shades of gray (256) into a dedicated array in a dict?
# we need 256 fonts, every font has 71 or something chars
# every char should be an object of
#   width  (2 byte),
#   height (2 byte),
#   xoffset (2 byte) = 0,
#   yoffset (2 byte) = 0 ? what about p or q?,
#   device width (2 byte) = -1
# (different for each color):
#   bitmap data = (w * h + 7) / 8 bytes

def toByte(x: int, length: int) -> bytes:
    return (x).to_bytes(length, byteorder="big")

def sectionLen(bytes: bytes):
    return len(bytes).to_bytes(4, byteorder="big")


metadata = {}
# They actually need to be in codepoint order!!
chars = " !%-./0123456789:;?ABCDEFGHIJKLMNOPQRSTUVWXYZ`abcdefghijklmnopqrstuvwxyz"
char_file_names = {c: c for c in chars}
for c in "abcdefghijklmnopqrstuvwxyz":
    char_file_names[c] = "lower" + c.upper()
char_file_names[' '] = "SPACE"
char_file_names['!'] = "EXCL"
char_file_names['`'] = "TICK"
char_file_names[';'] = "SEMICOL"
char_file_names[':'] = "COL"
char_file_names['.'] = "DOT"
char_file_names['%'] = "PERCENT"
char_file_names['?'] = "QUES"
char_file_names['-'] = "DASH"
char_file_names['/'] = "SLASH"
char_amount = len(chars)
print(char_file_names)


# size of the font, Ascent + Descent (here: 15 + 2)
ascent = 15
descent = 2
font_size_px = ascent + descent
# how many fonts we want, because 256 is too much lol, pst_range is how many shades of gray are in one posterization color
graustufen = 8
pst_range = 256 // graustufen
# all the font indices we wanna modify :)
gray_list = [pst_range//2 + g * pst_range for g in range(graustufen)]
print(gray_list)
# all the fonts
fonts = [{c: bitarray(endian="big") for c in chars} for g in range(255)]

# how big one pixel of the png should be in the font
pxsize: int = 5
font_size = font_size_px * pxsize


maxw = 0
maxh = 0

for c in chars:
    print("Processing character: \'" + c + "\'")
    # load image
    filename = char_file_names[c] + ".png"
    img: Image = Image.open("./characterPngs/" + filename)
    # grayscale mode
    img.convert("LA")
    # get data and write is scaled as a tuple into metadata
    w: int = img.width
    h: int = img.height
    x: int = 0
    y: int = 0 if c != "Q" else 2
    device_width: int = img.width - 1
    metadata[c] = {"w": w*pxsize, "h": h*pxsize, "x": x*pxsize, "y": y*pxsize, "device_width": device_width * pxsize}
    # print("\t", metadata)

    # maxW and maxH, because idk
    if w > maxw:
        maxw = w
    if h > maxh:
        maxh = h

    # iterate through pixels
    pixels = img.load()
    for y in range(h*pxsize):
        for x in range(w):
            px_gray, px_alpha = pixels[x, y//pxsize]
            # if pixel is transparent
            if px_alpha == 0:
                # write 0 in every font (at fonts[0-255]['A']
                for gray in gray_list:
                    fonts[gray][c] += '0'*pxsize
            # if pixel is color 124 or something
            else:
                # write 1 in the font pst_range//2 + (124//pst_range) * pst_range  and 0 into every other
                # iterate through all the grays
                for gray in gray_list:
                    # if our pixel belongs in that font (should be mapped to that one)
                    gray_to_be_mapped_to = pst_range//2 + (px_gray//pst_range) * pst_range
                    if gray == gray_to_be_mapped_to:
                        fonts[gray][c] += '1'*pxsize
                    else:
                        fonts[gray][c] += '0'*pxsize

    # convert bitarray to bytes
    for gray in gray_list:
        fonts[gray][c] = fonts[gray][c].tobytes()

    # for i, font in enumerate(fonts):
    #     for character in font:
    #         # print("Font greyvalue:", i, "char:", character,  ":",font[character], bin(font[character]))
    #         pass
    # # test, funzt!!
    # with open("out.lmao", "ab") as out:
    #     out.write(fonts[69]["A"])
    #     out.write(b"%06b" % b"kekw")
    # pass

# write these to file now lmao


maxw = toByte(maxw * pxsize, 2)
maxh = toByte(maxh * pxsize, 2)
asce = toByte(font_size, 2)
# descend of 2 pixels
desc = toByte(2 * pxsize, 2)
ptsz = toByte(font_size, 2)
chix_len = 9*char_amount

for gray in gray_list:
    font = fonts[gray]
    # write ALMOST always the same header
    name = b"DoomShade Regular %s %s\x00" % (f"shade{gray}".encode(encoding='utf-8'), str(font_size).encode(encoding='utf-8'))
    name_len = toByte(len(name), 4)
    # this has some hard coded section lengths (these ---v ), so you just gotta count

    header = b"FILE\x00\x00\x00\x04PFF2NAME%b%b" % (name_len, name) \
             + b"FAMI\x00\x00\x00\x0ADoomShade\x00WEIG\x00\x00\x00\x07normal\x00SLAN\x00\x00\x00\x07normal\x00" \
               b"PTSZ\x00\x00\x00\x02%bMAXW\x00\x00\x00\x02%bMAXH\x00\x00\x00\x02%bASCE\x00\x00\x00\x02%bDESC\x00\x00\x00\x02%bCHIX%b" \
             % (ptsz, maxw, maxh, asce, desc, toByte(chix_len, 4))

    with open(f"./doomgrub-theme/DoomShade{gray}.pf2", "wb+") as font_file:
        font_file.write(header)
        data_start = len(header) + chix_len + 4 + 4
        data_offset = 0
        # CHIX....
        for c_index, c in enumerate(chars):
            # 4 bytes: unicode code point
            font_file.write(toByte(ord(c), 4))
            # 1 byte:  0
            font_file.write(b"\x00")
            # 4 bytes: OFFSET (needs to be calculated)
            # the offset is the datastart + data_offset
            offset = data_start + data_offset
            font_file.write(toByte(offset, 4))
            # data_offset gets incremented by the amount of bytes we need for our current character
            data_offset += 2 + 2 + 2 + 2 + 2 + len(font[c])
        # DATA....
        font_file.write(b"DATA\xff\xff\xff\xff")
        for c_index, c in enumerate(chars):
            # ...v (at position CHIX+4 + (9 * c)
            # w w h h x x y y d d
            ww = toByte(metadata[c]["w"], 2)
            hh = toByte(metadata[c]["h"], 2)
            xx = toByte(metadata[c]["x"], 2)
            yy = toByte(metadata[c]["y"], 2)
            dd = toByte(metadata[c]["device_width"], 2)
            # bitmap data data data w*h bits

            char_data = ww + hh + xx + yy + dd + font[c]
            font_file.write(char_data)


