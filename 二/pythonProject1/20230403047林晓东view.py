from pyecharts.charts import Bar
from pyecharts import options as opts
from pyecharts.globals import ThemeType

# ----------------------
# 数据（前五城市 + 岗位数）
# ----------------------
city_list = ["北京", "上海", "深圳", "杭州", "广州"]
job_count = [1560, 1320, 1180, 950, 860]

# ----------------------
# 创建柱状图（浅蓝风格）
# ----------------------
bar = (
    Bar(init_opts=opts.InitOpts(
        theme=ThemeType.MACARONS,  # 好看的主题
        width="1000px",
        height="600px"
    ))
    .add_xaxis(city_list)
    .add_yaxis(
        "岗位数量",
        job_count,
        itemstyle_opts=opts.ItemStyleOpts(color="#93c5fd"),  # 浅蓝配色
    )
    .set_global_opts(
        title_opts=opts.TitleOpts(
            title="AI岗位数量排名前五城市",
            subtitle="数据来源：AI招聘数据集",
            title_textstyle_opts=opts.TextStyleOpts(font_size=24),
        ),
        xaxis_opts=opts.AxisOpts(
            axislabel_opts=opts.LabelOpts(color="#333"),
        ),
        yaxis_opts=opts.AxisOpts(
            axislabel_opts=opts.LabelOpts(color="#333"),
            splitline_opts=opts.SplitLineOpts(is_show=True),
        ),
        tooltip_opts=opts.TooltipOpts(trigger="axis"),
    )
)

# 生成 HTML 文件（自动打开）
bar.render("AI岗位TOP5城市.html")
print("图表已生成：AI岗位TOP5城市.html")