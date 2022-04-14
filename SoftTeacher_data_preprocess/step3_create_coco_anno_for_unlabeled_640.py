import os 
import csv 
import json

root_dir = 'data/coco'

img_dir = os.path.join(root_dir, 'unlabeled2017')

anno_dir = os.path.join(root_dir, 'annotations')

if not os.path.exists(anno_dir):
    os.makedirs(anno_dir)
    
anno_json_file = os.path.join(anno_dir, 'instances_unlabeled2017.json')


file_list = os.listdir(img_dir)

name_list = []
for file1 in file_list: 
    img_name = os.path.splitext(file1)[0]
    name_list.append(img_name)


coco_data = {'images':[],'annotations':[], 'categories':[]}


"""
construct images for coco_data
"""
height = 640
width = 640
for name in name_list:
    if name[0] == 'c':
        img_id  = int('222'+name[1:]) #'222' was used to mark image without object
    elif name[0] == 'u':
        img_id  = int('333'+name[1:]) #'333' was used to mark image without labeling
    else:
        print("wrong image name: ", name)
        exit(0)
        
    img_name = name+'.png'
    # 添加图像的信息到dataset中
    coco_data['images'].append({'file_name': img_name,
                              'id': img_id,
                              'width': width,
                              'height': height})
                              

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
    json.dump(coco_data, f, indent=4)