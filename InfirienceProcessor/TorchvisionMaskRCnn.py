import os
from os.path import exists, join, basename, splitext
import random
import PIL
import torchvision
import cv2
import numpy as np
import torch
import time
import matplotlib
import matplotlib.pylab as plt

model = {}

def init():
    torch.set_grad_enabled(False)  
    plt.rcParams["axes.grid"] = False
    model = torchvision.models.detection.maskrcnn_resnet50_fpn(pretrained=True)
    model = model.eval().cuda()

def run(imageFilename):
    image = PIL.Image.open(imageFilename)
    image_tensor = torchvision.transforms.functional.to_tensor(image).cuda()
    output = model([image_tensor])[0]
        
    return output;