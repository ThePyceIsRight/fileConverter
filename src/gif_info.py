import cv2
import numpy as np
import multiprocessing as mp
from PIL import Image, ImageSequence, GifImagePlugin
import rembg
import os
import pprint


def interrogate(img, print_header=False,print_frame_data=False):
    """
    Prints various data points about a gif image to the console. Returns the elements as a dict.

    :param img: the gif to edit frame duration.
    :type img: PIL.Image, numpy.ndarray, or string path.
    :return: gif_info_dict
    :rtype: dict
    """

    # determine / handle input image type
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
    elif isinstance(img, np.ndarray):
        gif_PIL = Image.fromarray(img)
    elif isinstance(img, Image.Image):
        gif_PIL = img
    else:
        print("invalid image type passed. valid options are: PIL.Image, numpy.ndarray, or a valid string path to gif.")
        return None

    # get frame count
    frame_count = gif_PIL.n_frames
    print(f'frame count: {frame_count}')

    gif_PIL.seek(0)

    # extract header info
    frame_header = GifImagePlugin.getheader(gif_PIL)

    # convert to np and cv2 to grab additional info
    gif_np = np.asarray(gif_PIL)
    gif_cv2 = cv2.cvtColor(gif_np, cv2.COLOR_RGB2BGR)
    h, w, channels = gif_cv2.shape
    gif_type = gif_PIL.info["version"]
    pallete_mode = gif_PIL.palette.mode
    gif_mode = gif_PIL.mode
    pallete_rawmode = gif_PIL.palette.rawmode
    pallete_colors = gif_PIL.palette.colors

    # print gif info
    print(f'gif type: {gif_type}')
    print(f'height x width: ({h},{w})')
    print(f'number of channels: {channels}')
    print(f'img dtype: {gif_np.dtype}')
    if print_header:
        print(f'frame header:')
        pprint.pprint(frame_header)
    if print_frame_data:
        print(f'raw frame data:')
        frame_data = GifImagePlugin.getdata(gif_PIL)
        pprint.pprint(frame_data)

    # assign gif info to dict
    gif_info_dict = {'gif_type': gif_type,
                     'height': h,
                     'width': w,
                     'channels': channels,
                     'dtype': gif_np.dtype,
                     'gif_format': gif_type,
                     'pallete_mode': pallete_mode,
                     'pallete_rawmode': pallete_rawmode,
                     'palette_colors': pallete_colors,
                     'gif_mode': gif_mode}
    return gif_info_dict
