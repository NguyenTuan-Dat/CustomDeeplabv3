import os

list_dir = os.listdir("/Users/ntdat/Tài liệu/Năm 4/Kỳ 2/Các hệ thống đa phương tiện/Data_Camera_SanTennis_Labeled/Labels/")

train_txt = open("/Users/ntdat/Tài liệu/Năm 4/Kỳ 2/Các hệ thống đa phương tiện/Data_Camera_SanTennis_Labeled/train.txt", "w")
valid_txt = open("/Users/ntdat/Tài liệu/Năm 4/Kỳ 2/Các hệ thống đa phương tiện/Data_Camera_SanTennis_Labeled/valid.txt", "w")
str_train = ""
str_valid = ""
for img in list_dir[0:300]:
    str_train += img.split(".")[0] + "\n"
train_txt.write(str_train)
for img in list_dir[300:]:
    str_valid += img.split(".")[0] + "\n"
valid_txt.write(str_valid)
