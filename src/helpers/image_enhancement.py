import cv2
import numpy as np
from PIL import Image
import os
import asyncio
import concurrent.futures


class ImageEnhancement:
    def __init__(self, image: Image.Image, author_id: str) -> None:
        self.image = cv2.cvtColor(np.array(image), cv2.COLOR_RGB2BGR)
        self.author_id = author_id
        self.ml_models = [ml_model for ml_model in os.listdir(
            "./models") if ml_model.endswith(".pb")]

    def __repr__(self) -> str:
        return f"ImageEnhancement(image={self.image}, ml_models={self.ml_models})"

    async def full_enhance(self, scale_factor: int = 4) -> None:
        await self.__async_upsample(scale_factor)
        await self.__async_sharpen()
        await self.__async_denoise()
        self.__save_enhanced_image()

    async def upsample_enhance(self, scale_factor: int = 4) -> None:
        await self.__async_upsample(scale_factor)
        self.__save_enhanced_image()

    async def denoise_enhance(self) -> None:
        await self.__async_denoise()
        self.__save_enhanced_image()

    async def sharpen_enhance(self) -> None:
        await self.__async_sharpen()
        await self.__async_denoise()
        self.__save_enhanced_image()

    def __upsample(self, scale_factor) -> None:
        sr = cv2.dnn_superres.DnnSuperResImpl.create()

        sr.readModel(f"./models/FSRCNN_x{scale_factor}.pb")
        sr.setModel("fsrcnn", scale_factor)

        # Change this to others backends and targets based on your device CPU and GPU
        sr.setPreferableBackend(cv2.dnn.DNN_BACKEND_DEFAULT)
        sr.setPreferableTarget(cv2.dnn.DNN_TARGET_CPU)

        self.image = sr.upsample(self.image)

    def __denoise(self) -> None:
        self.image = cv2.fastNlMeansDenoisingColored(
            self.image, None, 6, 6, 7, 21)

    def __sharpen(self) -> None:
        kernel = np.array([[0, -1, 0], [-1, 5, -1], [0, -1, 0]], np.float32)
        self.image = cv2.filter2D(self.image, -1, kernel)

    async def __async_upsample(self, scale_factor: int = 4) -> None:
        with concurrent.futures.ThreadPoolExecutor() as executor:
            loop = asyncio.get_event_loop()
            await loop.run_in_executor(executor, self.__upsample, scale_factor)

    async def __async_denoise(self) -> None:
        with concurrent.futures.ThreadPoolExecutor() as executor:
            loop = asyncio.get_event_loop()
            await loop.run_in_executor(executor, self.__denoise)

    async def __async_sharpen(self) -> None:
        with concurrent.futures.ThreadPoolExecutor() as executor:
            loop = asyncio.get_event_loop()
            await loop.run_in_executor(executor, self.__sharpen)

    def __save_enhanced_image(self) -> None:
        filename = f"{self.author_id}.png"
        path = f"../results/{filename}"
        cv2.imwrite(path, self.image)
