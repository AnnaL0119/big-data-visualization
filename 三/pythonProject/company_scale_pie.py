import pandas as pd
import webbrowser
from pyecharts import options as opts
from pyecharts.charts import Pie
from pyecharts.globals import ThemeType

# 读取数据
df = pd.read_csv("招聘数据_预处理后.csv", encoding='utf-8-sig')

# ====================== 修复点 1：正确获取数据 ======================
scale_counts = df['scale'].value_counts()
# 转换成 pyecharts 支持的列表格式
data = []
for key, value in zip(scale_counts.index, scale_counts.values):
    data.append([str(key), int(value)])

# 浅蓝色配色
color_blue = ["#ADD8E6", "#87CEFA", "#6495ED", "#4169E1", "#1E3A8A"]
bg_color = "#F0F8FF"

# 生成图表
pie_scale = (
    Pie(init_opts=opts.InitOpts(theme=ThemeType.LIGHT, bg_color=bg_color, width="800px", height="500px"))
    .add(
        series_name="公司规模",
        data_pair=data,  # 使用修复后的数据
        radius=["30%", "70%"],
    )
    .set_colors(color_blue)
    .set_global_opts(
        title_opts=opts.TitleOpts(
            title="公司规模分布",
            pos_left="center",
            title_textstyle_opts=opts.TextStyleOpts(font_size=18, color="#1E3A8A", font_weight="bold")
        ),
        legend_opts=opts.LegendOpts(orient="vertical", pos_right="5%", pos_top="15%")
    )
    .set_series_opts(
        label_opts=opts.LabelOpts(
            formatter="{b}: {d}%",
            font_size=12
        )
    )
)

# 输出并自动打开
pie_scale.render("04_company_scale_pie.html")
webbrowser.open("04_company_scale_pie.html")  # 自动打开浏览器
print("✅ 已生成并打开：04_company_scale_pie.html")