import sys

# thread_counts = [1, 2, 4, 8, 16, 32, 64]
thread_counts = sys.argv[1:]

for p in thread_counts:
    input_file = f'res_{p}'   # 기존 파일
    output_file = f'res_filt_{p}' # 결과를 저장할 파일

    with open(input_file, 'r') as infile, open(output_file, 'w') as outfile:
        for line in infile:
            # "user"와 "sys"가 포함된 행을 제외하고 쓰기
            if not line.startswith("user") and not line.startswith("sys"):
                if line.startswith("real"):
                    line = line.replace("real", "").replace("0m", "").replace("s", "").strip() + '\n'

                outfile.write(line)
