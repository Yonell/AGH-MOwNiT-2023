from PIL import Image, ImageOps
import numpy as np

def get_correlation(picture_filename, pattern_filename):
    picture = Image.open(picture_filename)
    pattern = Image.open(pattern_filename)
    picture = ImageOps.invert(picture)
    pattern = ImageOps.invert(pattern)
    picture_size = (picture.size[1], picture.size[0], 3)
    pattern_size = (pattern.size[1], pattern.size[0], 3)
    numpy_picture = np.array(picture.getdata()).reshape(picture_size)
    numpy_pattern = np.array(pattern.getdata()).reshape(pattern_size)
    numpy_picture = np.average(numpy_picture, axis=2)
    numpy_pattern = np.average(numpy_pattern, axis=2)
    correlation = np.fft.ifft2(np.fft.fft2(numpy_picture, s=numpy_picture.shape) * np.fft.fft2(np.rot90(numpy_pattern,2), s = numpy_picture.shape))
    correlation = correlation.real

    picture = Image.open(picture_filename)
    pattern = Image.open(pattern_filename)
    picture_size = (picture.size[1], picture.size[0], 3)
    pattern_size = (pattern.size[1], pattern.size[0], 3)
    numpy_picture = np.array(picture.getdata()).reshape(picture_size)
    numpy_pattern = np.array(pattern.getdata()).reshape(pattern_size)
    numpy_picture = np.average(numpy_picture, axis=2)
    numpy_pattern = np.average(numpy_pattern, axis=2)
    correlation2 = np.fft.ifft2(np.fft.fft2(numpy_picture, s=numpy_picture.shape) * np.fft.fft2(np.rot90(numpy_pattern,2), s = numpy_picture.shape))
    correlation2 = correlation2.real

    correlation2 = correlation2 * correlation



    correlation2 = correlation2/ np.max(correlation2)*255

    return correlation2

letter_to_treshold_map = {
    "a": 240,
    "b": 240,
    "c": 250,
    "d": 250,
    "e": 250,
    "f": 250,
    "g": 250,
    "h": 250,
    "i": 250,
    "j": 245,
    "k": 240,
    "l": 250,
    "m": 253,
    "n": 250,
    "o": 245,
    "p": 250,
    "q": 250,
    "r": 250,
    "s": 250,
    "t": 245,
    "u": 250,
    "v": 250,
    "w": 250,
    "x": 250,
    "y": 250,
    "z": 250
}

letter_width_map = {
    "a": 6,
    "b": 8,
    "c": 6,
    "d": 7,
    "e": 8,
    "f": 5,
    "g": 8,
    "h": 9,
    "i": 4,
    "j": 6,
    "k": 8,
    "l": 4,
    "m": 15,
    "n": 10,
    "o": 10,
    "p": 10,
    "q": 10,
    "r": 7,
    "s": 7,
    "t": 6,
    "u": 9,
    "v": 10,
    "w": 15,
    "x": 9,
    "y": 10,
    "z": 8
}

SPACE_WIDTH = 4


if __name__ == '__main__':
    picture = Image.open("loremipsum2.png")
    result = np.zeros((picture.size[1], picture.size[0]))
    #result = np.array(picture.getdata()).reshape((picture.size[1], picture.size[0], 3))
    #result = np.average(result, axis=2)

    for i in "abcdefghijklmnopqrstuvwxyz":
        correlation = get_correlation("loremipsum2.png", i+".png")
        for j in range(correlation.shape[0]):
            for k in range(correlation.shape[1]):
                if correlation[j][k] > letter_to_treshold_map[i]:
                    result[j][k] = ord(i)

    text = ""

    row_had_letter = False
    pixels_since_last_letter = 0

    for i in range(result.shape[0]):
        row_had_letter = False
        row = ""

        for j in range(result.shape[1]):
            pixels_since_last_letter += 1
            if result[i][j] != 0:
                row_had_letter = True
                if pixels_since_last_letter-letter_width_map[chr(int(result[i][j]))] > SPACE_WIDTH:
                    row += " "
                row += chr(int(result[i][j]))
                pixels_since_last_letter = 0

        if row_had_letter:
            text += row + "\n"

    print(text)

    pass
