import pandas as pd
import re
from collections import Counter
from pyecharts import options as opts
from pyecharts.charts import WordCloud

# 读取数据
df = pd.read_csv("招聘数据_预处理后.csv", encoding='utf-8-sig')

# 数据处理
skill_list = []
for s in df['skill']:
    if s != "未知":
        words = re.split(r'[ ，、；;]', str(s))
        skill_list.extend([w for w in words if len(w) > 1])
skill_top30 = Counter(skill_list).most_common(30)

# 浅蓝色配色
color_blue = ["#ADD8E6", "#87CEFA", "#6495ED", "#4169E1", "#1E3A8A"]
bg_color = "#F0F8FF"

# 生成图表
wordcloud = (
    WordCloud(init_opts=opts.InitOpts(bg_color=bg_color, width="1000px", height="600px"))
    .add(
        series_name="技能词频",
        data_pair=skill_top30,
        word_size_range=[14, 60]
    )
    .set_global_opts(
        title_opts=opts.TitleOpts(
            title="热门技能词云",
            pos_left="center",
            title_textstyle_opts=opts.TextStyleOpts(font_size=18, color="#1E3A8A", font_weight="bold")
        )
    )
)

wordcloud.render("05_skill_wordcloud.html")
print("✅ 已生成：05_skill_wordcloud.html")