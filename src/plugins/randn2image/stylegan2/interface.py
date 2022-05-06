
import os
import numpy as np
import torch
from .stylegan2.models import *
from .stylegan2 import utils

truncation_psi = 0.7
output = './results'
device = torch.device('cuda')
network = './src/plugins/randn2image/stylegan2/checkpoint/Gs.pth'
G = load(network).to(device)
G.eval()
latent_size = G.latent_size

def rand2img(seed):
    if truncation_psi != 1:
        G.set_truncation(truncation_psi=truncation_psi)
    noise_reference = G.static_noise()
    noise_tensors = [[] for _ in noise_reference]
    rnd = np.random.RandomState(seed)
    latent = torch.from_numpy(rnd.randn(latent_size)).to(device=device, dtype=torch.float32)
    latent =  latent.unsqueeze(0)
    for i, ref in enumerate(noise_reference):
        noise_tensors[i].append(torch.from_numpy(rnd.randn(*ref.size()[1:])))
    noise_tensors = [
                torch.stack(noise, dim=0).to(device=device, dtype=torch.float32)
                for noise in noise_tensors
            ]
    G.static_noise(noise_tensors=noise_tensors)
    with torch.no_grad():
        generated = G(latent)
    img = utils.tensor_to_PIL(
        generated, pixel_min=-1, pixel_max=1)
    return img[0]