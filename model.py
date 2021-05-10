import torch
import torch.nn as nn
import torch.nn.functional as F
from torchvision.models import resnet50
import numpy as np
from utils.utils import *

def get_loss_model(cfg):
    return nn.CrossEntropyLoss().cuda()

def get_optimizer(cfg, params):
    if cfg["optimizer"]["type"] == "adam":
        optimizer = torch.optim.Adam(params,
                        lr=cfg["optimizer"]["lr"],
                        weight_decay=cfg["optimizer"]["weight_decay"])
    elif cfg["optimizer"]["type"] == "sgd":
        optimizer = torch.optim.SGD(params,
                        lr=cfg["optimizer"]["lr"],
                        weight_decay=cfg["optimizer"]["weight_decay"],
                        momentum=cfg["optimizer"]["momentum"])
    return optimizer

def get_lr_scheduler(cfg, optimizer):
    return torch.optim.lr_scheduler.StepLR(optimizer,
                        step_size=cfg["optimizer"]["step_size"], gamma=cfg["optimizer"]["gamma"])

class CarColor(nn.Module):
    def __init__(self, cfg):
        super().__init__()
        self.cfg = cfg
        self.cfg_data = cfg["data"]

        self.resnet50 = resnet50(pretrained=True)
        num_features = self.resnet50.fc.in_features
        num_class = getTotalColorLabel()
        self.resnet50.fc = nn.Linear(num_features, num_class) # length of color classes
        self.loss_model = get_loss_model(self.cfg)

    def forward(self, track):
        return self.resnet50(track)

    def compute_loss(self, track):
        loss = 0.
        out = self.forward(track['crop'])

        for index, o in enumerate(out):
            o = torch.unsqueeze(o, dim=0)
            l = 0.
            for k, v in track['color'][index].items():
                target = torch.LongTensor([k]).cuda()
                l += self.loss_model(o, target) * v
            loss += l
        loss /= len(track['crop'])
        return loss

    def compute_color_list(self, query):
        return getColorList(query)

    def compute_similarity_on_frame(self, tracks):
        with torch.no_grad():
            percentages = list()
            for i, t in enumerate(tracks['crops']):
                actual_t = t[:tracks['sequence_len'][i]]
                out = self.forward(actual_t)
                percentage = nn.functional.softmax(out, dim=1)[0]
                percentage = percentage.detach().to('cpu').numpy()
                percentages.append(percentage)

        return percentages

    def compute_color_prob(self, colors, probs):
        score = 0.
        for c in colors:
            score += probs[c]
        return score

class CarType(nn.Module):
    def __init__(self, cfg):
        super().__init__()
        self.cfg = cfg
        self.cfg_data = cfg["data"]

        self.resnet50 = resnet50(pretrained=True)
        num_features = self.resnet50.fc.in_features
        num_class = getTotalTypeLabel()
        self.resnet50.fc = nn.Linear(num_features, num_class) # length of model classes
        self.loss_model = get_loss_model(self.cfg)

    def forward(self, track):
        return self.resnet50(track)

    def compute_loss(self, track):
        loss = 0.
        out = self.forward(track['crop'])

        for index, o in enumerate(out):
            o = torch.unsqueeze(o, dim=0)
            l = 0.
            for k, v in track['type'][index].items():
                target = torch.LongTensor([k]).cuda()
                l += self.loss_model(o, target) * v
            loss += l
        loss /= len(track['crop'])
        return loss

    def compute_type_list(self, query):
        return getTypeList(query)

    def compute_similarity_on_frame(self, tracks):
        with torch.no_grad():
            percentages = list()
            for i, t in enumerate(tracks['crops']):
                actual_t = t[:tracks['sequence_len'][i]]
                out = self.forward(actual_t)
                percentage = nn.functional.softmax(out, dim=1)[0]
                percentage = percentage.detach().to('cpu').numpy()
                percentages.append(percentage)

        return percentages

    def compute_type_prob(self, types, probs):
        score = 0.
        for tp in types:
            score += probs[tp]
        return score
