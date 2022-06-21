from PIL import Image
import os
from multiprocessing import Pool

# Set Params
CURR_DIR = 'data/images/'
NEW_DIR = 'data/images_transformed/'
START_IMAGE_DIR = 100000000
DELTA_ID = 100
N_PROCESSES = 7
CROP_FACTOR = 1.3
IMAGE_RESIZE = 400

def crop_center(pil_img, crop_width, crop_height):
    """Crops image to the center"""
    img_width, img_height = pil_img.size
    return pil_img.crop(((img_width - crop_width) // 2,
                         (img_height - crop_height) // 2,
                         (img_width + crop_width) // 2,
                         (img_height + crop_height) // 2))

def __rename_image(filenames: list):
    filename, new_filename = filenames
    if not filename.endswith(".png"):
        try:
            image = Image.open(filename)
            image = image.convert('RGB')

            height, width = image.size
            # Center crop
            image = crop_center(image, width / CROP_FACTOR, height / CROP_FACTOR)

            # Resize image
            image = image.resize(size=(IMAGE_RESIZE, IMAGE_RESIZE),
                                 resample=Image.NEAREST)
            # Save image
            image.save(new_filename)
            print(filename, '-->', new_filename)
        except Exception as e:
            print(e, 'Not worked for:', filename)


if __name__ == '__main__':
    # Make new folder if not yet created
    try:
        os.mkdir(NEW_DIR)
    except FileExistsError as fe:
        print(fe, NEW_DIR, 'Already Exists')

    filenames = [os.path.join(CURR_DIR, f) for f in os.listdir(CURR_DIR)]

    # Prepare
    new_filenames = [NEW_DIR + str(START_IMAGE_DIR + i * DELTA_ID) + '.png' for i in range(len(filenames))]
    filenames = list(zip(filenames, new_filenames))

    # Call func with MP
    with Pool(processes=N_PROCESSES) as pool:
        pool.map(func=__rename_image, iterable=filenames)
