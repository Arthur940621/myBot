import torch
from .model import create_model
from .data import tensor_to_img, resize_image, get_transform

device = torch.device('cuda')
model = create_model().to(device) 
model.eval()

def color2sketch(img):
    aus_resize = img.size
    transform = get_transform(load_size=512)
    img = transform(img)
    img = img.unsqueeze(0)
    aus_tensor = model(img.to(device))
    aus_img = tensor_to_img(aus_tensor)
    return resize_image(aus_img, aus_resize)