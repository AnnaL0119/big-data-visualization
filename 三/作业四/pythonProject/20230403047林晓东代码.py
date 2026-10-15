# -*- coding: utf-8 -*-
import pandas as pd

# ---------------------- 1. 读取数据（自动适配编码） ----------------------
def safe_read_csv(path):
    encodings = ["gbk", "gb2312", "utf-8-sig", "utf-8", "gb18030"]
    for enc in encodings:
        try:
            return pd.read_csv(path, encoding=enc)
        except (UnicodeDecodeError, LookupError):
            continue
    raise ValueError("文件读取失败，请检查文件路径和编码")

# 读取数据
df = safe_read_csv("bj_lianJia.csv")

print("=" * 60)
print("原始数据信息：")
print("数据形状（行, 列）：", df.shape)
print("列名列表：")
print(df.columns.tolist())
print("\n每列缺失值数量：")
print(df.isnull().sum())
print("=" * 60)

# ---------------------- 2. 按作业要求填充缺失值 ----------------------
# 遍历每一列，按数据类型处理
for col in df.columns:
    # 判断列的数据类型
    if pd.api.types.is_numeric_dtype(df[col]):
        # 数值型：用列的平均值填充，保留两位小数
        fill_value = round(df[col].mean(), 2)
        df[col] = df[col].fillna(fill_value)
        print(f"✅ 数值列【{col}】已用平均值 {fill_value} 填充缺失值")
    else:
        # 非数值型：用前向填充（缺失值之前的最后一个有效值）
        df[col] = df[col].fillna(method="ffill")
        print(f"✅ 非数值列【{col}】已用前向填充处理缺失值")

# ---------------------- 3. 验证结果并保存 ----------------------
print("\n" + "=" * 60)
print("处理后每列缺失值数量：")
print(df.isnull().sum())
print("=" * 60)

# 保存处理后的数据
df.to_csv("bj_lianJia_填充完成.csv", index=False, encoding="utf-8-sig")
print("\n✅ 缺失值填充完成！已保存为：bj_lianJia_填充完成.csv")