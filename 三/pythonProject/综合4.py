import pandas as pd
import re
from collections import Counter
from pyecharts import options as opts
from pyecharts.charts import Page, Bar, Pie, Map, WordCloud, Bar3D
from pyecharts.globals import ThemeType

# ====================== 读取数据 ======================
df = pd.read_csv("招聘数据_预处理后.csv", encoding='utf-8-sig')

# 核心数据
total_jobs = len(df)
avg_salary = round(df['avg_salary'].mean(), 1)
undergrad_jobs = len(df[df['education'] == '本科'])

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

# ====================== 图表2：全国薪资地图 ======================
city_salary = df.groupby('city')['avg_salary'].mean().round(0).reset_index()
map_china = (
    Map(init_opts=opts.InitOpts(theme=ThemeType.LIGHT, bg_color=bg_color, width="550px", height="400px"))
    .add("平均薪资", list(zip(city_salary.city, city_salary.avg_salary)), maptype="china")
    .set_global_opts(title_opts=opts.TitleOpts(title="全国城市平均薪资分布", pos_left="center"))
)

# ====================== 图表3：城市岗位TOP5 ======================
city_top5 = df['city'].value_counts().head(5)
bar_city = (
    Bar(init_opts=opts.InitOpts(theme=ThemeType.LIGHT, bg_color=bg_color, width="550px", height="400px"))
    .add_xaxis(city_top5.index.tolist())
    .add_yaxis("岗位数量", city_top5.values.tolist(), color=color_blue[1])
    .set_global_opts(title_opts=opts.TitleOpts(title="城市岗位数量 Top5", pos_left="center"))
)

# ====================== ✅ 图表4：公司规模饼图（强制显示版） ======================
# 强制取前5个，确保数据有效
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
        legend_opts=opts.LegendOpts(is_show=False),  # 直接关闭图例，避免遮挡
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

# ====================== 整合：上3下2 布局 ======================
page = Page(layout=Page.SimplePageLayout)

# 第一行 3 张图
page.add(bar3d, map_china, bar_city)

# 第二行 2 张图
page.add(pie_scale, wordcloud)

# 生成
page.render("AI招聘数据看板.html")
print("✅ 生成成功！打开：AI招聘数据看板1.html")