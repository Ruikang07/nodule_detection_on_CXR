import os 
from pathlib import Path
import shutil

# path of the directory 
src_root = Path("../YOLOv5_data_preprocess/cxr_images/balanced/balanced_node21_png_640/")

src_train_path = os.path.join(src_root, 'images/train') 
src_val_path = os.path.join(src_root, 'images/val') 
src_unlabeled_path = Path("../VinBigData_preprocess/images_with_nodule_png_640/")


dst_root = Path("./data/coco/")
if not os.path.exists(dst_root):
    os.makedirs(dst_root)

dst_train_path = os.path.join(dst_root, 'train2017') 
if not os.path.exists(dst_train_path):
    os.makedirs(dst_train_path)
    
dst_val_path = os.path.join(dst_root, 'val2017') 
if not os.path.exists(dst_val_path):
    os.makedirs(dst_val_path)
    
dst_unlabeled_path = os.path.join(dst_root, 'unlabeled2017') 
if not os.path.exists(dst_unlabeled_path):
    os.makedirs(dst_unlabeled_path)




file_list = os.listdir(src_root)
for f1 in file_list: 
    name, ext = os.path.splitext(f1)
    if ext == '.csv':
        src_file = os.path.join(src_root, f1)  
        dst_file = os.path.join(dst_root, f1)    
        shutil.copyfile(src_file, dst_file)



count = 0  
file_list = os.listdir(src_train_path)
for img in file_list:       
    count += 1    
    src_file = Path(os.path.join(src_train_path, img))
    dst_file = Path(os.path.join(dst_train_path, img)) 
    shutil.copyfile(src_file, dst_file)
    print(count, "  finished train file: ", dst_file)

       
count = 0  
file_list = os.listdir(src_val_path)
for img in file_list: 
    count += 1    
    src_file = Path(os.path.join(src_val_path, img))
    dst_file = Path(os.path.join(dst_val_path, img))    
    shutil.copyfile(src_file, dst_file)
    print(count, "  finished val file: ", dst_file)
    
    
count = 0  
file_list = os.listdir(src_unlabeled_path)
for img in file_list: 
    count += 1    
    src_file = Path(os.path.join(src_unlabeled_path, img))
    dst_file = Path(os.path.join(dst_unlabeled_path, img))   
    shutil.copyfile(src_file, dst_file)
    print(count, "  finished unlabeled file: ", dst_file)  


    