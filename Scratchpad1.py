import numpy as np
import pandas as pd

# np.random.seed(42)  # 재현 가능성 확보 (선택)

# 100개 포인트 만들기
n_points = 100

# x 간격: 0.5 ~ 2.0 범위의 무작위 값
x_steps = np.random.uniform(0.5, 2.0, size=n_points)
x = np.cumsum(x_steps)  # 누적합으로 x 좌표 생성

# y = 20 - 0.1x + 랜덤 노이즈(-1 ~ 1)
noise = np.random.uniform(-1, 1, size=len(x))  # 랜덤값 생성
y = 20 - 0.1 * x + noise

# 데이터프레임 생성
df = pd.DataFrame({'x': x, 'y': y})

# CSV 저장
df.to_csv("linear_data_with_noise.csv", index=False)

print("CSV 파일 저장 완료: linear_data_with_noise.csv")