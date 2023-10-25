from PIL import Image, ImageOps
import numpy as np

if __name__ == '__main__':
    treashold = 1000
    picture = Image.open("fish1.png")
    picture_size = (picture.size[1], picture.size[0], 3)
    numpy_picture = np.array(picture.getdata()).reshape(picture_size)
    fft_picture = np.fft.fft2(numpy_picture, s=numpy_picture.shape[0:2], axes=(0, 1))
    picture_mask = np.abs(fft_picture) > treashold
    fft_picture *= picture_mask



    # high pass filter
    fft_picture = np.fft.fftshift(fft_picture)
    for i in range(fft_picture.shape[0]):
        for j in range(fft_picture.shape[1]):
            buf = (i - fft_picture.shape[0] // 2) ** 2 + (j - fft_picture.shape[1] // 2) ** 2
            if buf < 3**2:
                fft_picture[i, j] = (0,0,0)
    fft_picture = np.fft.ifftshift(fft_picture)


    numpy_picture = np.fft.ifft2(fft_picture, axes=(0, 1)).real
    Image.fromarray(fft_picture.astype(np.uint8)).show()
    Image.fromarray(numpy_picture.astype(np.uint8)).show()
