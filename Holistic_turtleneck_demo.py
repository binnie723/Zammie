import cv2
import mediapipe as mp
import numpy as np
import datetime
import os

# MediaPipe 초기화
mp_face_mesh = mp.solutions.face_mesh
face_mesh = mp_face_mesh.FaceMesh(min_detection_confidence=0.5, min_tracking_confidence=0.5)

# 웹캠 초기화 (두 대의 웹캠)
cap_front = cv2.VideoCapture(2)  # 정면 웹캠
cap_side = cv2.VideoCapture(0)  # 옆면 웹캠

# 거북목 감지 관련 변수
NECK_THRESHOLD = 0.35
FOREHEAD_INDEX = 10
captured = False

# 이미지 저장 디렉토리 생성
save_directory = "static/images"
if not os.path.exists(save_directory):
    os.makedirs(save_directory)

def cartoonize_image(img):
    # 이미지를 회색조로 변환하고 블러 처리
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    gray_blur = cv2.medianBlur(gray, 7)

    # 가장자리 검출
    edges = cv2.adaptiveThreshold(gray_blur, 255,
                                  cv2.ADAPTIVE_THRESH_MEAN_C,
                                  cv2.THRESH_BINARY, 9, 9)

    # 컬러 이미지를 다운스케일링하여 색상을 단순화
    color = cv2.bilateralFilter(img, 9, 300, 300)

    # 만화 스타일로 이미지 병합
    cartoon = cv2.bitwise_and(color, color, mask=edges)
    return cartoon

while cap_front.isOpened() and cap_side.isOpened():
    ret_front, frame_front = cap_front.read()
    ret_side, frame_side = cap_side.read()

    if not ret_front or not ret_side:
        continue

    # 정면 이미지 처리
    image_front = cv2.cvtColor(frame_front, cv2.COLOR_BGR2RGB)
    image_front.flags.writeable = False
    results_front = face_mesh.process(image_front)

    image_front.flags.writeable = True
    image_front = cv2.cvtColor(image_front, cv2.COLOR_RGB2BGR)

    if results_front.multi_face_landmarks:
        for face_landmarks in results_front.multi_face_landmarks:
            landmarks = face_landmarks.landmark

            # 거북목 감지
            forehead = (landmarks[FOREHEAD_INDEX].x, landmarks[FOREHEAD_INDEX].y)
            nose_tip = (landmarks[1].x, landmarks[1].y)
            neck_length = abs(forehead[1] - nose_tip[1])

            if neck_length > NECK_THRESHOLD and not captured:
                cv2.putText(image_front, "TURTLE NECK DETECTED!", (10, 30),
                            cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 255), 2)

                # 옆면 이미지 카툰화 및 저장
                cartoon_image = cartoonize_image(frame_side)
                filename = datetime.datetime.now().strftime("image.jpg")
                filepath = os.path.join(save_directory, filename)
                cv2.imwrite(filepath, cartoon_image)

                captured = True
            elif neck_length <= NECK_THRESHOLD:
                captured = False

    cv2.imshow('Front Camera', image_front)
    cv2.imshow('Side Camera', frame_side)

    if cv2.waitKey(5) & 0xFF == ord('q'):
        break

cap_front.release()
cap_side.release()
cv2.destroyAllWindows()

