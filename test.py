import sys

if len(sys.argv) > 2:
    x = sys.argv[1]
    y = sys.argv[2]
    print(f"Received x={x} and y={y}")
    # 执行其他操作
else:
    print("Not enough arguments provided")