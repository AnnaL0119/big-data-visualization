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
total_quantity = df['Quantity'].sum()

# ============ 创建画布 ============
fig = plt.figure(figsize=(20, 14))
# 总标题下移，拉开与统计卡片距离
fig.suptitle('全球超市订单数据分析看板', fontsize=26, fontweight='bold', y=0.95)

# ---------- 常量展示区域：居中对齐，左右边界和图表匹配 ----------
# ax_const = fig.add_axes([0.12, 0.86, 0.76, 0.06])
# ax_const.axis('off')
# style1 = dict(boxstyle='round,pad=0.5', facecolor='#FFD700', alpha=0.4)
# style2 = dict(boxstyle='round,pad=0.5', facecolor='#90EE90', alpha=0.4)
# style3 = dict(boxstyle='round,pad=0.5', facecolor='#87CEEB', alpha=0.4)
# ax_const.text(0.02, 0.5, f'总销售额: ${total_sales:,.0f}', fontsize=16, fontweight='bold',
#               verticalalignment='center', bbox=style1)
# ax_const.text(0.36, 0.5, f'总利润: ${total_profit:,.0f}', fontsize=16, fontweight='bold',
#               verticalalignment='center', bbox=style2)
# ax_const.text(0.70, 0.5, f'总数量: {total_quantity:,}', fontsize=16, fontweight='bold',
#               verticalalignment='center', bbox=style3)
ax_const = fig.add_axes([0.06, 0.86, 0.88, 0.06])
ax_const.axis('off')
style1 = dict(boxstyle='round,pad=0.5', facecolor='#FFD700', alpha=0.4)
style2 = dict(boxstyle='round,pad=0.5', facecolor='#90EE90', alpha=0.4)
style3 = dict(boxstyle='round,pad=0.5', facecolor='#87CEEB', alpha=0.4)

# 左列居中
ax_const.text(0.25, 0.5, f'总销售额: ${total_sales:,.0f}', fontsize=16, fontweight='bold',
              verticalalignment='center', ha='center', bbox=style1)
# 页面正中间
ax_const.text(0.50, 0.5, f'总利润: ${total_profit:,.0f}', fontsize=16, fontweight='bold',
              verticalalignment='center', ha='center', bbox=style2)
# 右列居中
ax_const.text(0.75, 0.5, f'总数量: {total_quantity:,}', fontsize=16, fontweight='bold',
              verticalalignment='center', ha='center', bbox=style3)
# ============ 六张子图 (subplot2grid 6行4列) ============
# (1) 各类别利润 - 柱状图 (row 0-1, col 0-1)
ax1 = plt.subplot2grid((6, 4), (0, 0), rowspan=2, colspan=2)
cat_profit = df.groupby('Category')['Profit'].sum().sort_values(ascending=False)
colors1 = ['#FF6B6B', '#4ECDC4', '#45B7D1']
bars1 = ax1.bar(cat_profit.index, cat_profit.values, color=colors1, edgecolor='white', linewidth=1.2)
ax1.set_title('各产品类别利润', fontsize=14, fontweight='bold')
ax1.set_ylabel('利润 ($)')
ax1.yaxis.set_major_formatter(mticker.FuncFormatter(lambda x, _: f'${x:,.0f}'))
for bar, val in zip(bars1, cat_profit.values):
    ax1.text(bar.get_x() + bar.get_width()/2, bar.get_height() + max(cat_profit.values)*0.01,
             f'${val:,.0f}', ha='center', va='bottom', fontsize=10, fontweight='bold')

# (2) 各细分市场销售额 - 柱状图 (row 0-1, col 2-3)
ax2 = plt.subplot2grid((6, 4), (0, 2), rowspan=2, colspan=2)
seg_sales = df.groupby('Segment')['Sales'].sum().sort_values(ascending=False)
colors2 = ['#FF8A80', '#80D8FF', '#CCFF90']
bars2 = ax2.bar(seg_sales.index, seg_sales.values, color=colors2, edgecolor='white', linewidth=1.2)
ax2.set_title('各细分市场销售额', fontsize=14, fontweight='bold')
ax2.set_ylabel('销售额 ($)')
ax2.yaxis.set_major_formatter(mticker.FuncFormatter(lambda x, _: f'${x:,.0f}'))
for bar, val in zip(bars2, seg_sales.values):
    ax2.text(bar.get_x() + bar.get_width()/2, bar.get_height() + max(seg_sales.values)*0.005,
             f'${val:,.0f}', ha='center', va='bottom', fontsize=10, fontweight='bold')

# (3) 月度销售额趋势 - 折线图 (row 2-3, col 0-2)
ax3 = plt.subplot2grid((6, 4), (2, 0), rowspan=2, colspan=2)
monthly = df.set_index('OrderDate').resample('M')['Sales'].sum()
ax3.plot(monthly.index, monthly.values, color='#2196F3', linewidth=2.5, marker='o', markersize=3)
ax3.set_title('月度销售额趋势', fontsize=14, fontweight='bold')
ax3.set_ylabel('销售额 ($)')
ax3.yaxis.set_major_formatter(mticker.FuncFormatter(lambda x, _: f'${x:,.0f}'))
ax3.tick_params(axis='x', rotation=45)
ax3.grid(alpha=0.3)

# (4) 各市场销售额占比 - 饼图 (row 2-3, col 2-3)
ax4 = plt.subplot2grid((6, 4), (2, 2), rowspan=2, colspan=2)
market_sales = df.groupby('Market')['Sales'].sum().sort_values(ascending=False)
ax4.pie(market_sales.values, labels=market_sales.index, autopct='%1.1f%%',
        startangle=90, colors=plt.cm.Set2(np.linspace(0, 1, len(market_sales))),
        textprops={'fontsize': 11})
ax4.set_title('各市场销售额占比', fontsize=14, fontweight='bold')

# (5) 销售额 vs 利润散点图 (row 4-5, col 0-2)
ax5 = plt.subplot2grid((6, 4), (4, 0), rowspan=2, colspan=2)
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

# (6) Top 10 国家销售额 - 水平柱状图 (row 4-5, col 2-3)
ax6 = plt.subplot2grid((6, 4), (4, 2), rowspan=2, colspan=2)
top10 = df.groupby('Country')['Sales'].sum().sort_values(ascending=True).tail(10)
bars6 = ax6.barh(top10.index, top10.values,
                 color=plt.cm.Paired(np.linspace(0, 1, len(top10))), edgecolor='white')
ax6.set_title('Top 10 国家销售额', fontsize=14, fontweight='bold')
ax6.set_xlabel('销售额 ($)')
ax6.xaxis.set_major_formatter(mticker.FuncFormatter(lambda x, _: f'${x:,.0f}'))
for bar, val in zip(bars6, top10.values):
    ax6.text(bar.get_width() + max(top10.values)*0.002, bar.get_y() + bar.get_height()/2,
             f'${val:,.0f}', ha='left', va='center', fontsize=9)

# 顶部留白加大，垂直间距宽松
plt.subplots_adjust(left=0.06, right=0.97, top=0.82, bottom=0.04, hspace=0.42, wspace=0.3)
plt.savefig('dashboard_subplot2grid.png', dpi=150, bbox_inches='tight')
print('dashboard_subplot2grid.png 已保存')