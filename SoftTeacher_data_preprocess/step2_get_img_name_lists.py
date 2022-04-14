import os 
import csv 


root_dir = 'data/coco'


#For training img name list

img_dir = os.path.join(root_dir, 'train2017')

filename = 'nodule_train_img_list'

txt_file = os.path.join(root_dir,filename+'.txt')
csv_file = os.path.join(root_dir,filename+'.csv')

file_list = os.listdir(img_dir)

 
name_list = []
for file1 in file_list: 
    img_name = os.path.splitext(file1)[0]
    name_list.append([img_name])



with open(txt_file, 'w') as f:
    for item in name_list:
        f.write("%s\n" % item[0])
        
        
with open(csv_file, 'w', newline ='') as f: 
    write = csv.writer(f) 
    write.writerows(name_list) 








#For val img name list

img_dir = os.path.join(root_dir, 'val2017')

filename = 'nodule_val_img_list'

txt_file = os.path.join(root_dir,filename+'.txt')
csv_file = os.path.join(root_dir,filename+'.csv')

file_list = os.listdir(img_dir)

 
name_list = []
for file1 in file_list: 
    img_name = os.path.splitext(file1)[0]
    name_list.append([img_name])



with open(txt_file, 'w') as f:
    for item in name_list:
        f.write("%s\n" % item[0])
        
        
with open(csv_file, 'w', newline ='') as f: 
    write = csv.writer(f) 
    write.writerows(name_list) 









#For unlabeled img name list

img_dir = os.path.join(root_dir, 'unlabeled2017')

filename = 'nodule_unlabeled_img_list'

txt_file = os.path.join(root_dir,filename+'.txt')
csv_file = os.path.join(root_dir,filename+'.csv')

file_list = os.listdir(img_dir)

 
name_list = []
for file1 in file_list: 
    img_name = os.path.splitext(file1)[0]
    name_list.append([img_name])



with open(txt_file, 'w') as f:
    for item in name_list:
        f.write("%s\n" % item[0])
        
        
with open(csv_file, 'w', newline ='') as f: 
    write = csv.writer(f) 
    write.writerows(name_list) 