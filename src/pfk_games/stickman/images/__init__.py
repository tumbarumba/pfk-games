import os

_image_dir = os.path.dirname(os.path.realpath(__file__))

def image_path(image_file: str) -> str:
    return os.path.join(_image_dir, image_file)
