import cv2
import os
import datetime
import mediapipe as mp

# MediaPipe 초기화
mp_pose = mp.solutions.pose
pose = mp_pose.Pose(min_detection_confidence=0.5, min_tracking_confidence=0.5)

# 웹캠 초기화 (옆면 웹캠)
cap_side = cv2.VideoCapture(0)

# 이미지 저장 디렉토리 생성
save_directory = "static/images"
if not os.path.exists(save_directory):
    os.makedirs(save_directory)

# 거북목 감지 관련 변수
NECK_THRESHOLD = 0.35
captured = False

# 이전 캡쳐 시간 초기화
last_capture_time = datetime.datetime.now()

def is_turtle_neck(landmarks):
    # 거북목 감지
    left_shoulder = landmarks[mp_pose.PoseLandmark.LEFT_SHOULDER.value].y
    left_hip = landmarks[mp_pose.PoseLandmark.LEFT_HIP.value].y
    right_shoulder = landmarks[mp_pose.PoseLandmark.RIGHT_SHOULDER.value].y
    right_hip = landmarks[mp_pose.PoseLandmark.RIGHT_HIP.value].y

    neck_length = max(left_shoulder, right_shoulder) - min(left_hip, right_hip)
    return neck_length > NECK_THRESHOLD

while cap_side.isOpened():
    ret_side, frame_side = cap_side.read()

    if not ret_side:
        continue

    # 옆모습 이미지 처리
    image_side = cv2.cvtColor(frame_side, cv2.COLOR_BGR2RGB)
    image_side.flags.writeable = False
    results_side = pose.process(image_side)

    image_side.flags.writeable = True
    image_side = cv2.cvtColor(image_side, cv2.COLOR_RGB2BGR)

    # 사람을 감지한 경우
    if results_side.pose_landmarks and is_turtle_neck(results_side.pose_landmarks):
        current_time = datetime.datetime.now()
        # 현재 시간과 이전 캡쳐 시간을 비교하여 10초마다 캡쳐
        if (current_time - last_capture_time).total_seconds() >= 10:
            # 이미지 저장
            filename = current_time.strftime("image.jpg")
            filepath = os.path.join(save_directory, filename)
            cv2.imwrite(filepath, frame_side)
            last_capture_time = current_time  # 캡쳐 시간 업데이트

    cv2.imshow('Side Camera', image_side)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap_side.release()
cv2.destroyAllWindows()

