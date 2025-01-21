import torch
import torch.nn as nn
from torch.utils.data import DataLoader, Dataset


''' Salt and Pepper '''
class SaltAndPepper(object):
    def __init__(self, prob = 0.01):
        self.p = prob  # Probability of noise

    def __call__(self, tensor):
        t = tensor.clone()
        n = torch.rand(t.size())
        t[n < self.p / 2] = 0.0  # Pepper
        t[(n >= self.p / 2) & (n < self.p)] = 1.0  # Salt
        return t

''' Dataset '''
class MyDataset(Dataset):
    def __init__(self, annotations_file, img_dir, is_train = False):
        import json
        import pandas as pd
        import torchvision.transforms as transforms
        super(MyDataset, self).__init__()

        with open(annotations_file) as f:
            data = json.load(f)

        self.img_labels = pd.DataFrame(
            [{"filename": k, "label": v} for k, v in data.items()]
        )

        self.img_dir = img_dir
        self.is_train = is_train
        self.crop_size = (256, 256)

        if self.is_train:
            self.transform = transforms.Compose([
                transforms.Resize((300, 300)),
                transforms.RandomCrop(self.crop_size),
                transforms.RandomHorizontalFlip(),
                transforms.ColorJitter(brightness = 0.11, contrast = 0.11, saturation = 0.11, hue = 0.11),
                transforms.RandomAffine(degrees = 10, translate = (0.1, 0.1),scale = (0.9, 1.1)),
                transforms.ToTensor(),
                SaltAndPepper(prob = 0.001),
                transforms.Normalize(mean = [0.485, 0.456, 0.406], std = [0.229, 0.224, 0.225]),
                transforms.RandomErasing(p = 0.5, scale = (0.02, 0.08), ratio = (0.3, .9))
            ])
        else:
            self.transform = transforms.Compose([
                transforms.Resize((256, 256)),
                transforms.CenterCrop(self.crop_size),
                transforms.ToTensor(),
                transforms.Normalize(mean = [0.485, 0.456, 0.406], std = [0.229, 0.224, 0.225])
            ])

    def __len__(self):
        return len(self.img_labels)
    
    def __getitem__(self, idx):
        import os
        from PIL import Image
        path = os.path.join(self.img_dir, self.img_labels.iloc[idx, 0])
        image = Image.open(path).convert('RGB')
        image = self.transform(image)
        label = self.img_labels.iloc[idx, 1] - 1 # convert to 0 indexed
        label = torch.tensor(label)
        return image, label

''' ResNet Architecture '''
class MyNetwork(nn.Module):
    def __init__(self):
        import torchvision
        super(MyNetwork, self).__init__()

        ''' ResNet '''
        ref_model = torchvision.models.resnet18(weights = torchvision.models.ResNet18_Weights.IMAGENET1K_V1)

        ''' batch norm '''
        self.bn1 = ref_model.bn1

        ''' convolution layers '''
        self.conv1 = ref_model.conv1

        ''' activation layers '''
        self.relu = ref_model.relu

        ''' pooling layers '''
        self.maxpool = ref_model.maxpool
        self.avgpool = ref_model.avgpool # global average pooling

        ''' residual layers '''
        self.layer1 = ref_model.layer1
        self.layer2 = ref_model.layer2
        self.layer3 = ref_model.layer3
        self.layer4 = ref_model.layer4

        ''' linear layers '''
        self.fc = nn.Linear(ref_model.fc.in_features, 196) # fully connected

    def forward(self, x):
        x = self.conv1(x)
        x = self.bn1(x)
        x = self.relu(x)
        x = self.maxpool(x)
        x = self.layer1(x)
        x = self.layer2(x)
        x = self.layer3(x)
        x = self.layer4(x)
        x = self.avgpool(x)
        
        x = self.fc(torch.flatten(x, 1))  # Pass through new fully connected layer
        return x

TRAINING_DATA = MyDataset(annotations_file = "train_annos.json", img_dir = "cars_train", is_train = True)
TEST_DATA = MyDataset(annotations_file = "test_annos.json", img_dir = "cars_test")
MODEL = MyNetwork()
MODEL = MODEL.cuda()

''' Training '''
def training_loop(epochs = 8, batch = 8, initial_rate = 1e-5, max_rate = .001):
    from torch.optim.lr_scheduler import OneCycleLR
    from tqdm import tqdm
    global MODEL, TRAINING_DATA; MODEL.train()

    # training
    training_loader = DataLoader(TRAINING_DATA, batch_size = batch, shuffle = True, num_workers = 4)
    losses = []
    twenty = 20
    batch_count = 0

    # optimizer & scheduler
    optimizer = torch.optim.Adam(MODEL.parameters(), lr = initial_rate)
    scheduler = OneCycleLR(optimizer = optimizer, max_lr = max_rate, steps_per_epoch = len(training_loader), epochs = epochs)

    # loss function
    loss_func = torch.nn.CrossEntropyLoss()

    for epoch in range(epochs):
        with tqdm(training_loader, unit = "batch") as timed_epoch:
            for images, labels in timed_epoch:
                timed_epoch.set_description(f"Epoch {epoch + 1}")
                images, labels = images.cuda(), labels.cuda()
                
                optimizer.zero_grad() # zero the gradients
                outs = MODEL(images) # forward pass
                loss = loss_func(outs, labels) # compute loss
                loss.backward() # backward pass
                optimizer.step() # update weights
                scheduler.step()

                # track losses
                losses.append(loss.item()) 
                batch_count += 1
                if batch_count % twenty == 0:
                    avg_loss = sum(losses[-twenty:]) / twenty
                    timed_epoch.set_postfix(loss = avg_loss)
        
''' Testing '''
def test_loop(batch = 1):
    global MODEL, TEST_DATA; MODEL.eval() # evaluation mode
    test_loader = DataLoader(TEST_DATA, batch_size = batch, shuffle = True, num_workers = 4)
    all_predictions = []
    all_labels = []

    # test loop
    with torch.no_grad():
        for images, labels in test_loader:
            images, labels = images.cuda(), labels.cuda() # accelerate
            outputs = MODEL(images) # Get model predictions
            _, predicted = torch.max(input = outputs, dim = 1)
            # store predictions and ground truth labels
            all_predictions.extend(predicted.tolist())
            all_labels.extend(labels.tolist())
    return all_predictions, all_labels

''' Calculate Accuracy '''
def calculate_accuracy(predictions, labels):
    total_correct = sum([pred == true for pred, true in zip(predictions, labels)])
    accuracy = total_correct / len(labels) * 100
    print(f"Test Accuracy: {accuracy:.2f}%")

if __name__ == "__main__":
    training_loop(epochs = 20, batch = 64, initial_rate = 1e-6, max_rate = .001)
    p, l = test_loop(batch = 1)
    calculate_accuracy(predictions = p, labels = l)
