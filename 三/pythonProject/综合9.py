import pandas as pd
import re
from collections import Counter
from pyecharts import options as opts
from pyecharts.charts import Page, Bar, Pie, Map, WordCloud, Bar3D, Geo
from pyecharts.globals import ThemeType, ChartType
import tempfile
import os

# ====================== 读取数据 ======================
df = pd.read_csv("招聘数据_预处理后.csv", encoding='utf-8-sig')

# 核心数据
total_jobs = len(df)
avg_salary = round(df['avg_salary'].mean(), 1)
undergrad_jobs = len(df[df['education'] == '本科'])
undergrad_pct = round(undergrad_jobs / total_jobs * 100, 1)

# 薪资范围
min_salary_global = int(df['min_salary'].min())
max_salary_global = int(df['max_salary'].max())

# 城市数
city_count = df['city'].nunique()

# 浅蓝色配色
color_blue = ["#ADD8E6", "#87CEFA", "#6495ED", "#4169E1", "#1E3A8A"]
bg_color = "#F0F8FF"

# ====================== 图表1：3D柱状图 ======================
exp_edu = df.groupby(['experience', 'education'])['avg_salary'].mean().reset_index()
exp_list = exp_edu['experience'].unique().tolist()
edu_list = exp_edu['education'].unique().tolist()
data_3d = [[exp_list.index(row.experience), edu_list.index(row.education), round(row.avg_salary)] for _, row in exp_edu.iterrows()]

bar3d = (
    Bar3D(init_opts=opts.InitOpts(theme=ThemeType.LIGHT, bg_color=bg_color, width="550px", height="400px"))
    .add("", data_3d,
         xaxis3d_opts=opts.Axis3DOpts(data=exp_list, type_="category"),
         yaxis3d_opts=opts.Axis3DOpts(data=edu_list, type_="category"),
         zaxis3d_opts=opts.Axis3DOpts(type_="value"))
    .set_global_opts(title_opts=opts.TitleOpts(title="经验·学历·薪资 3D 分布", pos_left="center"))
)

# ====================== 图表2：城市薪资地图（直接使用城市数据） ======================
# 计算各城市平均薪资
city_salary = df.groupby('city')['avg_salary'].mean().round(0).reset_index()
city_salary.columns = ['city', 'avg_salary']
city_salary = city_salary.sort_values('avg_salary', ascending=False)

print("各城市平均薪资：")
print(city_salary)

# 使用 Geo 地理图，直接显示城市和数据
geo_chart = (
    Geo(init_opts=opts.InitOpts(theme=ThemeType.LIGHT, bg_color=bg_color, width="550px", height="400px"))
    .add_schema(maptype="china", itemstyle_opts=opts.ItemStyleOpts(border_color="#fff"))
    .add(
        series_name="平均薪资(元)",
        data_pair=list(zip(city_salary['city'], city_salary['avg_salary'])),
        type_=ChartType.EFFECT_SCATTER,  # 使用带涟漪效果的散点图
        symbol_size=12,
        label_opts=opts.LabelOpts(
            is_show=True,
            formatter="{b}",  # 只显示城市名称
            position="top",
            color="#333",
            font_size=10,
            font_weight="bold"
        ),
    )
    .set_series_opts(
        tooltip_opts=opts.TooltipOpts(
            trigger="item",
            formatter="{b}<br/>平均薪资: {c} 元"
        )
    )
    .set_global_opts(
        title_opts=opts.TitleOpts(title="全国城市薪资分布", pos_left="center"),
        visualmap_opts=opts.VisualMapOpts(
            min_=int(city_salary['avg_salary'].min()),
            max_=int(city_salary['avg_salary'].max()),
            range_color=["#e0f3f8", "#abd9e9", "#74add1", "#4575b4", "#313695"],
            is_calculable=True,
            pos_left="10%",
            pos_bottom="5%",
        ),
        tooltip_opts=opts.TooltipOpts(
            trigger="item",
            formatter="{b}<br/>平均薪资: {c} 元"
        ),
    )
)

# ====================== 图表3：城市岗位TOP5 ======================
city_top5 = df['city'].value_counts().head(5)
bar_city = (
    Bar(init_opts=opts.InitOpts(theme=ThemeType.LIGHT, bg_color=bg_color, width="550px", height="400px"))
    .add_xaxis(city_top5.index.tolist())
    .add_yaxis("岗位数量", city_top5.values.tolist(), color=color_blue[1])
    .set_global_opts(title_opts=opts.TitleOpts(title="城市岗位数量 Top5", pos_left="center"))
)

# ====================== 图表4：公司规模饼图 ======================
scale_cnt = df['scale'].value_counts().head(5)

pie_scale = (
    Pie(init_opts=opts.InitOpts(theme=ThemeType.LIGHT, bg_color=bg_color, width="800px", height="450px"))
    .add(
        series_name="公司规模",
        data_pair=list(zip(scale_cnt.index.tolist(), scale_cnt.values.tolist())),
        radius=["40%", "70%"],
    )
    .set_colors(color_blue)
    .set_global_opts(
        title_opts=opts.TitleOpts(title="公司规模分布", pos_left="center"),
        legend_opts=opts.LegendOpts(is_show=False),
    )
    .set_series_opts(label_opts=opts.LabelOpts(formatter="{b}: {d}%", font_size=12))
)

# ====================== 图表5：技能词云 ======================
skill_list = []
for s in df['skill']:
    if s != "未知":
        skill_list.extend([w for w in re.split(r'[ ，、；;]', str(s)) if len(w) > 1])

wordcloud = (
    WordCloud(init_opts=opts.InitOpts(bg_color=bg_color, width="800px", height="450px"))
    .add("", Counter(skill_list).most_common(40), word_size_range=[15, 60])
    .set_global_opts(title_opts=opts.TitleOpts(title="热门技能词云", pos_left="center"))
)

# ====================== 生成 HTML ======================
page = Page(layout=Page.SimplePageLayout)
page.add(bar3d, geo_chart, bar_city)
page.add(pie_scale, wordcloud)

tmp_path = tempfile.NamedTemporaryFile(delete=False, suffix='.html', mode='w', encoding='utf-8')
page.render(tmp_path.name)
tmp_path.close()

with open(tmp_path.name, 'r', encoding='utf-8') as f:
    charts_html = f.read()

body_start = charts_html.find('<body>')
body_end = charts_html.find('</body>')
chart_body = charts_html[body_start+6:body_end] if body_start != -1 and body_end != -1 else charts_html

os.unlink(tmp_path.name)

final_html = f'''<!DOCTYPE html>
<html>
<head>
    <meta charset="utf-8">
    <title>AI招聘数据看板</title>
    <style>
        * {{
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }}
        body {{
            font-family: 'Microsoft YaHei', 'PingFang SC', 'Helvetica Neue', Arial, sans-serif;
            background: linear-gradient(135deg, #f5f7fa 0%, #e8edf5 100%);
            padding: 30px 20px;
        }}
        .dashboard-container {{
            max-width: 1800px;
            margin: 0 auto;
        }}
        .main-title {{
            text-align: center;
            margin-bottom: 30px;
        }}
        .main-title h1 {{
            font-size: 42px;
            font-weight: 700;
            background: linear-gradient(120deg, #1E3A8A, #4169E1, #6495ED);
            background-clip: text;
            -webkit-background-clip: text;
            color: transparent;
            letter-spacing: 2px;
            margin-bottom: 10px;
        }}
        .main-title p {{
            color: #666;
            font-size: 16px;
            letter-spacing: 1px;
        }}
        .stats-row {{
            display: flex;
            justify-content: space-between;
            gap: 20px;
            margin-bottom: 40px;
            flex-wrap: wrap;
        }}
        .stat-card {{
            flex: 1;
            min-width: 200px;
            background: white;
            border-radius: 20px;
            padding: 25px 20px;
            text-align: center;
            box-shadow: 0 10px 30px rgba(0,0,0,0.08);
            transition: transform 0.3s ease, box-shadow 0.3s ease;
            cursor: default;
            border: 1px solid rgba(100, 148, 237, 0.2);
        }}
        .stat-card:hover {{
            transform: translateY(-5px);
            box-shadow: 0 20px 40px rgba(0,0,0,0.12);
        }}
        .stat-card .stat-number {{
            font-size: 48px;
            font-weight: 800;
            background: linear-gradient(135deg, #1E3A8A, #6495ED);
            background-clip: text;
            -webkit-background-clip: text;
            color: transparent;
            line-height: 1.2;
        }}
        .stat-card .stat-label {{
            font-size: 16px;
            color: #555;
            margin-top: 10px;
            letter-spacing: 1px;
            font-weight: 500;
        }}
        .stat-card .stat-sub {{
            font-size: 13px;
            color: #999;
            margin-top: 8px;
        }}
        .stat-card:nth-child(1) .stat-number {{ background: linear-gradient(135deg, #1E3A8A, #4169E1); background-clip: text; -webkit-background-clip: text; }}
        .stat-card:nth-child(2) .stat-number {{ background: linear-gradient(135deg, #2E5BFF, #5B8FF9); background-clip: text; -webkit-background-clip: text; }}
        .stat-card:nth-child(3) .stat-number {{ background: linear-gradient(135deg, #3498DB, #85C1F5); background-clip: text; -webkit-background-clip: text; }}
        .stat-card:nth-child(4) .stat-number {{ background: linear-gradient(135deg, #1ABC9C, #48D1CC); background-clip: text; -webkit-background-clip: text; }}
        .stat-card:nth-child(5) .stat-number {{ background: linear-gradient(135deg, #9B59B6, #C39BD3); background-clip: text; -webkit-background-clip: text; }}
        .charts-container {{
            background: transparent;
        }}
        hr {{
            margin: 10px 0 30px 0;
            border: none;
            height: 1px;
            background: linear-gradient(90deg, transparent, #ccc, transparent);
        }}
    </style>
</head>
<body>
<div class="dashboard-container">
    <div class="main-title">
        <h1>📊 AI 招聘数据分析看板</h1>
        <p>数据洞察 · 驱动决策 | 基于全国招聘数据可视化分析</p>
    </div>

    <div class="stats-row">
        <div class="stat-card">
            <div class="stat-number">{total_jobs:,}</div>
            <div class="stat-label">📋 总岗位数</div>
            <div class="stat-sub">覆盖 {city_count} 个城市</div>
        </div>
        <div class="stat-card">
            <div class="stat-number">{avg_salary}</div>
            <div class="stat-label">💰 平均月薪 (元)</div>
            <div class="stat-sub">范围 {min_salary_global:,} ~ {max_salary_global:,} 元</div>
        </div>
        <div class="stat-card">
            <div class="stat-number">{undergrad_jobs:,}</div>
            <div class="stat-label">🎓 本科岗位数</div>
            <div class="stat-sub">占比 {undergrad_pct}%</div>
        </div>
        <div class="stat-card">
            <div class="stat-number">{city_count}</div>
            <div class="stat-label">🏙️ 覆盖城市</div>
            <div class="stat-sub">全国主要城市</div>
        </div>
        <div class="stat-card">
            <div class="stat-number">{max_salary_global:,}</div>
            <div class="stat-label">⭐ 最高月薪</div>
            <div class="stat-sub">高薪岗位机会</div>
        </div>
    </div>

    <hr>

    <div class="charts-container">
        {chart_body}
    </div>
</div>
</body>
</html>'''

with open("AI招聘数据看板.html", "w", encoding="utf-8") as f:
    f.write(final_html)

print("✅ 生成成功！打开：AI招聘数据看板.html")
print(f"📊 地图包含 {len(city_salary)} 个城市的数据")
print("🏙️ 各城市薪资（前10）：")
print(city_salary.head(10).to_string(index=False))