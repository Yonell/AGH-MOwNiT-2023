from PIL import Image, ImageOps
import numpy as np

if __name__ == '__main__':
    treashold = 100000
    picture = Image.open("school.jpg")
    pattern = Image.open("fish1.png")
    #picture = ImageOps.invert(picture)
    #pattern = ImageOps.invert(pattern)
    picture_size = (picture.size[1], picture.size[0], 3)
    pattern_size = (pattern.size[1], pattern.size[0], 3)
    numpy_picture = np.array(picture.getdata()).reshape(picture_size)
    numpy_pattern = np.array(pattern.getdata()).reshape(pattern_size)
    numpy_picture = np.average(numpy_picture, axis=2)
    numpy_pattern = np.average(numpy_pattern, axis=2)
    fft_picture = np.fft.fft2(numpy_picture, s=numpy_picture.shape)
    fft_pattern = np.fft.fft2(np.rot90(numpy_pattern, 2), s=numpy_picture.shape)
    picture_mask = np.abs(fft_picture) > treashold
    pattern_mask = np.abs(fft_pattern) > 200
    fft_picture *= picture_mask
    fft_pattern *= pattern_mask



    # high pass filter
    '''fft_picture = np.fft.fftshift(fft_picture)
    fft_pattern = np.fft.fftshift(fft_pattern)
    for i in range(fft_picture.shape[0]):
        for j in range(fft_picture.shape[1]):
            if (i - fft_picture.shape[0] // 2) ** 2 + (j - fft_picture.shape[1] // 2) ** 2 < 3**2:
                fft_picture[i, j] = 0
                fft_pattern[i, j] = 0
    fft_picture = np.fft.ifftshift(fft_picture)
    fft_pattern = np.fft.ifftshift(fft_pattern)'''



    correlation = np.fft.ifft2(fft_picture * fft_pattern).real
    correlation = correlation / np.max(correlation) * 255
    numpy_picture = np.array(ImageOps.invert(picture).getdata()).reshape(picture_size)
    for i in range(correlation.shape[0]):
        for j in range(correlation.shape[1]):
            if correlation[i, j] > 150:
                for k in range(14):
                    numpy_picture[i - k, j] = np.array([255, 0, 0])
                    numpy_picture[i - k, j - 13] = np.array([255, 0, 0])
                    numpy_picture[i - 13, j - k] = np.array([255, 0, 0])
                    numpy_picture[i, j - k] = np.array([255, 0, 0])

    #Image.fromarray(np.fft.ifft2(fft_picture).astype(np.uint8)).show()
    #Image.fromarray(np.fft.ifft2(fft_pattern).astype(np.uint8)).show()
    #Image.fromarray(correlation.astype(np.uint8)).show()
    ImageOps.invert(Image.fromarray(numpy_picture.astype(np.uint8))).show()
