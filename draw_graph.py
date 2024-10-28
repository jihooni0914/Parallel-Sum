import numpy as np
import matplotlib.pyplot as plt
import sys

# 쓰레드 수와 파일 이름 정의
# threads = [1, 2, 4, 8, 16, 32, 64]
threads = sys.argv[1:]
only_parallel_avg = []
total_program_avg = []

# 각 파일에서 데이터를 읽어 평균을 계산
for t in threads:
    filename = f'res_filt_{t}'
    only_parallel_times = []
    total_program_times = []

    # 파일에서 각 시간 데이터 추출
    with open(filename, 'r') as f:
        lines = f.readlines()
        for i in range(0, len(lines), 2):
            only_parallel_time = float(lines[i].strip())
            total_program_time = float(lines[i + 1].strip())
            
            only_parallel_times.append(only_parallel_time)
            total_program_times.append(total_program_time)
    
    # 평균 계산
    only_parallel_avg.append(np.mean(only_parallel_times))
    total_program_avg.append(np.mean(total_program_times))

# 차이값 (total program time - only parallel sum time)
difference = np.array(total_program_avg) - np.array(only_parallel_avg)

# 그래프 생성
fig, ax = plt.subplots(figsize=(10, 6))
bar_width = 0.6
bar1 = ax.bar(threads, only_parallel_avg, bar_width, label='Only Parallel Sum', color='skyblue')

# 그래프 레이블 및 제목
ax.set_xlabel('Number of Threads')
ax.set_ylabel('Elapsed Time (seconds)')
ax.set_title('Elapsed Time by Number of Threads')
ax.set_xticks(threads)
ax.legend()

# 그래프 이미지 파일로 저장
plt.savefig("elapsed_time_by_threads_1.png")

######################################################

plt.clf()
fig, ax = plt.subplots(figsize=(10, 6))
bar_width = 0.6

bar2 = ax.bar(threads, only_parallel_avg, bar_width, bottom=difference, label='Only Parallel Sum', color='skyblue')
bar3 = ax.bar(threads, difference, bar_width, label='Other Program Tasks', color='orange')

# 그래프 레이블 및 제목
ax.set_xlabel('Number of Threads')
ax.set_ylabel('Elapsed Time (seconds)')
ax.set_title('Elapsed Time by Number of Threads')
ax.set_xticks(threads)
ax.legend()

# 그래프 이미지 파일로 저장
plt.savefig("elapsed_time_by_threads_2.png")