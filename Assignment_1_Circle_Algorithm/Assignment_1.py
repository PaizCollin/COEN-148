from PIL import Image 

# init image dimensions
imgWidth = 320
imgHeight = 240

# init img for circle & fill
img = Image.new('RGB', (imgWidth, imgHeight)) 
pixels = img.load() 

# init img2 for anti-aliasing
img2 = Image.new('RGB', (imgWidth, imgHeight)) 
pixels2 = img2.load() 

# put pixels
def drawCircle(xc, yc, x, y): 
    img.putpixel((xc+x, yc+y), (255, 0, 0))         # 270 - 315 (degrees by unit circle)
    img.putpixel((xc-x, yc+y), (255, 0, 0))         # 225 - 270
    img.putpixel((xc+x, yc-y), (255, 0, 0))         # 45 - 90
    img.putpixel((xc-x, yc-y), (255, 0, 0))         # 90 - 135
    img.putpixel((xc+y, yc+x), (255, 0, 0))         # 315 - 0
    img.putpixel((xc-y, yc+x), (255, 0, 0))         # 180 - 225
    img.putpixel((xc+y, yc-x), (255, 0, 0))         # 0 - 45
    img.putpixel((xc-y, yc-x), (255, 0, 0))         # 135 - 180

# midpoint circle
def midpointCircle(xc, yc, r):
    x = 0
    y = r
    d = 5/4 - r

    while(x <= y):
        drawCircle(xc, yc, x, y)
        x += 1
        
        if(d < 0):
            d += 2 * x + 3
        else:
            d += (2*x) - (2*y) - 5
            y -= 1

# scanline fill
def scanlineFill(xc, yc, x, y, r):
    return (((x-xc)**2 + (y-yc)**2) < (r**2))

# anti-aliasing
def antiAliasing(x, y):
    th = 0.01
    factor = (1-th) / 4
    pixel = pixels[x, y]

    # get current pixel rgb
    r = pixel[0] * th
    g = pixel[1] * th
    b = pixel[2] * th

    # top pixel (within img range)
    if(y != 0):
        r += pixels[x, y-1][0] * factor
        g += pixels[x, y-1][1] * factor
        b += pixels[x, y-1][2] * factor

    # bottom pixel (within img range)
    if(y != imgHeight - 1):
        r += pixels[x, y+1][0] * factor
        g += pixels[x, y+1][1] * factor
        b += pixels[x, y+1][2] * factor

    # left pixel (within img range)
    if(x != 0):
        r += pixels[x-1, y][0] * factor
        g += pixels[x-1, y][1] * factor
        b += pixels[x-1, y][2] * factor

    # right pixel (within img range)
    if(x != imgWidth - 1):
        r += pixels[x+1, y][0] * factor
        g += pixels[x+1, y][1] * factor
        b += pixels[x+1, y][2] * factor

    # top left pixel (within img range)
    if(y != 0 and x != 0):
        r += pixels[x-1, y-1][0] * factor
        g += pixels[x-1, y-1][1] * factor
        b += pixels[x-1, y-1][2] * factor

    # top right pixel (within img range)
    if(y != 0 and x != imgWidth - 1):
        r += pixels[x+1, y-1][0] * factor
        g += pixels[x+1, y-1][1] * factor
        b += pixels[x+1, y-1][2] * factor

    # bottom left pixel (within img range)
    if(y != imgHeight - 1 and x != 0):
        r += pixels[x-1, y+1][0] * factor
        g += pixels[x-1, y+1][1] * factor
        b += pixels[x-1, y+1][2] * factor

    # bottom right pixel (within img range)
    if(y != imgHeight - 1 and x != imgWidth - 1):
        r += pixels[x+1, y+1][0] * factor
        g += pixels[x+1, y+1][1] * factor
        b += pixels[x+1, y+1][2] * factor

    return(int(r), int(g), int(b))

if __name__ == '__main__':

    # center of image
    xc = int(imgWidth / 2)
    yc = int(imgHeight / 2)

    # radius
    r = 105

    # draw midpoint circle
    midpointCircle(xc, yc, r)
    img.save("circle.png")

    # scanline fill
    for x in range(imgWidth):
            for y in range(imgHeight):
                if scanlineFill(xc, yc, x, y, r):
                    img.putpixel((x, y), (255, 0, 0))
    img.save("filled.png")

    # anti-aliasing
    # reads pixel data from original circle
    # writes anti-aliased pixels to new image (prevent smudging)
    for x in range(imgWidth):
        for y in range(imgHeight):
            pixels2[x, y] = antiAliasing(x, y)
    img2.save("anti-aliased.png")

    # img.show()
    # img2.show()