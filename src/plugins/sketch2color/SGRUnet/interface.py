from .model import Gnet
import torch
from torchvision import transforms
import numpy as np
import random
from PIL import Image

model_path = './src/plugins/sketch2color/SGRUnet/checkpoints/checkpoint.pth'
device = torch.device('cuda')
model = Gnet.SGRU().to(device)
ckp = torch.load(model_path, map_location=device)
model.load_state_dict(ckp['model'])
model = model.eval()

def sketch2color(img):
    aus_resize = img.size
    img = img.resize((256, 256)).convert('L')
    img = transforms.ToTensor()(img).unsqueeze(0)
    with torch.no_grad():
        output = model(img).squeeze()
    output = output.detach().numpy()
    output = output.clip(0.0, 255.0)
    output = output.astype(np.uint8).transpose(0, 2, 3, 1)
    num_idx = random.randint(0, output.shape[0]-1)
    img_fake_rgb = Image.fromarray(output[num_idx, ...])
    img_fake_rgb = img_fake_rgb.resize(aus_resize)
    # img_fake_rgb.save("./src/plugins/sketch2color/SGRUnet/output/out_{0}".format(i))
    return img_fake_rgb