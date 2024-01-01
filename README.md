
# Vision Enhancer

A Pycord bot that will use OpenCV with FSRCNN ML model to enhance any photos with super resolution and other methods of enhancement.




## Installation

```
  pip install -r requirements.txt
```

## Environment Variables

To run this project, you will need to add this variable to your .env file

`BOT_TOKEN=YOUR_DISCORD_BOT_TOKEN`


## Slash Commands Usage

#### Returns your photo upsampled inside an embed

```
  /upscale {factor}
```

| Parameters   | Type       | Description                           |
| :---------- | :--------- | :---------------------------------- |
| `factor` | `string` | **Optional**. The scale factor that you want to upsample your image (min: 2, max: 4, default: 4) |

#### Returns your photo sharpened inside an embed

```
  /sharpen
```

#### Returns your photo denoised inside an embed

```
  /denoise
```
#### Returns your photo with all above methods applied

```
  /full {factor}
```

| Parameters   | Type       | Description                           |
| :---------- | :--------- | :---------------------------------- |
| `factor` | `string` | **Optional**. The scale factor that you want to upsample your image (min: 2, max: 4, default: 4) |





## Authors

- [@Bluh7](https://www.github.com/Bluh7)


## References

 - [Denoising Method](https://docs.opencv.org/3.4/d5/d69/tutorial_py_non_local_means.html)
 - [Super Resolution](https://towardsdatascience.com/deep-learning-based-super-resolution-with-opencv-4fd736678066)
 - [Sharpening Method](https://www.analyticsvidhya.com/blog/2021/08/sharpening-an-image-using-opencv-library-in-python/#:~:text=Common%20sharpening%20kernels%20include%20Laplacian,enhancing%20the%20edges%20and%20details.)
 - [Pycord Docs](https://docs.pycord.dev/en/stable/index.html)

## License

[MIT](https://choosealicense.com/licenses/mit/)

