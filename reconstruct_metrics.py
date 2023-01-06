import astra
import matplotlib.pyplot as plt
import numpy as np

###fan_beam reconstruction
def Sinogram2Img(sinogram, param):
    nx = param.param['nx']  ## 原图像大小
    image_size = param.param['image_pixels']
    radius1 = param.param['sod']
    radius2 = param.param['odd']
    detectorlength = param.param['detector_length']
    du = param.param['du']
    ratio = param.param['ratio']
    nbins = param.param['nbins']
    angles = param.param['angles']
    '''


    此方法使用正弦图生成空间域图像
    :return 输出空间域图像
    '''
    '''
    ``create_proj_geom('fanflat', det_width, det_count, angles, source_origin, origin_det)``:

    :param det_width: Size of a detector pixel.
    :type det_width: :class:`float`
    :param det_count: Number of detector pixels.
    :type det_count: :class:`int`
    :param angles: Array of angles in radians.
    :type angles: :class:`numpy.ndarray`
    :param source_origin: Position of the source.
    :param origin_det: Position of the detector
    :returns: A fan-beam projection geometry.
    '''
    plt.imshow(sinogram, 'gray')
    plt.show()
    vol_geom = astra.create_vol_geom(image_size, image_size)
    proj_geom = astra.create_proj_geom('fanflat', du * ratio, nbins, angles,
                                       radius1 * ratio, radius2 * ratio)  # unit: mmnx / ximageside
    # As before, create a sinogram from a phantom

    proj_id = astra.data2d.create('-sino', proj_geom, sinogram)
    rec_id = astra.data2d.create('-vol', vol_geom)

    # create the a data object for the reconstruction

    # Set up the parameters for a reconstruction algorithm using the GPU
    cfg = astra.astra_dict('FBP_CUDA')
    cfg['ReconstructionDataId'] = rec_id
    cfg['ProjectionDataId'] = proj_id
    # cfg['option'] = {'ShortScan': False}
    # Create the algorithm object from the configuration structure
    alg_id = astra.algorithm.create(cfg)

    # Run 150 iterations of the algorithm

    astra.algorithm.run(alg_id, 100)

    # Get the result
    rec = astra.data2d.get(rec_id)
    astra.algorithm.delete(alg_id)
    astra.data2d.delete(rec_id)
    astra.data2d.delete(proj_id)

    img = np.array(rec).astype('float32')
    img[img < 0] = 0
    return img
