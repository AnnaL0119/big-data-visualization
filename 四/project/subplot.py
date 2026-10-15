import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.ticker as mticker
import numpy as np

plt.rcParams['font.sans-serif'] = ['SimHei', 'Microsoft YaHei', 'DejaVu Sans']
plt.rcParams['axes.unicode_minus'] = False

# ============ 数据加载 ============
df = pd.read_csv('4 - 全球超市订单数据（难度大）--谨慎选择.csv', encoding='gbk')
cols = ['RowID','OrderID','OrderDate','ShipDate','ShipMode','CustomerID','CustomerName',
        'Segment','City','StateProvince','Country','Region','Market','ProductID',
        'Category','SubCategory','ProductName','Sales','Quantity','Discount','Profit','ShippingCost','OrderPriority']
df.columns = cols

# ============ 数据清洗与预处理 ============
# 1. 移除重复行
n_before = len(df)
df = df.drop_duplicates()
n_dup = n_before - len(df)

# 2. 转换数值列（去除 $ 和逗号）
for col in ['Sales', 'Profit']:
    df[col] = df[col].str.replace('[$,]', '', regex=True).astype(float)

# 3. 日期转换
df['OrderDate'] = pd.to_datetime(df['OrderDate'])
df['ShipDate'] = pd.to_datetime(df['ShipDate'])

# 4. 移除发货日期早于订单日期的异常记录
n_bad = (df['ShipDate'] < df['OrderDate']).sum()
df = df[df['ShipDate'] >= df['OrderDate']].copy()

# 5. 处理利润异常极端值 (IQR 方法)
Q1 = df['Profit'].quantile(0.25)
Q3 = df['Profit'].quantile(0.75)
IQR = Q3 - Q1
lower = Q1 - 3 * IQR
upper = Q3 + 3 * IQR
n_outlier = ((df['Profit'] < lower) | (df['Profit'] > upper)).sum()
df = df[(df['Profit'] >= lower) & (df['Profit'] <= upper)].copy()

# 6. 折扣率合理性检查
df = df[(df['Discount'] >= 0) & (df['Discount'] <= 1)].copy()

print(f'数据清洗完成: 移除 {n_dup} 条重复行, {n_bad} 条日期异常, {n_outlier} 条利润极端值')
print(f'剩余数据: {len(df)} 条')

# ============ 三个常量 ============
total_sales = df['Sales'].sum()
total_profit = df['Profit'].sum()
total_orders = df['OrderID'].nunique()

# ============ 创建画布 ============
fig = plt.figure(figsize=(20, 14))
fig.suptitle('全球超市订单数据分析看板', fontsize=26, fontweight='bold', y=0.96)  # 标题往下挪

# ---------- 常量展示区域 (往下挪，不重叠) ----------
ax_const = fig.add_axes([0.08, 0.88, 0.84, 0.06])  # 整体下移
ax_const.axis('off')
style1 = dict(boxstyle='round,pad=0.5', facecolor='#FFD700', alpha=0.4)
style2 = dict(boxstyle='round,pad=0.5', facecolor='#90EE90', alpha=0.4)
style3 = dict(boxstyle='round,pad=0.5', facecolor='#87CEEB', alpha=0.4)
ax_const.text(0.02, 0.5, f'总销售额: ${total_sales:,.0f}', fontsize=16, fontweight='bold',
              verticalalignment='center', bbox=style1)
ax_const.text(0.38, 0.5, f'总利润: ${total_profit:,.0f}', fontsize=16, fontweight='bold',
              verticalalignment='center', bbox=style2)
ax_const.text(0.72, 0.5, f'总订单数: {total_orders:,}', fontsize=16, fontweight='bold',
              verticalalignment='center', bbox=style3)

# ============ 六张子图 (subplot) ============

# (1) 各类别销售额 - 柱状图
ax1 = plt.subplot(3, 3, 1)
cat_sales = df.groupby('Category')['Sales'].sum().sort_values(ascending=False)
colors = ['#FF6B6B', '#4ECDC4', '#45B7D1']
bars = ax1.bar(cat_sales.index, cat_sales.values, color=colors, edgecolor='white', linewidth=1.2)
ax1.set_title('各产品类别销售额', fontsize=14, fontweight='bold')
ax1.set_ylabel('销售额 ($)')
ax1.yaxis.set_major_formatter(mticker.FuncFormatter(lambda x, _: f'${x:,.0f}'))
for bar, val in zip(bars, cat_sales.values):
    ax1.text(bar.get_x() + bar.get_width()/2, bar.get_height() + max(cat_sales.values)*0.01,
             f'${val:,.0f}', ha='center', va='bottom', fontsize=10, fontweight='bold')

# (2) 各市场销售额占比 - 饼图
ax2 = plt.subplot(3, 3, 2)
market_sales = df.groupby('Market')['Sales'].sum().sort_values(ascending=False)
ax2.pie(market_sales.values, labels=market_sales.index, autopct='%1.1f%%',
        startangle=90, colors=plt.cm.Set2(np.linspace(0, 1, len(market_sales))),
        textprops={'fontsize': 11})
ax2.set_title('各市场销售额占比', fontsize=14, fontweight='bold')

# (3) 月度销售额趋势 - 折线图
ax3 = plt.subplot(3, 3, 3)
monthly = df.set_index('OrderDate').resample('M')['Sales'].sum()
ax3.plot(monthly.index, monthly.values, color='#2196F3', linewidth=2.5, marker='o', markersize=4)
ax3.set_title('月度销售额趋势', fontsize=14, fontweight='bold')
ax3.set_ylabel('销售额 ($)')
ax3.yaxis.set_major_formatter(mticker.FuncFormatter(lambda x, _: f'${x:,.0f}'))
ax3.tick_params(axis='x', rotation=45)
ax3.grid(alpha=0.3)

# (4) 各细分市场利润 - 水平柱状图
ax4 = plt.subplot(3, 3, 4)
seg_profit = df.groupby('Segment')['Profit'].sum().sort_values(ascending=False)
bars4 = ax4.barh(seg_profit.index, seg_profit.values, color=['#FF8A80', '#80D8FF', '#CCFF90'], edgecolor='white')
ax4.set_title('各细分市场利润', fontsize=14, fontweight='bold')
ax4.set_xlabel('利润 ($)')
ax4.xaxis.set_major_formatter(mticker.FuncFormatter(lambda x, _: f'${x:,.0f}'))
for bar, val in zip(bars4, seg_profit.values):
    ax4.text(bar.get_width() + max(seg_profit.values)*0.005, bar.get_y() + bar.get_height()/2,
             f'${val:,.0f}', ha='left', va='center', fontsize=10, fontweight='bold')

# (5) 销售额 vs 利润散点图
ax5 = plt.subplot(3, 3, 5)
sample = df.sample(min(2000, len(df)), random_state=42)
sc = ax5.scatter(sample['Sales'], sample['Profit'], c=sample['Discount'], cmap='viridis',
                 alpha=0.6, s=15, edgecolors='none')
ax5.set_title('销售额 vs 利润 (颜色=折扣)', fontsize=14, fontweight='bold')
ax5.set_xlabel('销售额 ($)')
ax5.set_ylabel('利润 ($)')
ax5.xaxis.set_major_formatter(mticker.FuncFormatter(lambda x, _: f'${x:,.0f}'))
ax5.yaxis.set_major_formatter(mticker.FuncFormatter(lambda x, _: f'${x:,.0f}'))
cbar = plt.colorbar(sc, ax=ax5)
cbar.set_label('折扣率')
ax5.grid(alpha=0.3)

# (6) 各地区销售额 - 水平柱状图
ax6 = plt.subplot(3, 3, 6)
region_sales = df.groupby('Region')['Sales'].sum().sort_values(ascending=True)
bars6 = ax6.barh(region_sales.index, region_sales.values,
                 color=plt.cm.Paired(np.linspace(0, 1, len(region_sales))), edgecolor='white')
ax6.set_title('各地区销售额', fontsize=14, fontweight='bold')
ax6.set_xlabel('销售额 ($)')
ax6.xaxis.set_major_formatter(mticker.FuncFormatter(lambda x, _: f'${x:,.0f}'))
for bar, val in zip(bars6, region_sales.values):
    ax6.text(bar.get_width() + max(region_sales.values)*0.003, bar.get_y() + bar.get_height()/2,
             f'${val:,.0f}', ha='left', va='center', fontsize=9)

plt.subplots_adjust(left=0.06, right=0.97, top=0.84, bottom=0.04, hspace=0.4, wspace=0.3)
plt.savefig('dashboard_subplot.png', dpi=150, bbox_inches='tight')
print('dashboard_subplot.png 已保存')