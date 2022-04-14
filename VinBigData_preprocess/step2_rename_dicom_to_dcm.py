import os 
from pathlib import Path
import shutil

# path of the directory 
src_img_path = Path("images_with_nodule/train")

src_file_list = os.listdir(src_img_path)
if src_file_list == []: 
    print("No files found in "+src_img_path) 

count = 0  

for f in src_file_list: 
    count += 1    
    src_img = os.path.join(src_img_path, f)  
    new_name = 'u'+'{0:04d}'.format(count) + '.dcm' 
    dst_img = os.path.join(src_img_path, new_name)    
    os.rename(src_img, dst_img)
    print(count, "  finished file: ", dst_img)
    
