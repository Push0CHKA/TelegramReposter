from PIL import Image


def crop_img(path: str):
    """Обрезка изображений"""
    im = Image.open(path)
    im = im.crop((0,
                  30,
                  im.width,
                  im.height - 30))
    im.save(path)
