import torch
import torch.nn as nn
import torch.nn.functional as F

from ..base import BaseSuperlayer
from ..block_utils import ConvBNAct


class ZeroConv(nn.Module):
    def __init__(self, in_channels, out_channels, stride):
        super(ZeroConv, self).__init__()
        self.zero_conv = nn.Conv2d(in_channels, out_channels, 1, stride=stride, bias=False)
    
    def forward(self, x):
        return self.zero_conv(x) * 0


class UnifiedSubBlock(BaseSuperlayer):
    def _construct_supernet_layer(self, in_channels, out_channels, stride, bn_momentum, bn_track_running_stats):
        activation = self.micro_cfg[1]
        self.micro_cfg = self.micro_cfg[0]
        
        self.supernet_layer = nn.ModuleList()
        # Micro confg is  kernel size list
        for i, kernel_size in enumerate(self.micro_cfg):
            if kernel_size == "skip":
                operation = ZeroConv(in_channels=in_channels,
                                     out_channels=out_channels,
                                     stride=stride)

            else:
                operation = ConvBNAct(in_channels=in_channels,
                                      out_channels=out_channels,
                                      kernel_size=kernel_size,
                                      stride=stride,
                                      activation=activation,
                                      bn_momentum=bn_momentum,
                                      bn_track_running_stats=bn_track_running_stats,
                                      pad=(kernel_size // 2),
                                      group=out_channels)

            self.supernet_layer.append(operation)
