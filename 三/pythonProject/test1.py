import pandas as pd

# 读取数据
df = pd.read_csv("招聘数据_预处理后.csv", encoding='utf-8-sig')

# 查看所有唯一的城市
cities = df['city'].unique()
print(f"共有 {len(cities)} 个城市")
print("\n所有城市列表：")
for city in sorted(cities):
    print(f"  - {city}")

# 查看每个城市的岗位数和平均薪资
city_stats = df.groupby('city')['avg_salary'].agg(['count', 'mean']).round(0).sort_values('count', ascending=False)
print("\n各城市岗位数及平均薪资：")
print(city_stats.head(20))