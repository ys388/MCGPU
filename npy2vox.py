import numpy as np
from os.path import join as ospj
import pydicom
import shutil
import matplotlib.pyplot as plt
from PIL import Image
import codecs
from HU2npy import hu2npy
import os
def txt_phantom(f,phantom):
    line = f.readline()
    while line:
        if line[0] != '#' and line != '\n' and line.split() != []:
            line_temp = line.split()
            phantom[int(line_temp[0])]['organ_id'] = int(line_temp[0])
            phantom[int(line_temp[0])]['mc_material'] = int(line_temp[2])
            phantom[int(line_temp[0])]['density'] = float(line_temp[3])
        line = f.readline()
    f.close()
    return phantom

def mc_de_id(phantom_, mayo_npy, channels, height, width):
    vox_length = channels * height * width
    vox_list = np.zeros((vox_length, 3), dtype=np.float32)
    for c in range(channels):
        print(c)
        for h in range(height):
            for w in range(width):
                voxel = w + h * width + c * width * height
                # voxel_value = img[channels-c-1][w][h]
                voxel_value = int(mayo_npy[c][h][width - w - 1])
                # phantom_, voxel_value = amend_phantom(phantom_, voxel_value)
                vox_list[voxel][0] = phantom_[voxel_value]['mc_material']
                vox_list[voxel][1] = phantom_[voxel_value]['density']
                vox_list[voxel][2] = phantom_[voxel_value]['organ_id']
    return vox_list



if '__name__ == __main__':

    #dicom 转换成HU
    #先运行prep文件
    #HU 转换成npy,保存为'1.npy'
    patient = 'L506'
    data_path = './mayo_' + patient
    npyfiles = 'npyfiles'
    hu2npy(data_path,npyfiles)
    # ##加载phantom
    PhantomType = np.dtype(
    {'names': ['organ_id', 'organ_name', 'mc_material', 'density'], 'formats': ['i', 'S32', 'i', 'f']})
    #
    phantom = np.array([(0, 'zero', 0, 0.)] * 150, dtype=PhantomType)


    mayo_npy = np.load(ospj(data_path,'1.npy'))
    plt.imshow(mayo_npy[159], 'gray')
    plt.show()
    plt.imshow(mayo_npy[:,256,:], 'gray')
    plt.show()
    plt.imshow(mayo_npy[:,:,256], 'gray')
    plt.show()
    table_path = 'D:/CT_Project/MCGPU/table.txt'
    save_vox_path = os.path.join(ospj(data_path,'mayo_vox.txt'))
    channels, height, width = mayo_npy.shape[0], mayo_npy.shape[1], mayo_npy.shape[2]
    #
    #
    # ##加载table里的material,density
    table_file = codecs.open(table_path)
    phantom_ = txt_phantom(table_file, phantom)

    ##存储 mayo_vox,写入material_id、density、organ_id
    mayo_vox = mc_de_id(phantom_, mayo_npy, channels, height, width)
    np.savetxt(save_vox_path, mayo_vox, fmt='%d %.3f %d')

    ##test



