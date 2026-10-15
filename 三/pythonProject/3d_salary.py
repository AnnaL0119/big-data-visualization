import pandas as pd
from pyecharts import options as opts
from pyecharts.charts import Bar3D
from pyecharts.globals import ThemeType

# 读取数据
df = pd.read_csv("招聘数据_预处理后.csv", encoding='utf-8-sig')

# 数据处理
exp_edu = df.groupby(['experience', 'education'])['avg_salary'].mean().reset_index()
exp_list = exp_edu['experience'].unique().tolist()
edu_list = exp_edu['education'].unique().tolist()
data_3d = []
for _, row in exp_edu.iterrows():
    x = exp_list.index(row['experience'])
    y = edu_list.index(row['education'])
    z = round(row['avg_salary'], 0)
    data_3d.append([x, y, z])

# 浅蓝色配色
color_blue = ["#ADD8E6", "#87CEFA", "#6495ED", "#4169E1", "#1E3A8A"]
bg_color = "#F0F8FF"

# 生成图表
bar3d = (
    Bar3D(init_opts=opts.InitOpts(theme=ThemeType.LIGHT, bg_color=bg_color, width="1000px", height="600px"))
    .add(
        series_name="平均薪资",
        data=data_3d,
        xaxis3d_opts=opts.Axis3DOpts(type_="category", data=exp_list, name="工作经验"),
        yaxis3d_opts=opts.Axis3DOpts(type_="category", data=edu_list, name="学历"),
        zaxis3d_opts=opts.Axis3DOpts(type_="value", name="平均薪资(元)")
    )
    .set_global_opts(
        title_opts=opts.TitleOpts(
            title="岗位薪酬-经验/学历分布",
            pos_left="center",
            title_textstyle_opts=opts.TextStyleOpts(font_size=18, color="#1E3A8A", font_weight="bold")
        ),
        visualmap_opts=opts.VisualMapOpts(range_color=color_blue, pos_left="5%", pos_bottom="5%")
    )
)

bar3d.render("01_3d_salary.html")
print("✅ 已生成：01_3d_salary.html")