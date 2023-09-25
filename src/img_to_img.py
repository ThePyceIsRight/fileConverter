from PIL import Image
from pillow_heif import register_heif_opener
import os

register_heif_opener()


def image_to_image(folder_path: str, old_type: str, new_type: str, delete_files: bool = False):
    """
    Converts all images in a folder to the specified image type

    :param folder_path: path to the folder containing images to convert
    :param old_type: the image types that you want to convert FROM
    :param new_type: the type of image to convert images TO
    :param delete_files: set to True to delete converted files
    """

    old_type = old_type.replace(".", "")
    new_type = new_type.replace(".", "")

    print(f"{folder_path}\n{old_type}\n{new_type}")

    # Loop through all files in the directory
    for filename in os.listdir(folder_path):

        # Check if the file is an image
        if filename.endswith(old_type):
            # Open the file
            img = Image.open(f"{folder_path}/{filename}")

            # Save the image in new format
            img.save(f"{folder_path}/{os.path.splitext(os.path.basename(filename))[0]}.{new_type}")

            if delete_files:
                os.remove(f"{folder_path}/{filename}")


if __name__ == '__main__':
    image_to_image("C:/Users/lprice/OneDrive - Range Resources/Desktop/Imagine 2023 Images", "heic", "png")
