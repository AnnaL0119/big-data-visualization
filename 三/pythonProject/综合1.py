import pandas as pd
import re
from collections import Counter
from pyecharts import options as opts
from pyecharts.charts import Page, Bar, Pie, Map, WordCloud, Bar3D
from pyecharts.globals import ThemeType

# ====================== 读取数据 ======================
df = pd.read_csv("招聘数据_预处理后.csv", encoding='utf-8-sig')

# 统计数据
total_jobs = len(df)
avg_salary = round(df['avg_salary'].mean(), 1)
undergrad_jobs = len(df[df['education'] == '本科'])

# 浅蓝色配色
color_blue = ["#ADD8E6", "#87CEFA", "#6495ED", "#4169E1", "#1E3A8A"]
bg_color = "#F0F8FF"

# ====================== 1. 城市岗位数量 Top5 柱状图 ======================
city_counts = df['city'].value_counts().head(5)
bar_city = (
    Bar(init_opts=opts.InitOpts(theme=ThemeType.LIGHT, bg_color=bg_color, width="500px", height="350px"))
    .add_xaxis(city_counts.index.tolist())
    .add_yaxis("岗位数量", city_counts.values.tolist(), color=color_blue[1])
    .set_global_opts(
        title_opts=opts.TitleOpts(title="城市岗位数量 Top5", pos_left="center"),
        xaxis_opts=opts.AxisOpts(axislabel_opts=opts.LabelOpts(rotate=0)),
        yaxis_opts=opts.AxisOpts(name="岗位数量"),
    )
)

# ====================== 2. 公司规模 环形饼图 ======================
scale_counts = df['scale'].value_counts()
pie_scale = (
    Pie(init_opts=opts.InitOpts(theme=ThemeType.LIGHT, bg_color=bg_color, width="500px", height="350px"))
    .add(series_name="公司规模", data_pair=list(zip(scale_counts.index, scale_counts.values)), radius=["30%", "70%"])
    .set_colors(color_blue)
    .set_global_opts(
        title_opts=opts.TitleOpts(title="公司规模分布", pos_left="center"),
        legend_opts=opts.LegendOpts(orient="vertical", pos_right="5%", pos_top="15%")
    )
    .set_series_opts(label_opts=opts.LabelOpts(formatter="{b}: {d}%"))
)

# ====================== 3. 全国薪资 地图 ======================
city_salary = df.groupby('city')['avg_salary'].mean().round(0).reset_index()
map_china = (
    Map(init_opts=opts.InitOpts(theme=ThemeType.LIGHT, bg_color=bg_color, width="1000px", height="450px"))
    .add(series_name="平均薪资", data_pair=list(zip(city_salary['city'], city_salary['avg_salary'])), maptype="china")
    .set_global_opts(
        title_opts=opts.TitleOpts(title="全国主要城市平均薪资分布", pos_left="center"),
        visualmap_opts=opts.VisualMapOpts(min_=city_salary['avg_salary'].min(), max_=city_salary['avg_salary'].max(), range_color=color_blue)
    )
)

# ====================== 4. 技能词云 ======================
skill_list = []
for s in df['skill']:
    if s != "未知":
        words = re.split(r'[ ，、；;]', str(s))
        skill_list.extend([w for w in words if len(w) > 1])

skill_top30 = Counter(skill_list).most_common(30)
wordcloud = (
    WordCloud(init_opts=opts.InitOpts(bg_color=bg_color, width="1000px", height="400px"))
    .add(series_name="技能词频", data_pair=skill_top30, word_size_range=[14, 60])
    .set_global_opts(title_opts=opts.TitleOpts(title="热门技能词云", pos_left="center"))
)

# ====================== 5. 3D 薪资柱状图 ======================
exp_edu = df.groupby(['experience', 'education'])['avg_salary'].mean().reset_index()
exp_list = exp_edu['experience'].unique().tolist()
edu_list = exp_edu['education'].unique().tolist()

data_3d = []
for _, row in exp_edu.iterrows():
    x = exp_list.index(row['experience'])
    y = edu_list.index(row['education'])
    z = round(row['avg_salary'], 0)
    data_3d.append([x, y, z])

bar3d = (
    Bar3D(init_opts=opts.InitOpts(theme=ThemeType.LIGHT, bg_color=bg_color, width="1000px", height="500px"))
    .add(series_name="平均薪资", data=data_3d,
         xaxis3d_opts=opts.Axis3DOpts(type_="category", data=exp_list),
         yaxis3d_opts=opts.Axis3DOpts(type_="category", data=edu_list),
         zaxis3d_opts=opts.Axis3DOpts(type_="value"))
    .set_global_opts(
        title_opts=opts.TitleOpts(title="经验·学历 薪资分布 3D", pos_left="center"),
        visualmap_opts=opts.VisualMapOpts(range_color=color_blue)
    )
)

# ====================== 组合成看板（已修复HTML报错） ======================
page = Page(layout=Page.SimplePageLayout)

# 直接添加图表，去掉报错的HTML
page.add(
    bar3d,
    map_china,
    bar_city,
    pie_scale,
    wordcloud
)

# 生成HTML
page.render("招聘数据可视化看板.html")
print("✅ 运行成功！已生成：招聘数据可视化看板.html")