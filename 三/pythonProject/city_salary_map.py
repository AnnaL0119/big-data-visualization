import pandas as pd
from pyecharts import options as opts
from pyecharts.charts import Map
from pyecharts.globals import ThemeType

# 读取数据
df = pd.read_csv("招聘数据_预处理后.csv", encoding='utf-8-sig')

# 数据处理
city_salary = df.groupby('city')['avg_salary'].mean().round(0).reset_index()

# 浅蓝色配色
color_blue = ["#ADD8E6", "#87CEFA", "#6495ED", "#4169E1", "#1E3A8A"]
bg_color = "#F0F8FF"

# 生成图表
map_china = (
    Map(init_opts=opts.InitOpts(theme=ThemeType.LIGHT, bg_color=bg_color, width="1000px", height="600px"))
    .add(
        series_name="平均薪资",
        data_pair=list(zip(city_salary['city'], city_salary['avg_salary'])),
        maptype="china",
        is_map_symbol_show=False
    )
    .set_global_opts(
        title_opts=opts.TitleOpts(
            title="全国主要城市平均薪资分布",
            pos_left="center",
            title_textstyle_opts=opts.TextStyleOpts(font_size=18, color="#1E3A8A", font_weight="bold")
        ),
        visualmap_opts=opts.VisualMapOpts(
            min_=city_salary['avg_salary'].min(),
            max_=city_salary['avg_salary'].max(),
            range_color=color_blue,
            pos_left="5%",
            pos_bottom="5%"
        )
    )
)

map_china.render("02_city_salary_map.html")
print("✅ 已生成：02_city_salary_map.html")