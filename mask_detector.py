import cv2
import numpy as np
import cvlib as cv
from tensorflow.keras.models import load_model
from tensorflow.keras.applications.resnet50 import preprocess_input
from tensorflow.keras.preprocessing.image import img_to_array
import os

class MaskDetector:
    def __init__(self, model_path='saved_model_mayhun.h5', cam_index=0):
        # 사전 학습된 마스크 탐지 모델 로드
        print(f"{os.path.basename(model_path)} load start")
        self.model = load_model(model_path)
        print("model load success")
        # 웹캠 연결
        self.webcam = cv2.VideoCapture(cam_index)
        if not self.webcam.isOpened():
            raise RuntimeError("Could not open webcam.")

    def preprocess_face(self, face_img):
        """
        얼굴 이미지를 모델 입력 형식(224x224 RGB)으로 전처리
        """
        face_resized = cv2.resize(face_img, (224, 224), interpolation=cv2.INTER_AREA)
        x = img_to_array(face_resized)
        x = np.expand_dims(x, axis=0)  # 배치 차원 추가
        x = preprocess_input(x)        # ResNet50 기준 전처리
        return x

    def predict(self, face_img):
        """
        얼굴 이미지에 대한 마스크 착용 여부 예측
        반환값:
        - is_no_mask: True이면 마스크 미착용, False이면 마스크 착용
        - confidence: 모델이 예측한 확률 값
        """
        processed = self.preprocess_face(face_img)
        prediction = self.model.predict(processed)
        is_no_mask = prediction[0][0] < 0.5  # 0: 미착용, 1: 착용
        confidence = prediction[0][0]
        return is_no_mask, confidence

    def draw_result(self, frame, box, is_no_mask, confidence):
        """
        예측 결과를 영상에 시각적으로 표시
        - 얼굴 영역에 색깔 박스와 라벨 텍스트 표시
        """
        (startX, startY, endX, endY) = box
        Y = startY - 10 if startY - 10 > 10 else startY + 10

        if is_no_mask:
            label = f"No Mask ({(1 - confidence) * 100:.2f}%)"
            color = (0, 0, 255)  # 빨간색: 마스크 없음
        else:
            label = f"Mask ({confidence * 100:.2f}%)"
            color = (0, 255, 0)  # 초록색: 마스크 있음

        # 얼굴 영역 사각형과 라벨 출력
        cv2.rectangle(frame, (startX, startY), (endX, endY), color, 2)
        cv2.putText(frame, label, (startX, Y), cv2.FONT_HERSHEY_SIMPLEX, 0.7, color, 2)

    def run(self):
        """
        실시간 웹캠 스트리밍을 통해 마스크 탐지 실행
        """
        while self.webcam.isOpened():
            status, frame = self.webcam.read()
            if not status:
                print("Could not read frame.")
                break

            # 얼굴 탐지 (cvlib 사용)
            faces, _ = cv.detect_face(frame)

            for f in faces:
                (startX, startY, endX, endY) = f
                # 얼굴 영역이 프레임 범위 내에 있는지 확인
                if 0 <= startX <= frame.shape[1] and 0 <= endX <= frame.shape[1] and \
                    0 <= startY <= frame.shape[0] and 0 <= endY <= frame.shape[0]:

                    # 얼굴 영역 크롭
                    face_region = frame[startY:endY, startX:endX]
                    # 마스크 착용 예측
                    is_no_mask, confidence = self.predict(face_region)
                    # 결과 시각화
                    self.draw_result(frame, f, is_no_mask, confidence)

            # 결과 영상 출력
            cv2.imshow("Mask Detection", frame)

            # 'q' 키 누르면 종료
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break

        # 자원 정리
        self.webcam.release()
        cv2.destroyAllWindows()

# 실행 시작
if __name__ == "__main__":
    detector = MaskDetector(model_path='saved_model.h5')
    detector.run()
