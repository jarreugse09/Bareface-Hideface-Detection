import torch
from ultralytics import YOLO

if __name__ == '__main__':
    print(torch.cuda.is_available())
    print(torch.cuda.get_device_name(0))

    model = YOLO("yolov8n.pt")

    device = 'cuda' if torch.cuda.is_available() else 'cpu'
    results = model.train(data=r"C:\Users\Hanz Joshua\PycharmProjects\pythonProject4\data/data.yaml", epochs=40,
                          batch=16, device=device, mosaic=0)

