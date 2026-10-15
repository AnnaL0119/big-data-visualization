import pandas as pd
import matplotlib.pyplot as plt

# 中文显示
plt.rcParams['font.sans-serif'] = ['SimHei']
plt.rcParams['axes.unicode_minus'] = False

# 读取数据
df = pd.read_csv('data_process.csv')

# 统计各城市岗位数并取前五
top5_city_num = df['city'].value_counts().head(5)
print("===== 岗位数量排行前五的城市 =====")
print(top5_city_num)

# 绘图
plt.figure(figsize=(10, 6), dpi=150)
colors = ['#FF9999', '#66B2FF', '#99FF99', '#FFCC99', '#FF99CC']

bars = plt.bar(
    top5_city_num.index,
    top5_city_num.values,
    color=colors,
    edgecolor='black',
    linewidth=1.5
)

# 在柱子上标注数量
for bar in bars:
    height = bar.get_height()
    plt.text(
        bar.get_x() + bar.get_width()/2.,
        height + 5,
        f'{int(height)}',
        ha='center', va='bottom', fontsize=12, fontweight='bold'
    )

plt.title('AI岗位 数量排行 TOP5 城市', fontsize=16, pad=20, fontweight='bold')
plt.xlabel('城市', fontsize=12)
plt.ylabel('岗位数量', fontsize=12)
plt.ylim(0, top5_city_num.max() * 1.15)
plt.grid(axis='y', alpha=0.3)
plt.tight_layout()

# 保存高清图
plt.savefig('top5城市岗位数量排行.png', dpi=300, bbox_inches='tight')
plt.show()

print("\n✅ 图片已保存：top5城市岗位数量排行.png")