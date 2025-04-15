import torch
from torchvision import models, transforms
from PIL import Image
import json
import os
from torchvision.models import ResNet18_Weights



# Путь к текущей папке приложения
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

# === Загрузка модели ===
model = models.resnet18(weights=None)
model.fc = torch.nn.Linear(model.fc.in_features, 100)
model_path = os.path.join(BASE_DIR, 'resnet_music.pth')
model.load_state_dict(torch.load(model_path, map_location='cpu'))
model.eval()

# === Загрузка соответствия классов и песен ===
with open(os.path.join(BASE_DIR, 'class_to_songs.json'), 'r') as f:
    class_to_songs = json.load(f)

# === Преобразование для входного изображения ===
transform = transforms.Compose([
    transforms.Resize((244, 244)),
    transforms.ToTensor(),
    transforms.Normalize([0.485, 0.456, 0.406],
                         [0.229, 0.224, 0.225])
])

# === Основная функция предсказания ===
def predict_spectrogram(image_file):
    image = Image.open(image_file).convert('RGB')
    input_tensor = transform(image).unsqueeze(0)

    with torch.no_grad():
        output = model(input_tensor)
        pred_class = torch.argmax(output, dim=1).item()

    return class_to_songs.get(str(pred_class), ['Unknown class'])


# Функция: ищем класс по названию песни
def find_class_by_song(song_name: str):
    for class_id, songs in class_to_songs.items():
        for song in songs:
            if song_name.lower() in song.lower():
                return int(class_id), songs
    return None, []
