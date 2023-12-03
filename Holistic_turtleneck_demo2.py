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

# 캡쳐 간격 설정
capture_interval = 10  # 10초마다 캡쳐

# 이전 캡쳐 시간 초기화
last_capture_time = datetime.datetime.now()

def is_person_detected(landmarks):
    # 사람 감지
    return landmarks is not None

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
    if is_person_detected(results_side.pose_landmarks):
        current_time = datetime.datetime.now()
        # 현재 시간과 이전 캡쳐 시간을 비교하여 10초마다 캡쳐
        if (current_time - last_capture_time).total_seconds() >= capture_interval:
            # 골격 랜드마크 연결
            mp_drawing = mp.solutions.drawing_utils
            image_side_with_skeleton = frame_side.copy()
            mp_drawing.draw_landmarks(image_side_with_skeleton, results_side.pose_landmarks, mp_pose.POSE_CONNECTIONS)

            # 이미지 저장
            cartoon_image = cartoonize_image(image_side_with_skeleton)
            filename = datetime.datetime.now().strftime("image.jpg")
            filepath = os.path.join(save_directory, filename)
            cv2.imwrite(filepath, cartoon_image)

    cv2.imshow('Side Camera', image_side)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap_side.release()
cv2.destroyAllWindows()

