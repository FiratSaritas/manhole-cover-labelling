<img src="https://img.shields.io/badge/status-online-green" />

# manhole-cover-labelling

This repository labels images of manhole covers into 13 different classes:
  - Rost/Strassenrost
  - Vollguss/Pickelloch belueftet
  - Gussbeton/Pickelloch geschlossen
  - Vollguss/Pickelloch geschlossen
  - Gussbeton/Pickelloch belueftet
  - Vollguss/Handgriff geschlossen
  - Gussbeton/Handgriff seitlich
  - Rost/Einlauf rund
  - Rost/Strassenrost gewoelbt
  - Vollguss/Aufklappbar
  - Gussbeton/Handgriff mitte
  - Vollguss/Handgriff geschlossen, verschraubt
  - Andere/-
  

## Installation

1. Clone project locally 

```bash
git clone git@github.com:FiratSaritas/manhole-cover-labelling.git
```

2. Save your images that you want to label in the folder `./data/images` 

3. Install required packages

Preferably you create a new enviorment (conda environment is also possible).

```bash
pip install -r requirements.txt
```

## Usage

1. First we need to transform the images and run the following code to do it:
```bash
python program/prepare_images.py
```

2. After that we can start the webbrowser and label our images:
```bash
python main.py
```

Output:
  - When you have labeled all images, you get a csv file `./data/labels.csv`


## Guide -Tips
  - You can save the current status at any time.
  - It saves automatically after 10 images.
  - If there is an error it may be because the image has an issue.
  - If you want to start from scratch, just delete the file `./data/labels.csv` and folder `./data/images_transformed`
  - The images in the folder `./data/images_transformed` can be used to train the model with the repository [manhole-cover-classification](https://github.com/FiratSaritas/manhole-cover-classification)

## Credits

This is a continuation of the repository [labelly](https://github.com/SimonStaehli/labelly) and the actual work was created on the other repository.
