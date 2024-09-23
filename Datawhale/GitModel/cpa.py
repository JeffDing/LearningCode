#!/usr/bin/env python
# coding: utf-8

# # 中国人口分析
# **作者**：陈艺荣   
# **依赖**：python3.7、pytorch1.3.0    

# 导入相应包
import torch
import torch.nn.functional as F


class PAnet(torch.nn.Module):
    def __init__(self, n_feature, n_hidden, n_output, hidden_num=1):
        super(PAnet, self).__init__()
        self.hidden1 = torch.nn.Linear(n_feature, n_hidden)   # hidden1 layer
        self.hidden2 = torch.nn.ModuleList([torch.nn.Linear(n_hidden, n_hidden) for i in range(hidden_num)])
        self.predict = torch.nn.Linear(n_hidden, n_output)   # output layer        
        
    def forward(self, x):
        x = F.relu(self.hidden1(x)) 
        for i, h in enumerate(self.hidden2):
            x = F.relu(h(x))
        x = self.predict(x) # linear output
        return x