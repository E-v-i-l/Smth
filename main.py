"""
INFO
Python 3.11.3
made with albumentations, os, re, opencv
---------------------------------------------------------------------

INPUT
step 1 - input the path to the folder with files to augment
step 2 - input the number of augmented images out of each real one
---------------------------------------------------------------------

OUTPUT
you'll get new files with .jpg extension in the same folder as you inputed in path-variable
also you'll get a .json file for each augmented photo
their names are getting according to this pattern: old_name-n.jpg(.json)
"""

import albumentations as A
import os
import re
import cv2

# getting lists of files divided into 2 groups by their extension
print("please, enter the path to the folder with files to augment")
path = input()
files = os.listdir(path)
patternjson = re.compile(r".*\.json")
patternjpg = re.compile(r".*\.jpg")
json, jpg = [], []
for i in files:
    matchjson = patternjson.match(i)
    matchjpg = patternjpg.match(i)
    if matchjson:
        json += [matchjson.group()]
    if matchjpg:
        jpg += [matchjpg.group()]

# probabilities for augmentation
transform = A.Compose([
    A.Blur(blur_limit=15, always_apply=False, p=0.5),
    A.Defocus(radius=(2.5, 7), alias_blur=(0.1, 0.5), always_apply=False, p=0.5),
    A.ColorJitter(brightness=0.4, contrast=0.4, saturation=0.4, hue=0.4, always_apply=False, p=0.5),
    #A.ChannelShuffle(p=1),
    A.GaussNoise(var_limit=(5.0, 75.0), mean=0, per_channel=True, always_apply=False, p=0.8),
    A.RandomBrightnessContrast(brightness_limit=0.13, contrast_limit=0.15, brightness_by_max=True, always_apply=False),
    A.RandomFog(fog_coef_lower=0.20, fog_coef_upper=0.20, alpha_coef=0.14, always_apply=False, p=0.4),
    A.RandomGamma(gamma_limit=(30, 70), p=0.5),
    A.RandomSnow(p=0.6),
    #A.Affine(rotate=(-360, 360)),
    #A.Affine(rotate=(-360, 360))
]#, keypoint_params=A.KeypointParams(format='xy')
)

# preparing coordinates from json for augmentation step

# прочитать файл в строку -> finditer для определения list of labeles -> finditer для выделения больших подстрок
# (полигон) -> finditer для поиска координат -> (вывод) обрезать лишнее, split по запятой, привести к числам

# может быть стоит дополнить разметку Bounding Boxes'ами (с такими же label как и у точек, которые мы будем обрамлять
# рамкой),чтобы проверять принадлежность точек данному классу

# augmentation
print("please, input the number of copies that you want")
number_of_copies = int(input())
for file in range(len(jpg)):   # going through files
    # reading an image
    print(path + "\\" + jpg[file]) # which photo we are augumenting right now
    image = cv2.imread(path + "\\" + jpg[file])
    image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
    # прочитать новый .json
    for copy in range(number_of_copies):    # get as much copies as we need
        # для .json подать разметку вместе с изображением следующему объекту
        transformed = transform(image=image)
        transformed_image = transformed["image"]
        # принять измененную разметку
        # output
        cv2.imwrite(path + "\\" + jpg[file][:-4] + "-" + str(copy) + ".jpg", transformed_image)
        # для .json тоже
