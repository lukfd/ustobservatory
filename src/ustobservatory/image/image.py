from ustobservatory.lib.convertUtils import convertImageToNdarray


class Image:
    color: str
    image_path: str
    ndarray: None

    def __init__(self, color: str, image_path: str) -> None:
        self.color = color
        self.image_path = image_path
        self.ndarray = convertImageToNdarray(image_path)

    def get_ndarray(self):
        return self.ndarray
