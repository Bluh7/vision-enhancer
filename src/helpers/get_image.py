import requests
from PIL import Image


class GetImage:
    def __init__(self) -> None:
        pass

    def get_image(self, image_url: str) -> Image.Image:
        image = Image.open(requests.get(image_url, stream=True).raw)
        return image
