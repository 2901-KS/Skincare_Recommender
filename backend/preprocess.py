import torchvision.transforms as T
from PIL import Image

transform = T.Compose([
    T.Resize((224, 224)),
    T.ToTensor(),
])

def preprocess_image(img_path):
    img = Image.open(img_path).convert("RGB")
    return transform(img).unsqueeze(0)
