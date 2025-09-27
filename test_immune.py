import torch
import ImmuneBuilder
from ImmuneBuilder import ABodyBuilder2

print("=== PyTorch ===")
print("PyTorch version:", torch.__version__)
print("CUDA available:", torch.cuda.is_available())

print("\n=== ImmuneBuilder ===")
print("ImmuneBuilder imported:", ImmuneBuilder is not None)

# ABodyBuilder2 がクラスかどうかを確認
print("ABodyBuilder2 type:", type(ABodyBuilder2))

# インスタンス化できるか確認
try:
    builder = ABodyBuilder2()
    print("ABodyBuilder2 instance created successfully:", type(builder))
except Exception as e:
    print("ABodyBuilder2 instantiation failed:", e)

print("\n✅ ABodyBuilder2 test completed.")

