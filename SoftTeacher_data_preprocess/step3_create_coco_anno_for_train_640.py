import os 
import csv 
import json
import numpy as np
import pandas as pd

root_dir = 'data/coco'
meta_file = os.path.join(root_dir, 'train.csv')
img_dir = os.path.join(root_dir, 'train2017')
anno_dir = os.path.join(root_dir, 'annotations')
if not os.path.exists(anno_dir):
    os.makedirs(anno_dir)
    
anno_json_file = os.path.join(anno_dir, 'instances_train2017.json')
txt_file = os.path.join(root_dir,'nodule_train_img_list.txt')

coco_data = {'images':[],'annotations':[], 'categories':[]}

df = pd.read_csv(meta_file)

with open(txt_file, "r") as file:
    name_list = [line.rstrip() for line in file]

class NpEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, np.integer):
            return int(obj)
        if isinstance(obj, np.floating):
            return float(obj)
        if isinstance(obj, np.ndarray):
            return obj.tolist()
        return super(NpEncoder, self).default(obj)

def convert_imgName_to_imgId(img_name):
    if img_name[0] == 'n':
        img_id  = int('111'+img_name[1:]) #'111' was used to mark image with nodule object
    elif img_name[0] == 'c':
        img_id  = int('222'+img_name[1:]) #'222' was used to mark image without object
    elif img_name[0] == 'u':
        img_id  = int('333'+img_name[1:]) #'333' was used to mark image without labeling       
    else:
        print("wrong image name: ", img_name)
        img_id = None
    return img_id


"""
construct images for coco_data
"""
height = 640
width = 640
for img_name in name_list:
    img_id = convert_imgName_to_imgId(img_name)    
    file_name = img_name+'.png'
    coco_data['images'].append({'file_name': file_name,
                              'id': img_id,
                              'width': width,
                              'height': height})

def create_coco_annos(rows, img_id):
    annos = []
    len_rows = len(rows)
    r1 = 640.0/1024.0
    for i in range(len_rows):
        cat_id = (rows['label'].values)[i]
        w = (rows['width'].values)[i] 
        h = (rows['height'].values)[i]        
        x1 = (rows['x'].values)[i]   
        y1 = (rows['y'].values)[i]

        #convert image from 1024x1024 to 640x640
        w = float(w * r1)
        h = float(h * r1)
        x1 = float(x1 * r1)
        y1 = float(y1 * r1)

        area = w * h
        x2 = x1 + w
        y2 = y1 + h

        #build unique object id
        obj_id = 100*img_id+i
        
        if cat_id == 1:
            anno = {
                'area': area,
                'bbox': [x1, y1, w, h],
                'category_id': 0,
                'id': obj_id,
                'image_id': img_id,
                'iscrowd': 0,
                # use bbox as segmentation
                'segmentation': [],      
                }
        else:
            anno = {
                'area': 0.0,
                'bbox': [0, 0, 0, 0],
                'category_id': 0,
                'id': obj_id,
                'image_id': img_id,
                'iscrowd': 0,
                # use bbox as segmentation
                'segmentation': [],      
                }
            
        annos.append(anno)

    return annos


"""
construct annotations for coco_data
"""
for name in name_list:  
    img_id = convert_imgName_to_imgId(name)

    file1 = name+".mha"
    rows = df.loc[df['img_name'] == file1] 

    annos = create_coco_annos(rows, img_id)

    for anno in annos:
        coco_data['annotations'].append(anno)


"""
construct categories for coco_data
"""
category1 = {
"id": 0,
"name": 'nodule',
"supercategory": '',
}
coco_data['categories'].append(category1)


"""
save annotation to a json file
"""
with open(anno_json_file, 'w') as f:
    json.dump(coco_data, f, indent=4, cls=NpEncoder)