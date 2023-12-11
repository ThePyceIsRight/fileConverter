from PIL import Image


def convert_to_icon(path, extension):

    output_path = 'output/icon.ico'

    image = Image.open(path)
    image.save(output_path, format='ICO')



