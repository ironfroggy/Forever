def basic9filter(surface, pixel_func):
    for x in xrange(surface.get_width()):
        for y in xrange(surface.get_height()):
            if x > 0 and y > 0 and x < surface.get_width() - 2 and y < surface.get_height() - 2:
                colors = []
                for xo in (-1, 0, 1):
                    for yo in (-1, 0, 1):
                        colors.append(surface.get_at((x+xo, y+yo)))

                pixel_func(surface, (x, y), colors)

def blur_pixel(surface, (x, y), colors):
    red = 0
    green = 0
    blue = 0
    for color in colors:
        red += color[0]
        green += color[1]
        blue += color[2]
    red /= 9.0
    green /= 9.0
    blue /= 9.0
    color = (red, green, blue)
    surface.set_at((x, y), color)

def blur(surface):
    basic9filter(surface, blur_pixel)

def dim_pixel(surface, (x, y), colors):
    red, green, blue, alpha = colors[4]
    surface.set_at((x, y), (red*0.5, green*0.5, blue*0.5))

def dim(surface):
    basic9filter(surface, dim_pixel)
