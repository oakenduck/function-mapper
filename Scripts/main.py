from PIL import Image
from math import sin, floor
from datetime import datetime

now = datetime.now()

mode, size = 'RGBA', (300, 300)

def leftover(x, y):
    """ Keep x within range y """
    return sin(x) * y + y / 2
    #return x % y


def hex_convert(num):
    """ Takes a number, converts it into base 16, in 6 digit format min/max. """
    n = int(num)
    num = hex(abs(num))[2:]  # get the hex value minus the 0x

    if len(num) < 6:
        num = "0" * (6 - len(num)) + num

    for i in 'ghijklmnopqrstuvwxyz':
        if i in num:
            print(n, num)

    return num[:2], num[2:4], num[4:]


def imageAND(a, b):
    # display all pixels where the images overlap in exact value
    try:
        imgA = Image.open(f"{a}.png")
        imgB = Image.open(f"{b}.png")
    except FileNotFoundError:
        return print('One or more files not found.')

    pMapA = imgA.load()
    pMapB = imgB.load()

    # keeps the size of the new image within range of the smallest image, to prevent index errors.
    x_size = min(imgA.size[0], imgB.size[0])
    y_size = min(imgA.size[1], imgB.size[1])

    new = Image.new('RGBA', (x_size, y_size))
    pMapNew = new.load()

    for x in range(x_size):
        for y in range(y_size):
            if pMapA[x, y] == pMapB[x, y]:
                pMapNew[x, y] = pMapA[x, y]
                continue
            pMapNew[x, y] = (0, 0, 0, 0)

    new.show()


def fImage(function, size, save = False):
    img = Image.new("RGBA", size)
    pMap = img.load()

    for x in range(size[0]):
        for y in range(size[1]):
            num = [leftover(int(i,16), 255) for i in hex_convert(round(function(x, y)))]
            value = r, g, b, a = (num[0], num[1], num[2], 255)
            value = tuple(int(i) for i in value)
            pMap[x, y] = value

    img.show()
    if save:
        img.save(f"images/cf2-test-{now.strftime('%y_%m_%d_%H_%M_%S')}.png")
    img.close()


fImage((lambda x, y: x * y), (100, 100), save = True)
