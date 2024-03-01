from PIL import Image
from pillow_heif import register_heif_opener
import os

register_heif_opener()


def image_to_image(folder_path: str, old_type: str, new_type: str, delete_files: bool = False, compress_img: bool = True, new_size: int = 1500):
    """
    Converts all images in a folder to the specified image type

    :param folder_path: path to the folder containing images to convert
    :param old_type: the image types that you want to convert FROM
    :param new_type: the type of image to convert images TO
    :param delete_files: set to True to delete converted files
    """

    print(f"/nbeginning type conversion process. delete file after conversion = {delete_files}")

    old_type = old_type.replace(".", "")
    new_type = new_type.replace(".", "")

    print(f"/nchosen params:/n    path: {folder_path}/n    from type: {old_type}/n    to type: {new_type}/n    delete "
          f"original: {delete_files}/n    compress image: {compress_img}/n    new size: {new_size}/n")

    i = 0

    # Loop through all files in the directory
    for filename in os.listdir(folder_path):

        # Check if the file is an image
        if filename.endswith(old_type):
            status_msg = ""

            # Open the file
            img = Image.open(f"{folder_path}/{filename}")

            # New img name
            str_new_name = f"{folder_path}/{os.path.splitext(os.path.basename(filename))[0]}.{new_type}"

            # Save the image in new format
            if compress_img:
                width, height = img.size
                if width > new_size:
                    ratio = new_size / width
                    height = int(height * ratio)
                    img = img.resize((new_size, height))
                    status_msg = "resized, "
                img =  img.convert("P", palette=Image.ADAPTIVE, colors=256)
                status_msg = f"{status_msg}compressed, "
                img.save(str_new_name)
            else:
                img.save(str_new_name)

            if delete_files:
                os.remove(f"{folder_path}/{filename}")

            i = i + 1

            if delete_files:
                print(f"{filename} {status_msg}converted and deleted")
            else:
                print(f"{filename} {status_msg}converted")

            status_msg = ""

    print(f"/nprocess complete: {i} pictures converted from {old_type} to {new_type}")


if __name__ == '__main__':
    image_to_image(folder_path="C:/Users/lprice/OneDrive - Range Resources/Desktop/delete/New folder",
                   old_type="webp",
                   new_type="png",
                   delete_files=False,
                   compress_img=False,
                   new_size=1500)
