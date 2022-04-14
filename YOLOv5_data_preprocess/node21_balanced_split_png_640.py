import os
import numpy as np
import pandas as pd
import random
import shutil
import SimpleITK as sitk
from PIL import Image
import imageio
from matplotlib import pyplot as plt
import fnmatch

src_path = 'cxr_images/proccessed_data/'
src_image_path = os.path.join(src_path , 'images/')

dst_path = 'cxr_images/balanced/balanced_node21_png_640/'
if not os.path.exists(dst_path):
    os.makedirs(dst_path)


#prepare images directory

image_path = os.path.join(dst_path, 'images/')
if not os.path.exists(image_path):
    os.makedirs(image_path)
 
image_train_path = os.path.join(image_path, 'train/')
if not os.path.exists(image_train_path):
    os.makedirs(image_train_path)
    
image_val_path = os.path.join(image_path, 'val/')
if not os.path.exists(image_val_path):
    os.makedirs(image_val_path)    


#prepare labels directory 
 
label_path = os.path.join(dst_path, 'labels/')
if not os.path.exists(label_path):
    os.makedirs(label_path)
    
label_train_path = os.path.join(label_path, 'train/')
if not os.path.exists(label_train_path):
    os.makedirs(label_train_path)
    
label_val_path = os.path.join(label_path, 'val/')
if not os.path.exists(label_val_path):
    os.makedirs(label_val_path)  


#prepare bk directory 

bk_path = 'cxr_images/balanced/unused/'
if not os.path.exists(bk_path):
    os.makedirs(bk_path)

image_bk_path = os.path.join(bk_path, 'images/')
if not os.path.exists(image_bk_path):
    os.makedirs(image_bk_path)  
    
label_bk_path = os.path.join(bk_path, 'labels/')
if not os.path.exists(label_bk_path):
    os.makedirs(label_bk_path) 
    
    

#create training and validation image file list

image_list = os.listdir(src_image_path)

pattern_n = 'n*.mha'
pattern_c = 'c*.mha'

n_start_list = fnmatch.filter(image_list, pattern_n)
c_start_list = fnmatch.filter(image_list, pattern_c)

len_n = len(n_start_list)

c_start_list_1 = random.sample(c_start_list,len_n)
c_start_list_2 = list(set(c_start_list) - set(c_start_list_1))

print("image numbers with nodules = ", len(n_start_list))
print("image numbers not used = ", len(c_start_list_2))

len_n_val = int(0.2 * len_n)
val_list_n = random.sample(n_start_list,len_n_val)
val_list_c = random.sample(c_start_list_1,len_n_val)

full_list = n_start_list + c_start_list_1
val_list = val_list_n + val_list_c
train_list = list(set(full_list) - set(val_list))

random.shuffle(train_list)
random.shuffle(val_list)


#create metafile for training and validation image files

meta_file = os.path.join(src_path, 'metadata.csv')
meta_df = pd.read_csv(meta_file)
meta_df.drop('Unnamed: 0', axis=1, inplace=True)

meta_train = meta_df.loc[meta_df['img_name'].isin(train_list)]  
file1 = os.path.join(dst_path, 'train.csv')
meta_train.to_csv(file1, index=False)

meta_val = meta_df.loc[meta_df['img_name'].isin(val_list)]
file2 = os.path.join(dst_path, 'val.csv')
meta_val.to_csv(file2, index=False)

meta_bk = meta_df.loc[meta_df['img_name'].isin(c_start_list_2)]
file3 = os.path.join(bk_path, 'bk.csv')
meta_val.to_csv(file3, index=False)



def create_png_file(name, src_file, img_path):
    img = sitk.ReadImage(src_file)
    img = sitk.GetArrayFromImage(img)
    
    # Creates PIL image
    img = Image.fromarray(((np.asarray(img)/np.max(img))*255).astype(np.uint8), 'L') 
    newsize = (640, 640)
    img = img.resize(newsize)
    
    img_file = os.path.join(img_path, name+'.png' )
    img.save(img_file)  
    
    return   
    
    

def create_label_file(rows, name, label_path):
    lines = []
    len_rows = len(rows)
    for i in range(len_rows):
        label = (rows['label'].values)[i]
        width = (rows['width'].values)[i] 
        height = (rows['height'].values)[i]        
        x_min = (rows['x'].values)[i]   
        y_min = (rows['y'].values)[i]
        
        x_mid = x_min + 0.5*width
        y_mid = y_min + 0.5*height
          
        x = x_mid/1024.
        y = y_mid/1024.
        w = width/1024.
        h = height/1024.
        
        if label == 1:               
            #yolov5 label file: <class> <x> <y> <width> <height>
            line = [0, x, y, w, h]
            lines.append(line)
            
    #write yolov5 label file 
    file_label = os.path.join(label_path, name+'.txt' )
    if label == 1:
        with open(file_label, 'w') as f:
            for line in lines:
                f.writelines(["%s " % item  for item in line])
                f.write('\n')
    else:
        open(file_label, 'w').close()
    
    return


count = 0    
#create unused data
print("\n\n\nstart creating unused data")
for file in c_start_list_2:
    name, ext = os.path.splitext(file) 
    src_file = os.path.join(src_image_path, file)
    count += 1
    print(count, "   src_file  = ", src_file)
    #create unused images
    create_png_file(name, src_file, image_bk_path)  
    
    #write yolov5 label file 
    file_label = os.path.join(label_bk_path, name+'.txt' )
    open(file_label, 'w').close()
    
    
#create training data
print("\n\n\nstart creating training data")
for file in train_list: 
    name, ext = os.path.splitext(file) 
    src_file = os.path.join(src_image_path, file)
    count += 1
    print(count, "   src_file  = ", src_file)
    #create training images
    create_png_file(name, src_file, image_train_path)  
    #create training labels
    rows = meta_train.loc[meta_train['img_name'] == file]     
    create_label_file(rows, name, label_train_path)

    
#create validation data
print("\n\n\nstart creating validation data")
for file in val_list:
    name, ext = os.path.splitext(file) 
    src_file = os.path.join(src_image_path, file)
    count += 1
    print(count, "   src_file  = ", src_file)
    #create validation images
    create_png_file(name, src_file, image_val_path)  
    #create validation labels
    rows = meta_val.loc[meta_val['img_name'] == file]     
    create_label_file(rows, name, label_val_path)
    


