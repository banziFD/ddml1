import pickle
import numpy as np 
from PIL import Image
import glob
import torch
import torchvision.transforms as transforms
import json
import random

def msrcvData(datasetPath, select):
    folders =['airplane', 'bicycle', 'building', 'car', 'cow', 'face', 'tree']
    l = 0
    meta = dict()
    label = list()
    idx = 0
    for folder in folders:
        files = glob(datasetPath + '/' + folder + '/*.bmp')
        meta[l] = folder
        for f in files:
            img = Image.open(f)
            img.save('{}.jpg'.format(idx))
            label.append(l)
            idx += 1
        l += 1
        test = np.random.choice(len(label), len(label) // 10, replace = False).tolist()
    train = list()
    for i in range(len(label)):
        if i not in test:
            train.append(i)
    random.shuffle(train)
    json.dump(test, open(datasetPath + 'test.json', 'w'))
    json.dump(train, open(datasetPath + 'train.json', 'w'))
    json.dump(meta, open(datasetPath + 'meta.json', 'w'))

def prepareData(datasetPath, workPath, select = ['airplane', 'bicycle', 'building', 'car', 'cow', 'face', 'tree']):
    data = msrcvData(datasetPath, select)

class MsrcvSet(torch.utils.data.Dataset):
    def __init__(self, workPath, mode = 'train', vecLabel = False, nbClass = 7):
        super(MsrcvSet, self).__init__()
        self.mode = mode
        self.image = workPath + '/msrcv'
        self.label = json.load(workPath + '/mscrv7/label')
        self.key = json.load(workPath + '/{}'.format(self.mode))
        self.transform = transforms.Compose([transforms.resize(), transforms.ToTensor(), transforms.Normalize(mean = [0.485, 0.456, 0.406], std = [0.229, 0.224, 0.225])])
        self.vecLabel = vecLabel

    def __getitem__(self, index):
        k = self.key[index]
        x = Image.open(self.image + '/{}.jpg'.format(k))
        x = self.transform(x)
        y = self.label[k]
        if(self.vecLabel):
            t = torch.zeros(10)
            t[y] = 1
            y = t
        return x, y

    def __len__(self):
        assert self.label.shape[0] == self.image.shape[0]
        return self.label.shape[0]

if __name__ == '__main__':
    pass