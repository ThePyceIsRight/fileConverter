import gradio as gr
import cv2
import numpy as np


def view_im(image):
    # Show the image (provide a window name)
    cv2.imshow('image_window', image)
    cv2.waitKey(0)
    cv2.destroyAllWindows()


def handler():
    image = cv2.imread("C:/Users/lprice/Downloads/oil-rig.jpg")
    mask = cv2.imread("C:/Users/lprice/Downloads/mask.jpg")

    mask_blurred = cv2.GaussianBlur(mask, (99, 99), 0)

    image_blurred = cv2.GaussianBlur(image, (99, 99), 0)

    mask_blurred_3chan = mask_blurred.astype('float') / 255.

    img = image_blurred.astype('float') / 255.
    bg = image.astype('float') / 255.

    out = bg * (1 - mask_blurred_3chan) + img * mask_blurred_3chan

    view_im(out)

    return out


# handler()


def blur_mask(data_dict, blur_kernel, feather_kernel):
    image = data_dict["image"]
    mask = data_dict["mask"]
    mask = mask[:, :, :3]

    mask_blurred = cv2.GaussianBlur(mask, (feather_kernel, feather_kernel), 0)

    image_blurred = cv2.GaussianBlur(image, (blur_kernel, blur_kernel), 0)

    mask_blurred_3dim = mask_blurred.astype('float') / 255.

    top_image = image_blurred.astype('float') / 255.
    bottom_image = image.astype('float') / 255.

    final_image = bottom_image * (1 - mask_blurred_3dim) + top_image * mask_blurred_3dim

    return final_image


with gr.Blocks() as demo:
    with gr.Row():
        image_input = gr.Image(tool="sketch", label="input image", value="C:/Users/lprice/Downloads/Oil-rig.jpg")
        image_output = gr.Image(label="output image")

    slider_blur = gr.Slider(value=99, label="Blur intensity")
    slider_feather = gr.Slider(value=99, label="Feather size")

    button = gr.Button("process")

    button.click(fn=blur_mask,
                 inputs=[image_input, slider_blur, slider_feather],
                 outputs=image_output)

demo.launch()
