#!/bin/bash

gcc -o parallel_sum parallel_sum.c -pthread

# 배열에 스레드 개수 옵션 정의
thread_counts=(1 2 4 8 16 32 64)

# 각 스레드 개수에 대해 10번씩 실행
for threads in "${thread_counts[@]}"; do
    output_file="res_$threads"
    
    # 기존 파일 초기화
    > "$output_file"
    
    for i in {1..10}; do
        echo "Running with $threads threads, iteration $i"
        { time ./parallel_sum 100000000 "$threads"; } >> "$output_file" 2>&1
    done
done

python3 result_filtering.py "${thread_counts[@]}"
python3 draw_graph.py "${thread_counts[@]}"

rm res_* parallel_sum