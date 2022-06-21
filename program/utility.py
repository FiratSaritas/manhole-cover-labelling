import pandas as pd
import os
from PIL import Image
import numpy as np

def load_image_df(data_path: str):
    """
    Loads dataframe

    Parameters
    ----------
    data_path: path of dataframe

    Returns
    -------
    pd.DataFrame
    """
    return pd.read_csv(data_path)

def load_image(image_path: str, image_name: str):
    """
    Loads image with PIL

    Parameters
    ----------
    image_path: path where image is stored
    image_name: name of the stored image within image_path

    Returns
    -------
    PIL.Image-object
    """
    image_path = os.path.join(image_path, image_name)
    return Image.open(image_path)

def create_test_csv(image_path: str, csv_path: str, duplicated_label_factor: float = None):
    """
    Creates CSV. This function is used for testing purposes as well as in the first
    labelling iteration when no csv yet exists.

    No return of a value. Insteads saves created DF as CSV.

    Parameters
    ----------
    image_path: path to all the images (folder)
    csv_path: path where the csv should be created.
    duplicated_label_factor: Defines how many percent of duplicated will be added to the labelling

    Returns
    -------
    Saves Created Dataframe as CSV.
    """
    images = np.array(os.listdir(image_path))
    # Join duplicated labels
    if duplicated_label_factor:
        amount_duplicates = int(images.shape[0] * duplicated_label_factor)
        images = np.append(arr=images,
                           values=np.random.permutation(images)[:amount_duplicates],
                           axis=0)
    none_list = [None for _ in range(len(images))]
    df = pd.DataFrame(data={'image': images,
                            'type': none_list,
                            'subtype': none_list})
    # Resample Dataframe
    df = df.sample(frac=1)
    # Save to csv
    df.to_csv(csv_path, index=False)