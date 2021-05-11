# [GCT700] AR Project / Team 3
# A conversion of PyTorch model to the ONNX format

import torch

EXPORT_MODEL_NAME = "slrecog.onnx"

# read a temp model (until we get the RCV model)
model = torch.hub.load('pytorch/vision:v0.6.0', 'densenet121', pretrained = True)

# set the model to eval mode
model.eval()

# create a sample input
dummy_inpyt = torch.randn(1, 3, 256, 256) # --> the shape of the output tensor. (batch_size, channel(RGB), width, height)

    # Memo
    # - Image tensor (4D): batch_size, channel, width, heighh
    # - Video tensor (5D): batch_size, frames, chennel, width, height

# convert the model to onnx
torch.onnx.export(model, dummy_inpyt, EXPORT_MODEL_NAME, verbose = True)