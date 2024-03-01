import cv2
import numpy as np
import multiprocessing as mp
from PIL import Image, ImageSequence, GifImagePlugin
import rembg
import os
import pprint
from src.gif_info import interrogate


def change_frame_duration(img, frame_duration=50):
    """
    Calculates the area of a rectangle.

    :param img: the gif to edit frame duration.
    :type img: PIL.Image, numpy.ndarray, or string path.
    :param frame_duration: new duration of each frame in the gif
    :return: None
    :rtype: None
    """
    # GifImagePlugin.LOADING_STRATEGY = GifImagePlugin.loading.RGB_AFTER_FIRST
    print(f'img type is: {type(img)}')
    if isinstance(img, str):
        print('input passed as string path')
        valid_path = os.path.exists(img)
        if not valid_path:
            print("path is not valid")
            return None
        else:
            print("path is valid")
        gif_PIL = Image.open(img)
    elif isinstance(img, numpy.ndarray):
        gif_PIL = Image.fromarray(img)
    elif isinstance(img, Image.Image):
        gif_PIL = img
    else:
        print("invalid image type passed. valid options are: PIL.Image, numpy.ndarray, or a valid string path to gif.")
        return None

    frames = []

    frame_count = gif_PIL.n_frames

    print(f'frame count: {frame_count}')

    gif_info_dict = interrogate(gif_PIL)

    exit(0)

    for i in range(0, frame_count):
        print(f'==================== frame number: {i}')

        gif_PIL.seek(i)
        frame_data = GifImagePlugin.getdata(gif_PIL)
        frame_header = GifImagePlugin.getheader(gif_PIL)

        # Convert it to a NumPy array
        gif_np = np.asarray(gif_PIL)
        # Convert RGB to BGR (OpenCV format)
        gif_cv2 = cv2.cvtColor(gif_np, cv2.COLOR_RGB2BGR)

        h, w, channels = gif_cv2.shape

        print(f'frame header:')
        pprint.pprint(frame_header)
        print(f'frame data:')
        pprint.pprint(frame_data)
        print(f'img height x width: ({h},{w})')
        print(f'number of channels: {channels}')
        print(f'img dtype: {gif_np.dtype}')

        frames.append(gif_PIL)


    # Save the frames as a new GIF
    gif_PIL[0].save('new.gif', save_all=True, append_images=frames[1:], optimize=False, duration=frame_duration, loop=0)