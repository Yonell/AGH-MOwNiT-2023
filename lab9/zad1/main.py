from PIL import Image, ImageOps
import numpy as np



if __name__ == '__main__':
    picture = Image.open("galia.png")
    pattern = Image.open("galia_e.png")
    picture = ImageOps.invert(picture)
    pattern = ImageOps.invert(pattern)
    picture_size = (picture.size[1], picture.size[0], 3)
    pattern_size = (pattern.size[1], pattern.size[0], 3)
    numpy_picture = np.array(picture.getdata()).reshape(picture_size)
    numpy_pattern = np.array(pattern.getdata()).reshape(pattern_size)
    numpy_picture = np.average(numpy_picture, axis=2)
    numpy_pattern = np.average(numpy_pattern, axis=2)
    correlation = np.fft.ifft2(np.fft.fft2(numpy_picture, s=numpy_picture.shape) * np.fft.fft2(np.rot90(numpy_pattern,2), s = numpy_picture.shape))
    #correlation = np.abs(correlation)
    correlation = correlation.real
    correlation = correlation/ np.max(correlation)*255
    #correlation = np.vectorize(lambda x: 255 if x > 240 else 0)(correlation)
    Image.fromarray(correlation).show()
    numpy_picture = np.array(ImageOps.invert(picture).getdata()).reshape(picture_size)
    result = numpy_picture.copy()
    amount = 0
    for i in range(numpy_picture.shape[0]):
        for j in range(numpy_picture.shape[1]):
            if correlation[i,j] > 240:
                for k in range(14):
                    result[i - k,j] = np.array([255,0,0])
                    result[i - k, j - 13] = np.array([255, 0, 0])
                    result[i - 13, j - k] = np.array([255, 0, 0])
                    result[i, j - k] = np.array([255, 0, 0])
                amount += 1
                pass
    Image.fromarray(result.astype(np.uint8)).show()
    print("Amount of paterns in an image: " + str(amount))
    pass
