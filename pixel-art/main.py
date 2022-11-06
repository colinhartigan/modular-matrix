from PIL import Image
import colorsys

def preprocess(img):
    #img = img.resize((16, 16), Image.ANTIALIAS)
    #img = img.convert()
    #img.save('shrunk.png', quality=95)
    return img

def encode(img):
    width, height = img.size
    pixel_values = list(img.getdata())
    pixel_values = [pixel_values[i * width:(i + 1) * width] for i in range(height)]
    new_pixel_values = []
    for row in pixel_values:
        new = []
        for pixel in row:
            if pixel[3] != 255:
                new.append(0)
            else:
                new.append(1)
        new_pixel_values.append(new)

    # rotate the image by 90 degrees clockwise
    new_pixel_values = [[x[i] for x in new_pixel_values] for i in range(len(new_pixel_values[0]))]

    print(new_pixel_values)

def main():
    img = Image.open(r'D:/colin/programming/modular-matrix/pixel-art/Untitled.png')
    img = preprocess(img)
    encode(img)

if __name__ == '__main__':
    main()