import os
import random

#input
path = input("please, enter the path to the folder with the project\n")
source = input("please, enter the path to the folder with all images\n")

#separating pics
images, files = [], []
files = os.listdir(source)
for i in range(len(files)):
    if files[i][-4:] == ".jpg":
        images += [files[i][0:-4]]

#making all needable folders
os.mkdir(path+"\\dataset")
os.mkdir(path+"\\dataset\\test")
os.mkdir(path+"\\dataset\\train")
os.mkdir(path+"\\new_norm_voc")
os.mkdir(path+"\\new_norm_voc\\ImageSets")
os.mkdir(path+"\\new_norm_voc\\ImageSets\\Segmentation")

#transfering pics
length = len(images)
random.shuffle(images)
nlenght = length
for i in range(int(length*0.2)):
    nlenght -= 1;
    os.replace(source+"\\"+images[i]+".jpg", path+"\\dataset\\test"+"\\"+images[i]+".jpg")
for i in range(int(nlenght-2)):
    os.replace(source+"\\"+images[int(i+length*0.2)]+".jpg", path+"\\dataset\\train"+"\\"+images[int(i+length*0.2)]+".jpg")
nlenght = length

#making text files with names of pics
with open(path+"\\new_norm_voc\\ImageSets\\Segmentation\\test.txt", "w") as file:
    for i in range(int(length * 0.2)):
        nlenght -= 1;
        file.write(images[i]+"\n")
with open(path+"\\new_norm_voc\\ImageSets\\Segmentation\\train.txt", "w") as file:
    for i in range(nlenght - 2):
        file.write(images[i + int(length * 0.2)]+"\n")
with open(path+"\\new_norm_voc\\ImageSets\\Segmentation\\val.txt", "w") as file:
    file.write(images[-1]+"\n")
