from PIL import Image
from math import sin, floor
from datetime import datetime

now = datetime.now()

mode, size = 'RGBA', (300, 300)

def leftover(n, x, y):
    """ Keep n between x and y inclusive. """
    return sin(n) * (x + y) / 2 + (x + y) / 2


def hex_convert(num):
    """ Takes a number num, converts it into base 16, in 6 digit format min/max, to be used in RGB format.
    If num >= 16^6, it will not be properly represented, and instead only return the first 6 digits."""
    n = int(num)
    num = hex(abs(num))[2:]  # get the hex value minus the 0x

    if len(num) < 6:
        num = "0" * (6 - len(num)) + num

    for i in 'ghijklmnopqrstuvwxyz':
        if i in num:
            print(n, num)

    return num[:2], num[2:4], num[4:6]


def imageAND(a, b, save = False):
    """ Iterates over all pixels in images a and b, compares them, sets  """
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

    if save:
        new.save(f"image/imageAND-{now.strftime('%y_%m_%d_%H_%M_%S')}.png")
    new.show()
    new.close()


def fImage(f, size, save = False):
    """ Creates new image, each pixel's color being based on passed in function f of x, y coordinates of given pixel.
    f : function = take 2 variables, x and y, and return a number. No complex or imaginary numbers can be passed in or returned.
    size : tuple = (x axis width, y axis width) Default to (100, 100).
    save : bool = save image after building it or not. Default to False."""
    img = Image.new("RGBA", size)
    pMap = img.load()

    for x in range(size[0]):
        for y in range(size[1]):
            num = [leftover(int(i,16), 0, 255) for i in hex_convert(round(f(x, y)))]
            value = r, g, b, a = (num[0], num[1], num[2], 255)
            value = tuple(int(i) for i in value)
            pMap[x, y] = value

    img.show()
    if save:
        img.save(f"images/fImage-{now.strftime('%y_%m_%d_%H_%M_%S')}.png")
    img.close()


if __name__ == '__main__':
    fImage(
        (lambda x, y: x * y + x * sin(x)),
        (1000, 1000),
        save=True
    )

    imageAND(
        "images/cf2-test-20_05_27_19_31_34",
        "images/cf2-test-20_05_27_19_30_55",
        save=True
    )

else:
    print("""function-mapper project:
    Rendering 3D graphs of functions in color rather than height, using Pillow image manipulation.""")
