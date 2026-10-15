# -*- coding: utf-8 -*-
import pandas as pd

# ---------------------- 1. 读取数据（自动编码） ----------------------
def load_data(path):
    encodings = ["gbk", "gb2312", "utf-8-sig", "utf-8", "gb18030"]
    for e in encodings:
        try:
            return pd.read_csv(path, encoding=e)
        except:
            continue
    raise Exception("编码读取失败")

df = load_data("bj_lianJia.csv")

# ---------------------- 2. 查看缺失情况 ----------------------
print("===== 数据基本信息 =====")
print("形状：", df.shape)
print("列名：", df.columns.tolist())

print("\n===== 缺失值统计 =====")
missing_info = df.isnull().sum()
print(missing_info)

# ---------------------- 3. 分别填充：数值→均值，文本→众数 ----------------------
# 数值列：均值填充
num_cols = df.select_dtypes(include=["float64", "int64"]).columns
for col in num_cols:
    df[col] = df[col].fillna(df[col].mean())
    print(f"数值列【{col}】→ 均值填充完成")

# 文本/分类列：众数填充
str_cols = df.select_dtypes(include=["object"]).columns
for col in str_cols:
    df[col] = df[col].fillna(df[col].mode()[0])
    print(f"文本列【{col}】→ 众数填充完成")

# ---------------------- 4. 验证并保存 ----------------------
print("\n===== 填充后缺失值检查 =====")
print(df.isnull().sum())

df.to_csv("bj_lianJia_已填充.csv", index=False, encoding="utf-8-sig")
print("\n✅ 数据已保存为：bj_lianJia_已填充.csv")