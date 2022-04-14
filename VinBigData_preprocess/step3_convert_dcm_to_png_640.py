import os 
from pathlib import Path
import numpy as np
from PIL import Image
import opencxr
from opencxr.utils.file_io import read_file

src_img_path = Path('images_with_nodule/train')
dst_img_path_640 = Path('images_with_nodule_png_640')

src_file_list = os.listdir(src_img_path)
if src_file_list == []: 
    print("No files found in "+src_img_path) 
    
if not os.path.exists(dst_img_path_640):
    os.makedirs(dst_img_path_640)


cxr_std_algorithm = opencxr.load(opencxr.algorithms.cxr_standardize)

count = 0
for file in src_file_list:
    count += 1
    name, ext = os.path.splitext(file) 

    png_file_name = name+'.png'
    
    full_cxr_file_path = os.path.join(src_img_path, file)

    # read a file (supports dcm, mha, mhd, png)
    img_np, spacing, _ = read_file(full_cxr_file_path)
    # Do standardization of intensities, cropping to lung bounding box, and resizing to 1024
    std_img, new_spacing, size_changes = cxr_std_algorithm.run(img_np, spacing)

    # rotate the image 90 degree clockwise
    img = Image.fromarray(((np.asarray(std_img)/np.max(std_img))*255).astype(np.uint8), 'L') 
    angle = -90
    img = img.rotate(angle) 
    
    # create 640x640 png image file
    newsize = (640, 640)
    img = img.resize(newsize)
    img_file = os.path.join(dst_img_path_640, png_file_name)
    img.save(img_file) 
    print(count, "  finished file: ", img_file)
