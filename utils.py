from PIL import Image
from torchvision.models import mobilenet_v2, MobileNet_V2_Weights
import cv2
import numpy as np
import pandas as pd
import torch
import torch.nn as nn


class CNN_LSTM(nn.Module):
    def __init__(self, hidden_size=128, seq_length=5):
        super(CNN_LSTM, self).__init__()
        self.seq_length = seq_length
        mobilenet = mobilenet_v2(weights=MobileNet_V2_Weights.DEFAULT)
        # mobilenet = mobilenet_v3_small(weights=MobileNet_V3_Small_Weights.DEFAULT)
        self.cnn = mobilenet.features
        self.pool = nn.AdaptiveAvgPool2d((1, 1))
        self.flatten = nn.Flatten()
        self.lstm = nn.LSTM(input_size=1280, hidden_size=hidden_size, batch_first=True)
        # self.lstm = nn.LSTM(input_size=576, hidden_size=hidden_size, batch_first=True)
        self.fc = nn.Linear(hidden_size, 3)

    def forward(self, x):
        batch_size, seq_len, C, H, W = x.size()
        c_out = []
        for t in range(seq_len):
            cnn_feat = self.cnn(x[:, t, :, :, :])
            pooled = self.pool(cnn_feat)
            flat = self.flatten(pooled)
            c_out.append(flat)
        c_out = torch.stack(c_out, dim=1)
        lstm_out, _ = self.lstm(c_out)
        out = self.fc(lstm_out[:, -1, :])
        return out


def get_translations_coords(vo, i, cur_pose, K, df_gt=None):
    img1 = vo.get_image(i - 1)
    img2 = vo.get_image(i)

    kp1, des1 = vo.extract_features(img1)
    kp2, des2 = vo.extract_features(img2)

    matches = vo.match_features(des1, des2)
    print(f"Frame {i}: Eşleşen özellik sayısı = {len(matches)}")

    result = vo.estimate_pose(kp1, kp2, matches, K)

    T = np.eye(4)  # Varsayılan dönüşüm matrisi (değişmeyen pozisyon)
    if result is not None:
        R, t = result

        # Ölçeklendirme (Ground truth varsa)
        if df_gt is not None and i < len(df_gt):
            prev_gt = df_gt.loc[i - 1, ["translation_x", "translation_y", "translation_z"]].values
            curr_gt = df_gt.loc[i, ["translation_x", "translation_y", "translation_z"]].values
            gt_motion = curr_gt - prev_gt
            scale = np.linalg.norm(gt_motion)
            t_norm = np.linalg.norm(t)
            if t_norm > 0:
                t = t * (scale / t_norm)

        T[:3, :3] = R
        T[:3, 3] = t.flatten()
    else:
        print(f"Frame {i}: Poz tahmini başarısız, pozisyon aynı kalacak.")

    cur_pose = cur_pose @ T
    pos = cur_pose[:3, 3].flatten()

    translation_xyz = {
        "translation_x": float(pos[0]),
        "translation_y": float(pos[1]),
        "translation_z": float(pos[2])
    }

    return cur_pose, translation_xyz


def check_landing_status(detections, padding=20):
    boxes = []
    landing_status = -1  # Default değeri

    for index, row in detections.iterrows():
        x1, y1, x2, y2 = int(row[0]), int(row[1]), int(row[2]), int(row[3])
        label = int(row[5])
        boxes.append({"label": label, "coords": (x1, y1, x2, y2)})

    target_labels = [2, 3]

    for box in boxes:
        if box["label"] in target_labels:
            bx1, by1, bx2, by2 = box["coords"]
            bx1_p, by1_p = bx1 - padding, by1 - padding
            bx2_p, by2_p = bx2 + padding, by2 + padding

            for other_box in boxes:
                if other_box["label"] in [0, 1]:
                    ox1, oy1, ox2, oy2 = other_box["coords"]
                    # other_box diğer box içinde mi?
                    if ox1 >= bx1_p and oy1 >= by1_p and ox2 <= bx2_p and oy2 <= by2_p:
                        landing_status = 0  # uygun değil
                        break
            if landing_status == 0:
                break

    return landing_status, boxes


def detect_objects(model, image_path):
    image = cv2.imread(image_path)
    image_resized = cv2.resize(image, (640, 640))
    results = model.predict(image_resized)
    boxes_tensor = results[0].boxes.data
    boxes_tensor_np = [t.cpu().numpy() for t in boxes_tensor]
    detections = pd.DataFrame(boxes_tensor_np).astype("float")

    if not detections.empty:
        landing_status, boxes = check_landing_status(detections)
    else:
        boxes = []
        landing_status = -1

    return landing_status, boxes


def response(landing_status, boxes, translation_xyz):
    detected_objects = []

    if boxes:
        for box in boxes:
            x1, y1, x2, y2 = box["coords"]
            label = box["label"]
            detected_objects.append({
                "cls": str(label),
                "landing_status": str(landing_status),
                "top_left_x": x1,
                "top_left_y": y1,
                "bottom_right_x": x2,
                "bottom_right_y": y2
            })

    return detected_objects, translation_xyz


def load_image(image_path, transform, device):
    image = Image.open(image_path).convert('RGB')
    image = transform(image)
    image = image.unsqueeze(0).to(device)
    image = image.unsqueeze(1).to(device)
    return image


def process_frames2(model, translation_model, image_path, transform, device,
                    translation_xyz={"translation_x": 0, "translation_y": 0, "translation_z": 0}, health_status=0):
    inputs = load_image(image_path, transform, device)

    landing_status, boxes = detect_objects(model, image_path)

    if health_status == 1:
        translation_xyz = translation_xyz
    else:
        with (torch.no_grad()):
            prediction_translation = translation_model(inputs)
            preds = prediction_translation.cpu().detach().numpy()
            translation_xyz = {"translation_x": float(preds[0, 0]), "translation_y": float(preds[0, 1]),
                               "translation_z": float(preds[0, 2])}

    detected_objects, translation_xyz = response(landing_status, boxes, translation_xyz)

    return detected_objects, translation_xyz
