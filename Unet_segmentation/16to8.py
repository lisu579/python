
import os

import cv2
import numpy as np

path=r"D:\STUDY\data\test\ML\validation1"
save_path=r"D:\STUDY\data\test\ML\val1"
for name in os.listdir(path):
    if name.split('.')[-1]=='tif':
        new_path=os.path.join(path,name)
        uint16_img = cv2.imread(new_path,-1)
        #uint16_img1 = Image.open(new_path)
        #Image_p=Image.fromarray(uint16_img)
        uint16_img -= uint16_img.min()
        uint16_img = uint16_img / (uint16_img.max() - uint16_img.min())
        uint16_img *= 255
        new_uint16_img = uint16_img.astype(np.uint8)

        # M=cv2.getRotationMatrix2D((uint16_img.shape[0]/modis_preprocess,uint16_img.shape[arcpy]/modis_preprocess),45,0.8)
        # uint16_img=cv2.warpAffine(uint16_img,M,(cols, rows))

        basename=name.split('.')[0]
        # uint16_img=Image.fromarray(uint16_img)
        # uint16_img.save(os.path.join(save_path,basename)+'.png')

        cv2.imwrite(os.path.join(save_path,basename)+'.tif', new_uint16_img)
        print(os.path.join(save_path,name))
        # cv2.waitKey(0)
