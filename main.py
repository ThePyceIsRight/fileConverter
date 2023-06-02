from src import img_to_wav
from src import gif_to_imgs
from src import sandbox



if __name__ == '__main__':

    # gif_url = "https://media.tenor.com/tX_T48A14BwAAAAd/khaby-really.gif"
    gif_url = ""

    # sandbox.sandbox(gif_url)
    gif_to_imgs.gif_to_imgs("assets", gif_url)