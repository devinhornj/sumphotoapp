import torch
import torchvision
import torchvision.transforms as transforms
import torch.nn as nn
import torch.nn.functional as F
import torch.optim as optim
import matplotlib.pyplot as plt
import numpy as np
from PIL import Image
from torchvision import datasets

class my_segmentation_transforms(object):
    def __call__(self, img):
        if img.shape[1:] != (320, 240):
            img = torch.rot90(img, 1, (1, 2))

        return img

    def __repr__(self):
        return self.__class__.__name__ + '()'


def main():
    transform = transforms.Compose(
        [transforms.ToTensor(), my_segmentation_transforms(),
         transforms.Normalize((0.5, 0.5, 0.5), (0.5, 0.5, 0.5))
         ])

    trainset = datasets.ImageFolder("images", transform=transform)
    trainloader = torch.utils.data.DataLoader(trainset, batch_size=10, shuffle=True)

    classes = ('good', 'bad')

    device = torch.device('cuda:0' if torch.cuda.is_available() else 'cpu')
    net = Net().cuda()

    criterion = nn.CrossEntropyLoss()
    optimizer = optim.SGD(net.parameters(), lr=0.001, momentum=0.9)

    for epoch in range(100) :  # loop over the dataset multiple times

        running_loss = 0.0
        for i, data in enumerate(trainloader, 0):
            # get the inputs; data is a list of [inputs, labels]
            inputs, labels = data
            inputs = inputs.cuda()  # this is where the data is loaded into GPU
            labels = labels.cuda()

            # zero the parameter gradients
            optimizer.zero_grad()

            # forward + backward + optimize
            outputs = net(inputs)
            loss = criterion(outputs, labels)
            loss.backward()
            optimizer.step()

            # print statistics
            running_loss += loss.item()
            if i % 200 == 199:
                print('[%d, %5d] loss: %.3f' %
                      (epoch + 1, i + 1, running_loss / 200))
                running_loss = 0.0

        PATH = 'D:/models/kidsphotomodel' + str(epoch) + "(" + str(running_loss / 200) + ")" + '.pth'
        torch.save(net.state_dict(), PATH)

    print('Finished Training')

    def imshow(img):
        img = img / 2 + 0.5  # unnormalize
        npimg = img.numpy()
        plt.imshow(np.transpose(npimg, (1, 2, 0)))
        plt.show()


class Net(nn.Module):
    def __init__(self):
        super().__init__()
        self.conv1 = nn.Conv2d(3, 64, 3).cuda()
        self.pool = nn.MaxPool2d(2, 2).cuda()
        self.conv2 = nn.Conv2d(64, 128, 3).cuda()
        self.conv3 = nn.Conv2d(128, 256, 3).cuda()
        self.conv4 = nn.Conv2d(256, 512, 3).cuda()
        self.fc1 = nn.Linear(18 * 13 * 512, 120).cuda()
        self.fc2 = nn.Linear(120, 84).cuda()
        self.fc3 = nn.Linear(84, 2).cuda()
        self.batchNorm1 = nn.BatchNorm2d(64).cuda()
        self.batchNorm2 = nn.BatchNorm2d(128).cuda()
        self.batchNorm3 = nn.BatchNorm2d(256).cuda()
        self.batchNorm4 = nn.BatchNorm2d(512).cuda()

    def forward(self, x):
        x = self.pool(F.relu(self.batchNorm1(self.conv1(x))))
        x = self.pool(F.relu(self.batchNorm2(self.conv2(x))))
        x = self.pool(F.relu(self.batchNorm3(self.conv3(x))))
        x = self.pool(F.relu(self.batchNorm4(self.conv4(x))))
        x = torch.flatten(x, 1)
        x = F.relu(self.fc1(x))
        x = F.relu(self.fc2(x))
        x = self.fc3(x)
        return x
