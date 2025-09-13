from ultralytics import YOLO
import yaml

data_loc = "datasets/last_z"
yaml_loc = f"{data_loc}/data.yaml"

save_dir = "/Users/large/Documents/code/python/ultralytics/runs/detect/train"
model_loc = f"{save_dir}/weights/best.pt"

# load up the labels
with open(yaml_loc, 'r') as f:
	label = yaml.safe_load(f)['names']
print(label)

# Load a pretrained YOLO model (recommended for training)
# model = YOLO("yolo11n.pt")
model = YOLO(model_loc)

# Train the model using the dataset for 3 epochs
results = model.train(data=yaml_loc, epochs=100000, imgsz=1024, device="mps") #, resume=True)
save_dir = str(results.save_dir)
model_loc = f"{save_dir}/weights/best.pt"

# Evaluate the model's performance on the validation set
results = model.val()
print(results)
print(model_loc)
