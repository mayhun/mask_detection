# 🚀 마스크 착용 탐지
> (2021년 저작권 보호기술 팀 프로젝트) 코로나 시기에 마스크 착용 의무화로 인해 AI를 활용한 마스크 착용 탐지 시스템

![Python](https://img.shields.io/badge/Python-3766AB?style=flat-square&logo=Python&logoColor=white)
![Arduino](https://img.shields.io/badge/Arduino-00979D?style=flat-square&logo=Arduino&logoColor=white)

## 📝 프로젝트 소개
코로나가 활발한 시기에 국가적 차원에서 마스크 착용을 의무화를 시행했지만, 일부 사람들은 마스크를 착용하지 않은채 건물을 출입하는 일이 빈번히 일어났다. 간혹 마스크 착용을 확인하는 인원이 배치되어있으나, 많은 사람의 얼굴을 사람이 직접 확인하는 일은 많은 인력과 비용이 발생한다. 이러한 문제점을 해결하고자, Arduino 카메라 모듈과 인공지능을 사용하여 마스크 판별 시스템을 만들고자 한다.

## 데이터
Selenium을 사용하여 이미지 데이터 수집  
크롤링 코드 유실


## 🧠 모델 구조 및 설명

본 프로젝트에서는 이미지 분류 분야에서 널리 사용되는 **ResNet50 (Residual Network 50-layer)**을 기반으로 한 전이 학습(Transfer Learning) 모델을 사용하였습니다.

ResNet50은 마이크로소프트 연구소에서 제안한 딥러닝 모델로, **잔차 학습(Residual Learning)** 구조를 통해 깊은 네트워크에서도 기울기 소실 문제 없이 안정적인 학습이 가능한 특징을 갖습니다. 특히, 다양한 이미지 인식 대회에서 우수한 성능을 입증한 모델로, 사전 학습된 가중치를 활용하면 적은 데이터로도 높은 성능을 얻을 수 있습니다.

### ✅ 모델 구성

- **기본 모델**: `ResNet50`
  - `weights='imagenet'`: ImageNet 데이터셋으로 사전 학습된 가중치 사용
  - `include_top=False`: 기존 분류기(FC 레이어)는 제거
  - `trainable=False`: 사전 학습된 ResNet50은 학습하지 않고 고정 (Feature Extractor로 활용)

- **커스텀 분류기(Head)**:
  - `Flatten()`: ResNet50의 출력 feature map을 1차원 벡터로 변환
  - `Dense(128, activation='relu')`: 은닉층
  - `BatchNormalization()`: 학습 안정화 및 과적합 방지
  - `Dense(1, activation='sigmoid')`: 이진 분류 (마스크 착용 여부)

```plaintext
입력 이미지 (224x224x3)
        ↓
[ResNet50: 사전학습된 feature extractor]
        ↓
Flatten → Dense(128) → BatchNormalization → Dense(1, sigmoid)
        ↓
출력 (1: 마스크 착용 / 0: 미착용)
```

## 한계점
손 또는 다른 물건으로 입을 가리는 경우도 마스크 착용으로 인식하는 오류

// 프로젝트 당시(2021년) 메모리 64GB 서버에서 학습을 수행하였으며, 현재(2025년) 재 구현을 해보려하였으나, 현재 개인 홈 서버(RAM 16GB)에서 학습 불가, colab으로도 메모리 부족으로 인해 학습 수행한 모델로 탐지 구현 진행.

## 📂 **프로젝트 구조**
```
📂 mask_detection
├── 📂 Arduino_source/ 
│ 
├── final_mask_detection_Arduino.ipynb # python + Arduino 최종 코드
│ 
├── mask_detector.py # python으로만 이루어진 테스트 코드(2025 code refactor)
│ 
├── model_train.py # resnet50 학습 코드
│ 
├── README.md # 프로젝트 설명서 
│ 
└── requirements.txt # 필요한 Python 패키지 목록
```