from trainkidsphoto import Net
import torch
import torchvision
import torchvision.transforms as transforms
import torch.nn as nn
import torch.nn.functional as F
import torch.optim as optim
import matplotlib.pyplot as plt
import numpy as np
from PIL import Image
import io
import requests
from torchvision import models
import torchvision.transforms as T
from torch.autograd import Variable

normalize = T.Normalize(
   mean=[0.4914, 0.4822, 0.4465],
   std=[0.247, 0.243, 0.261]
)
preprocess = T.Compose([
   T.Resize((320,240)),
   T.CenterCrop((320,240)),
   T.ToTensor(),
   normalize
])

net = Net()

PATH = './cifar_net.pth'
#net.load_state_dict(torch.load(PATH))

criterion = nn.CrossEntropyLoss()

input = Image.open("m2106-red-500x300.jpg")

input_tensor = preprocess(input)

input_tensor.unsqueeze_(0)

output = net(input_tensor)

print(output)