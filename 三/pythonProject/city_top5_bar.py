import pandas as pd
from pyecharts import options as opts
from pyecharts.charts import Bar
from pyecharts.globals import ThemeType

# 读取数据
df = pd.read_csv("招聘数据_预处理后.csv", encoding='utf-8-sig')

# 数据处理
city_counts = df['city'].value_counts().head(5)

# 浅蓝色配色
color_blue = ["#ADD8E6", "#87CEFA", "#6495ED", "#4169E1", "#1E3A8A"]
bg_color = "#F0F8FF"

# 生成图表
bar_city = (
    Bar(init_opts=opts.InitOpts(theme=ThemeType.LIGHT, bg_color=bg_color, width="800px", height="500px"))
    .add_xaxis(city_counts.index.tolist())
    .add_yaxis("岗位数量", city_counts.values.tolist(), color=color_blue[1])
    .set_global_opts(
        title_opts=opts.TitleOpts(
            title="城市岗位数量 Top5",
            pos_left="center",
            title_textstyle_opts=opts.TextStyleOpts(font_size=18, color="#1E3A8A", font_weight="bold")
        ),
        xaxis_opts=opts.AxisOpts(axislabel_opts=opts.LabelOpts(rotate=0)),
        yaxis_opts=opts.AxisOpts(name="岗位数量")
    )
)

bar_city.render("03_city_top5_bar.html")
print("✅ 已生成：03_city_top5_bar.html")