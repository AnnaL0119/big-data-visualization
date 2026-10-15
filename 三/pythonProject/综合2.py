import pandas as pd
import re
from collections import Counter
from pyecharts import options as opts
from pyecharts.charts import Page, Bar, Pie, Map, WordCloud, Bar3D
from pyecharts.globals import ThemeType

# ====================== 读取数据 ======================
df = pd.read_csv("招聘数据_预处理后.csv", encoding='utf-8-sig')

# 核心统计数据
total_jobs = len(df)
avg_salary = round(df['avg_salary'].mean(), 1)
undergrad_jobs = len(df[df['education'] == '本科'])

# 浅蓝色配色
color_blue = ["#ADD8E6", "#87CEFA", "#6495ED", "#4169E1", "#1E3A8A"]
bg_color = "#F0F8FF"

# ====================== 1. 3D 薪资图表 ======================
exp_edu = df.groupby(['experience', 'education'])['avg_salary'].mean().reset_index()
exp_list = exp_edu['experience'].unique().tolist()
edu_list = exp_edu['education'].unique().tolist()
data_3d = [[exp_list.index(row.experience), edu_list.index(row.education), round(row.avg_salary)] for _, row in exp_edu.iterrows()]

bar3d = (
    Bar3D(init_opts=opts.InitOpts(theme=ThemeType.MACARONS, bg_color=bg_color, width="1000px", height="450px"))
    .add("", data_3d,
         xaxis3d_opts=opts.Axis3DOpts(data=exp_list, type_="category"),
         yaxis3d_opts=opts.Axis3DOpts(data=edu_list, type_="category"),
         zaxis3d_opts=opts.Axis3DOpts(type_="value"))
    .set_global_opts(
        title_opts=opts.TitleOpts(title="经验·学历·薪资 3D分布", pos_left="center"),
        visualmap_opts=opts.VisualMapOpts(range_color=color_blue)
    )
)

# ====================== 2. 全国薪资地图 ======================
city_salary = df.groupby('city')['avg_salary'].mean().round(0).reset_index()
map_china = (
    Map(init_opts=opts.InitOpts(theme=ThemeType.MACARONS, bg_color=bg_color, width="1000px", height="450px"))
    .add("平均薪资", list(zip(city_salary.city, city_salary.avg_salary)), maptype="china")
    .set_global_opts(
        title_opts=opts.TitleOpts(title="全国城市平均薪资分布", pos_left="center"),
        visualmap_opts=opts.VisualMapOpts(range_color=color_blue)
    )
)

# ====================== 3. 城市岗位TOP5 柱状图 ======================
city_top5 = df['city'].value_counts().head(5)
bar_city = (
    Bar(init_opts=opts.InitOpts(theme=ThemeType.MACARONS, bg_color=bg_color, width="500px", height="400px"))
    .add_xaxis(city_top5.index.tolist())
    .add_yaxis("岗位数", city_top5.values.tolist(), color=color_blue[1])
    .set_global_opts(title_opts=opts.TitleOpts(title="城市岗位数量 Top5", pos_left="center"))
)

# ====================== 4. 公司规模饼图 ======================
scale_cnt = df['scale'].value_counts()
pie_scale = (
    Pie(init_opts=opts.InitOpts(theme=ThemeType.MACARONS, bg_color=bg_color, width="500px", height="400px"))
    .add("", list(zip(scale_cnt.index, scale_cnt.values)), radius=["30%", "75%"])
    .set_colors(color_blue)
    .set_global_opts(title_opts=opts.TitleOpts(title="公司规模分布", pos_left="center"))
    .set_series_opts(label_opts=opts.LabelOpts(formatter="{b}: {d}%"))
)

# ====================== 5. 技能词云 ======================
skill_list = []
for s in df['skill']:
    if s != "未知":
        skill_list.extend([w for w in re.split(r'[ ，、；;]', str(s)) if len(w) > 1])

wordcloud = (
    WordCloud(init_opts=opts.InitOpts(bg_color=bg_color, width="1000px", height="400px"))
    .add("", Counter(skill_list).most_common(40), word_size_range=[15, 60])
    .set_global_opts(title_opts=opts.TitleOpts(title="岗位热门技能词云", pos_left="center"))
)

# ====================== 组合看板（100%无报错） ======================
page = Page(layout=Page.SimplePageLayout)

page.add(
    bar3d,
    map_china,
    bar_city,
    pie_scale,
    wordcloud
)

# 生成
page.render("招聘数据可视化看板.html")
print("✅ 运行成功！已生成：招聘数据可视化看板.html")
print(f"📊 核心数据展示：")
print(f"   总岗位数：{total_jobs}")
print(f"   平均薪资：{avg_salary}")
print(f"   本科岗位：{undergrad_jobs}")