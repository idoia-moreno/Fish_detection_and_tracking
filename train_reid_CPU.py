from sacred import Experiment
import os.path as osp
import os
import numpy as np
import yaml
import cv2
import tkinter

import matplotlib
matplotlib.use('tkAgg')

import matplotlib.pyplot as plt
import matplotlib.image as mpimg

import torch
import matplotlib.pyplot as plt
#import Transforms as T
#import torchvision.transform as T

from torch.utils.data import DataLoader

from tracktor.config import get_output_dir, get_tb_dir
from tracktor.reid.solver import Solver
from tracktor.datasets.factory import Datasets
from tracktor.reid.resnet_CPU import resnet50
#from PIL import Image

#ex = Experiment()
#ex.add_config('/home/idoia/Documentos/TFM/GITHUB/tracking_wo_bnw/experiments/cfgs/reid.yaml')

#Solver = ex.capture(Solver, prefix='reid.solver')

#@ex.automain
#def my_main(_config, reid):



if __name__ == "__main__":
    # Load reid.yaml' ########################################!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
    # read_categories.py file

    import yaml

    with open(r'/home/idoia/Documentos/TFM/GITHUB/tracking_wo_bnw/experiments/cfgs/reid.yaml') as file:
        document = yaml.full_load(file)

        for item, doc in document.items():
            print(item, ":", doc)
   # https: // stackabuse.com / reading - and -writing - yaml - to - a - file - in -python

    reid = document['reid']
    print("Type: "+str(type(document)))
    # set all seeds
    print("PRUEBA")
    torch.manual_seed(reid['seed'])
    torch.cuda.manual_seed(reid['seed'])
    np.random.seed(reid['seed'])
    torch.backends.cudnn.deterministic = True

    #print(_config)

    output_dir = osp.join(get_output_dir(reid['module_name']), reid['name'])
    tb_dir = osp.join(get_tb_dir(reid['module_name']), reid['name'])



    #sacred_config = osp.join(output_dir, 'sacred_config.yaml')

    print("output_dir" + output_dir)
    print("tb_dir" + tb_dir)
    #print("sacred_config"+sacred_config)

    if not osp.exists(output_dir):
        os.makedirs(output_dir)
###################################
  #  '''
   #     hola
    #    with open(sacred_config, 'w') as outfile:
     #   yaml.dump(_config, outfile, default_flow_style=False)
    #'''
############################
    #########################
    # Initialize dataloader #
    #########################
    print("[*] Initializing Dataloader")

    #########################
    # Initialize dataloader #
    #########################

   # '''
    #Dataset stores the samples and their corresponding labels, and DataLoader wraps an iterable around the Dataset to enable easy access to the samples.'''

    db_train_1 = Datasets(reid['db_train'], reid['dataloader'])
    db_train = DataLoader(db_train_1, batch_size=1, shuffle=True)

    # #########################
    # # VISUALIZE READ DATASET TO KNOW IF EVERYTHING IS ALRIGHT #
    # #########################
    # print(len(db_train))
    # figure = plt.figure(figsize=(8, 8))
    #
    # img = db_train.dataset._data[0]
    # image_path = img.data[0]['im_path']
    # image_gt_array = img.data[0]['gt']
    # print(image_path)
    #
    # image = cv2.imread(image_path)
    # window_name = 'image'
    # #cv2.imshow(window_name, image)
    # #cv2.waitKey(0)
    # #cv2.destroyAllWindows()
    #
    # #VISUALIZAR CON BOUNDING BOX:
    #
    # data = list(image_gt_array.items())
    # gt_array = np.array(data)
    #
    # start_point = (1721,178)
    # end_point = (1919,495)
    # color = (255,0,0)
    # thickness = 2
    # image_bb = cv2.rectangle(image,start_point,end_point,color,thickness)
    #
    # for i in range(1,22):
    #     sp_1 = gt_array[i][1][0]
    #     sp_2 = gt_array[i][1][1]
    #     ep_1 = gt_array[i][1][2]
    #     ep_2 = gt_array[i][1][3]
    #     start_point = (sp_1,sp_2)
    #     end_point = (ep_1,ep_2)
    #     image_bb = cv2.rectangle(image_bb, start_point, end_point, color, thickness)
    #
    #
    # cv2.imshow(window_name, image_bb)
    # cv2.waitKey(0)
    # cv2.destroyAllWindows()
    #



    if reid['db_val']:
        db_val = None
        #db_val = DataLoader(db_val, batch_size=1, shuffle=True)
    else:
        db_val = None

    ##########################
    # Initialize the modules #
    ##########################
    print("[*] Building CNN")
    network = resnet50(pretrained=True, **reid['cnn'])
    network.train()
    #network.cuda()

    ##################
    # Begin training #
    ##################
    print("[*] Solving ...")

    # build scheduling like in "In Defense of the Triplet Loss for Person Re-Identification"
    # from Hermans et al.
    lr = reid['solver']['optim_args']['lr']
    iters_per_epoch = len(db_train)
    # we want to keep lr until iter 15000 and from there to iter 25000 a exponential decay
    l = eval("lambda epoch: 1 if epoch*{} < 15000 else 0.001**((epoch*{} - 15000)/(25000-15000))".format(
                                                                iters_per_epoch,  iters_per_epoch))
    #else:
    #   l = None

    max_epochs = 50
    #max_epochs = 25000 // len(db_train.dataset) + 1 if 25000 % len(db_train.dataset) else 25000 // len(db_train.dataset)
    solver = Solver(output_dir, tb_dir, optim=reid['solver']['optim'], optim_args=reid['solver']['optim_args'], lr_scheduler_lambda=l)
    solver.train(network, db_train, db_val, max_epochs, 100, model_args=reid['model_args'])




