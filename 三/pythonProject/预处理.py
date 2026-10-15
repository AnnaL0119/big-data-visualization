import pandas as pd
import numpy as np

# 1. 读取CSV文件
df = pd.read_csv('E:\大三下学期\大数据可视化技术\三\pythonProject\招聘数据.csv')

# 2. 查看数据基本信息（包括空值情况）
print("=" * 50)
print("数据基本信息")
print("=" * 50)
print(f"数据形状：{df.shape} (行数, 列数)")
print("\n数据列名：")
print(df.columns.tolist())
print("\n数据类型：")
print(df.dtypes)
print("\n空值统计：")
null_counts = df.isnull().sum()
null_percentage = (df.isnull().sum() / len(df)) * 100
null_df = pd.DataFrame({
    '空值数量': null_counts,
    '空值占比(%)': round(null_percentage, 2)
})
print(null_df[null_df['空值数量'] > 0])  # 只显示有空值的列

# 3. 展示原始数据前四行（包含空值）
print("\n" + "=" * 50)
print("原始数据前四行（包含空值）")
print("=" * 50)
print(df.head(4))

# 4. 数据预处理 - 处理空值
print("\n" + "=" * 50)
print("开始处理空值")
print("=" * 50)

# 创建预处理后的数据副本
df_processed = df.copy()

# 根据不同数据类型采用不同的空值处理策略
for col in df_processed.columns:
    if df_processed[col].dtype == 'object':  # 字符串/分类类型
        # 用"未知"填充字符串类型的空值
        fill_value = "未知"
        df_processed[col].fillna(fill_value, inplace=True)
        print(f"列 {col} (字符串类型)：用'{fill_value}'填充空值")

    elif df_processed[col].dtype in ['int64', 'float64']:  # 数值类型
        # 用中位数填充数值类型的空值（中位数对异常值更稳健）
        fill_value = df_processed[col].median()
        df_processed[col].fillna(fill_value, inplace=True)
        print(f"列 {col} (数值类型)：用中位数'{fill_value}'填充空值")

# 5. 验证空值处理结果
print("\n" + "=" * 50)
print("空值处理结果验证")
print("=" * 50)
remaining_nulls = df_processed.isnull().sum().sum()
print(f"处理后剩余空值总数：{remaining_nulls}")
if remaining_nulls == 0:
    print("✅ 所有空值已成功处理")
else:
    print("❌ 仍有部分空值未处理")
    print("未处理的空值分布：")
    print(df_processed.isnull().sum()[df_processed.isnull().sum() > 0])

# 6. 展示预处理后的数据前四行
print("\n" + "=" * 50)
print("预处理后的数据前四行")
print("=" * 50)
print(df_processed.head(4))

# 7. 保存预处理后的数据（可选）
output_path = '招聘数据_预处理后.csv'
df_processed.to_csv(output_path, index=False, encoding='utf-8-sig')
print(f"\n✅ 预处理后的数据已保存至：{output_path}")