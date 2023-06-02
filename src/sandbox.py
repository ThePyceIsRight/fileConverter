#====================================================================================
#====================================================================================
# This python module is just for testing ideas and is not necessary for the package
# to run.
#====================================================================================
#====================================================================================

from PIL import Image, ImageSequence
import requests
from io import BytesIO


def sandbox(gif_url):
    response = requests.get(gif_url)
    with Image.open(BytesIO(response.content)) as im:
        im.seek(1)  # skip to the second frame
        try:
            while 1:
                im.seek(im.tell() + 1)
                # do something to im
        except EOFError:
            pass  # end of sequence
    im.show()