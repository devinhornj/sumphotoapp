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

PATH = 'D:/Models/kidsphotomodel89(0.03864210571628064).pth'
net.load_state_dict(torch.load(PATH))

criterion = nn.CrossEntropyLoss()

input = Image.open("testimages/IMG_0802.jpeg")

input_tensor = preprocess(input)

input_tensor.unsqueeze_(0)
input_tensor = input_tensor.cuda()

output = net(input_tensor)

print(output)