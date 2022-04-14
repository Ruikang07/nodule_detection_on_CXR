import os
import pandas as pd
import numpy as np
from zipfile import ZipFile

#the path that hold the original meta info file train.csv from the dataset
root_path = './'
nodule_img_path = os.path.join(root_path,'images_with_nodule')

#the path to downloaded vinbigdata-chest-xray-abnormalities-detection dataset file
img_zip_file = 'G:/dataset/Chest_X-ray_dataset/vinbigdata-chest-xray-abnormalities-detection.zip'

train_meta_file = os.path.join(root_path,'train.csv')
nodule_img_meta_file = os.path.join(root_path,'VinBigData_with_nodule.csv')


if not os.path.exists(root_path):
    os.makedirs(root_path)

if not os.path.exists(nodule_img_path):
    os.makedirs(nodule_img_path)

df_train = pd.read_csv(train_meta_file)
print("len(df_train) = ", len(df_train))

list_unique_image_id = df_train.image_id.unique()
print("len(list_unique_image_id) = ", len(list_unique_image_id))

object_number_per_class = df_train[['class_id', 'class_name', 'rad_id']].\
                            groupby(['class_id', 'class_name']).\
                            count().rename(columns={'rad_id': 'Number of records'})
print("object_number_per_class = ", object_number_per_class)

df_nodule = df_train.loc[df_train['class_name'] == 'Nodule/Mass']
print("nodule object number = ", len(df_nodule))

list_unique_nodule_image_id = df_nodule.image_id.unique()
print("image file number with nodules =  = ", len(list_unique_nodule_image_id))

#save the meta file for images with nodules
df_nodule.to_csv(nodule_img_meta_file)

count = 0
#extract the image files with nodules from the big zip file
with ZipFile(img_zip_file, 'r') as zipObj:
    for image_id in list_unique_nodule_image_id:
        fileName = image_id+'.dicom'
        file_full_path = 'train/'+fileName
        count += 1
        print(count, "  file_full_path = ",file_full_path)
        zipObj.extract(file_full_path, nodule_img_path)
