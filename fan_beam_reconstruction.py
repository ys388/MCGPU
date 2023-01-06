import codecs
import numpy as np
import matplotlib.pyplot as plt
import os
from PIL import Image
from reconstruct_metrics import Sinogram2Img
from skimage.metrics import structural_similarity as ssim
from skimage.metrics import peak_signal_noise_ratio as psnr

class init:
    def __init__(self):
        self.param = {}

        # image
        self.param['nx'] = 340
        self.param['ny'] = 340

        self.param['image_pixels'] = 512
        self.param['sod'] = 600
        self.param['odd'] = 300
        self.param['views'] = 360
        self.param['nbins'] = 640
        self.param['z'] = 32
        self.param['detector_length'] = 800
        ## detector
        self.param['u_water'] = 0.192 #0.0205
        self.param['angles'] = np.linspace(0, 2 * np.pi, self.param['views'], False)
        self.param['ratio'] = self.param['image_pixels'] / self.param['nx']
        self.param['du'] = self.param['detector_length']/self.param['nbins']

def reshape_(f,shape,z):

    line = f.readline()  # 以行的形式进行读取文件
    all = []  # 设置x y z数组
    scat_1 = []
    scat_2 = []
    scat_3 = []
    no_scat = []
    while line:
        if line[0] != '#' and line != '\n':
            line_temp = line.split(' ')  # 每行数据分隔情况，此数据以“,”分隔
            no_scatter = float(line_temp[0])
            scatter_1 = float(line_temp[1])
            scatter_2 = float(line_temp[2])
            scatter_3 = float(line_temp[3])

            no_scat.append(no_scatter)
            scat_1.append(scatter_1)  # 将其添加在列表之中
            scat_2.append(scatter_2)
            scat_3.append(scatter_3)
            all.append(no_scatter + scatter_1 + scatter_2 + scatter_3)
        line = f.readline()
    f.close()  # close文件 # 对获取的txt前两列数据进行保存
    no_scat_np = np.array(no_scat)
    scat_1_np = np.array(scat_1)
    scat_2_np = np.array(scat_2)
    scat_3_np = np.array(scat_3)
    all_np = np.array(all)
    no_scat_np = no_scat_np.reshape(z, shape)
    scat_1_np = scat_1_np.reshape(z, shape)
    scat_2_np = scat_2_np.reshape(z, shape)
    scat_3_np = scat_3_np.reshape(z, shape)
    all_np = all_np.reshape(z, shape)
    return no_scat_np,all_np
def npy2tif_save(npy_,path):
    tif_ = Image.fromarray(npy_)
    tif_.save(path)
def air2energy(path_ori_air,param):
    detectors, views = param.param['nbins'], param.param['views']
    z = param.param['z']
    get_line = int(z / 2)
    air_file = codecs.open(path_ori_air, mode='r')
    file_no, file_all = reshape_(air_file, detectors, z)
    air_line = file_all[get_line, :]
    return air_line
def trunc(npy_, w_l, w_r):
    npy_[npy_ < w_l] = w_l
    npy_[npy_ > w_r] = w_r
    return npy_

def raw2energy(path_ori, energy_no_path, energy_all_path, signal_sim, param,number_point = 6):

    detectors, views = param.param['nbins'], param.param['views']
    z = param.param['z']
    get_line = int(z/2)
    energy_map_no = np.zeros((views, detectors), dtype=np.float64)
    energy_map_all = np.zeros((views, detectors), dtype=np.float64)

    ##取出air_file中间一行


    for path in os.listdir(path_ori):
        if 'raw' in path:
            os.remove(os.path.join(path_ori, path))
    paths = sorted([path for path in os.listdir(path_ori) if signal_sim in path])
    paths.sort(key=lambda x: int(x[number_point:]))
    for i in range(len(paths)):

        num = int(i)   ##720 views
        # num = int(i/2) ##360 views
        path = paths[i]
        path_ = os.path.join(path_ori, path)
        mat_file = codecs.open(path_, mode='r')
        file_no, file_all = reshape_(mat_file, detectors, z)
        # plt.imshow(file_all,'gray')
        # plt.show()

        line_no = file_no[get_line, :]
        line_all = file_all[get_line, :] # mc_dat0....
        # num = int(path[9:])

        energy_map_no[num, :] = line_no
        energy_map_all[num, :] = line_all

    npy2tif_save(energy_map_no,energy_no_path)
    npy2tif_save(energy_map_all, energy_all_path)
    return energy_map_no, energy_map_all


def energy2sino(energy_map, air_line, param):
    detectors, views = param.param['nbins'], param.param['views']
    sino_map = np.zeros((views, detectors), dtype=np.float64)
    for i in range(energy_map.shape[0]):
        for j in range(energy_map.shape[1]):
            sino_map[i][j] = -np.log(energy_map[i][j] / air_line[j])
    return sino_map

def show_fig(ct_no, ct_all,w_l,w_r):

    f, ax = plt.subplots(1, 2, figsize=(20, 10))
    ax[0].imshow(ct_no, cmap=plt.cm.gray, vmin=w_l, vmax=w_r)
    ax[0].set_title('Scatter-free', fontsize=20)
    ax[1].imshow(ct_all, cmap=plt.cm.gray, vmin=w_l, vmax=w_r)
    ax[1].set_title('Scatter-contaminated', fontsize=20)
    plt.xticks([])
    plt.yticks([])
    plt.axis('off')
    plt.show()
    plt.savefig('compare.png')


if __name__ == '__main__':

    path_ori = 'D:/CT_Project/lung_data/mayo_simu/mayo_views_13/'
    path_ori_air = path_ori + 'air.dat'
    os.makedirs(path_ori + 'test_save', exist_ok='True')
    energy_no_path = path_ori + 'test_save/energy_no.tif'
    energy_all_path = path_ori + 'test_save/energy_all.tif'
    ct_no_path = path_ori + 'test_save/ct_no.tif'
    ct_all_path = path_ori + 'test_save/ct_all.tif'

    signal_sim = 'mc'  ###用于查找MC文件的标记
    w_l, w_r = 0.002, 0.030

    param = init()

    load_flag = False  ###是否需要重新加载数据
    ### ct和energy的numpy文件

    energy_map_no, energy_map_all = raw2energy(path_ori, energy_no_path, energy_all_path, signal_sim, param)
    # energy_map_no = np.load(energy_no_path)
    # energy_map_all = np.load(energy_all_path)
    air_line = air2energy(path_ori_air, param)
    sino_map_no = energy2sino(energy_map_no, air_line, param)
    sino_map_all = energy2sino(energy_map_all, air_line, param)

    ct_map_no = Sinogram2Img(sino_map_no, param)
    ct_map_all = Sinogram2Img(sino_map_all, param)

    ct_trunc_no, ct_trunc_all = trunc(ct_map_no, w_l, w_r), trunc(ct_map_all, w_l, w_r)
    npy2tif_save(ct_trunc_no, ct_no_path)
    npy2tif_save(ct_trunc_all, ct_all_path)
    show_fig(ct_trunc_no, ct_trunc_all, w_l, w_r)



