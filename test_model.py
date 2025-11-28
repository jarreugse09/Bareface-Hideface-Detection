import torch
from ultralytics import YOLO

if __name__ == '__main__':

    model = YOLO(r"C:\Users\Hanz Joshua\PycharmProjects\pythonProject4\runs\detect\train4\weights/best.pt")
    results = model.val(data=r"C:\Users\Hanz Joshua\PycharmProjects\pythonProject4\data/val_data.yaml")
