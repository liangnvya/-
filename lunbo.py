#-*- coding: utf-8 -*-

# 数据分析 读取 处理 存储
import pandas as pd
from pyecharts import options as opts
from pyecharts.charts import Pie ,Bar,Timeline,Line,WordCloud

# 用pandas.read_csv()读取指定的excel文件,选择编码格式gb18030(gb18030范围比)
df = pd.read_csv('weather.csv',encoding='gb18030')
print(df['日期'])

# datatime   Series DataFrame  日期格式的数据类型 month
# 这个过程通常用于数据清洗阶段，确保日期数据以统一的格式存储，这对于后续的数据分析和处理非常重要。
df['日期'] = df['日期'].apply(lambda x: pd.to_datetime(x))
print(df['日期'])
"""
0     2019-01-01
1     2019-01-02
2     2019-01-03
3     2019-01-04
4     2019-01-05
         ...    
359   2019-12-26
360   2019-12-27
361   2019-12-28
362   2019-12-29
363   2019-12-30
"""

# 新建一列月份数据(将日期中的月份month 一项单独拿取出来)
df['month'] = df['日期'].dt.month

print(df['month'])
# 需要的数据 每个月中每种天气出现的次数
"""
month(月份)   tianqi(天气)   count(出现次数)
1                  晴         8
1                  雨         9
1                  多云        4
1                  阵雨        10 
2
2
2
3
3
3
"""
# DataFrame GroupBy聚合对象 分组和统计的  size()能够计算分组的大小
df_agg = df.groupby(['month','天气']).size().reset_index()
print(df_agg)
"""
'重置前':
month  天气 
1      多云      5
       晴       2
       阴      20
       雨夹雪     4
2      多云      3
       阴      21
       雨夹雪     4
3      多云      6
       晴       1
       阴      24

'重置后':
    month   天气   0(还没设置列名,所以是0)
0       1   多云   5
1       1    晴   2
2       1    阴  20
3       1  雨夹雪   4
4       2   多云   3
5       2    阴  21
6       2  雨夹雪   4
7       3   多云   6
8       3    晴   1
9       3    阴  24
10      4   多云   6
"""
# 设置下这3列的列名
df_agg.columns = ['month','tianqi','count']
print(df_agg)

# 天气数据的形成 values numpy数组 tolist 列表数据
print(df_agg[df_agg['month']==1][['tianqi','count']]\
    .sort_values(by='count',ascending=False).values.tolist())
"""
[['阴', 20], ['多云', 5], ['雨夹雪', 4], ['晴', 2]]
"""

# 1，轮播图
# 画图
# 实例化一个时间序列的对象，Timeline组件是一个用于创建时间轴轮播图表的高级组件
timeline = Timeline()
# 播放参数:设置时间间隔 1s  单位是:ms(毫秒)
timeline.add_schema(play_interval=1000)    # 单位是:ms(毫秒)

# 循环遍历df_agg['month']里的唯一值
for month in df_agg['month'].unique():
    data = (

        df_agg[df_agg['month']==month][['tianqi','count']]
        .sort_values(by='count',ascending=True)
        .values.tolist()
    )
    # print(data)
    # 绘制柱状图
    bar = Bar()
    # x轴是天气名称
    bar.add_xaxis([x[0] for x in data])
    # y轴是出现次数
    bar.add_yaxis('',[x[1] for x in data])

    # 让柱状图横着放
    bar.reversal_axis()
    # 将计数标签放置在图形右边
    bar.set_series_opts(label_opts=opts.LabelOpts(position='right'))
    # 设置下图表的名称
    bar.set_global_opts(title_opts=opts.TitleOpts(title='长沙2024年每月天气变化 '))
    # 将设置好的bar对象放置到时间轮播图当中,并且标签选择月份 格式为: 数字月
    timeline.add(bar, f'{month}月')

# 将设置好的图表保存为'weathers.html'文件
timeline.render('weathers1.html')


# 2，柱状图
# 创建柱状图对象
bar = Bar()

# 添加 X 轴数据，这里是天气类型
bar.add_xaxis(df_agg['tianqi'].unique().tolist())

# 添加 Y 轴数据，这里是每个天气类型对应的天数
# 我们使用 groupby 来对每个天气进行计数，然后排序
weather_counts = df_agg.groupby('tianqi')['count'].sum().sort_values(ascending=False)
bar.add_yaxis("天气天数", weather_counts.tolist())

# 设置全局配置项
bar.set_global_opts(
    title_opts=opts.TitleOpts(title="长沙2024年天气类型柱状图"),
    xaxis_opts=opts.AxisOpts(axislabel_opts=opts.LabelOpts(rotate=-15)),  # X轴标签倾斜
    yaxis_opts=opts.AxisOpts(name="天数"),
    visualmap_opts=opts.VisualMapOpts(max_=weather_counts.max(), is_show=False),  # 颜色映射配置
    legend_opts=opts.LegendOpts(is_show=False)  # 不显示图例
)

# 渲染图表到文件
bar.render('weather_bar_chart.html')

# 3,折线图
# 创建折线图对象
line = Line()

# 添加 X 轴数据，这里是天气类型
line.add_xaxis(df_agg['tianqi'].unique().tolist())

# 添加 Y 轴数据，这里是每个天气类型对应的天数
# 我们使用 groupby 来对每个天气进行计数
weather_counts = df_agg.groupby('tianqi')['count'].sum()
line.add_yaxis("天气天数", weather_counts.tolist())

# 设置全局配置项
line.set_global_opts(
    title_opts=opts.TitleOpts(title="长沙2024年天气类型天数变化趋势"),
    xaxis_opts=opts.AxisOpts(axislabel_opts=opts.LabelOpts(rotate=-15)),  # X轴标签倾斜
    yaxis_opts=opts.AxisOpts(name="天数"),
    legend_opts=opts.LegendOpts(is_show=False)  # 不显示图例
)

# 渲染图表到文件
line.render('weather_line_chart.html')


# 4，饼图
# 4，详细版饼图
def detailed_weather(weather):
    # 基本天气类型
    if weather in ['多云', '晴', '阴']:
        return weather

    # 天气转换类型
    elif '多云转晴' in weather or '晴转多云' in weather:
        return '多云转晴'
    elif '阴转多云' in weather or '多云转阴' in weather:
        return '阴转多云'

    # 雨天类型
    elif '小雨' in weather:
        return '小雨'
    elif '中雨' in weather:
        return '中雨'
    elif '大雨' in weather:
        return '大雨'
    elif '阵雨' in weather:
        return '阵雨'

    # 组合天气类型
    elif '多云~阴' in weather:
        return '多云到阴'
    elif '晴~多云' in weather:
        return '晴到多云'
    elif '阴~小雨' in weather:
        return '阴转小雨'
    elif '多云~小雨' in weather:
        return '多云转小雨'

    # 其他类型
    else:
        return '其他天气'


# 创建新的DataFrame并合并天气类型
df_detailed = df_agg.copy()
df_detailed['tianqi'] = df_detailed['tianqi'].apply(detailed_weather)
df_detailed = df_detailed.groupby('tianqi')['count'].sum().reset_index()

# 按count值排序，便于展示
df_detailed = df_detailed.sort_values('count', ascending=False)

# 创建饼图对象
pie = Pie()

# 添加数据
pie.add(
    "",
    [list(z) for z in zip(df_detailed['tianqi'], df_detailed['count'])],
    center=["60%", "50%"],
    radius=["30%", "75%"],  # 设置成环形图，更容易区分
    rosetype="radius"  # 设置成南丁格尔玫瑰图，数值大的扇区半径更大
)

# 设置全局配置项
pie.set_global_opts(
    title_opts=opts.TitleOpts(
        title="长沙2024年天气类型分布",

        pos_left="center"
    ),
    legend_opts=opts.LegendOpts(
        orient="vertical",
        pos_top="15%",
        pos_left="2%",
        item_width=25,  # 图例标记的宽度
        item_height=14  # 图例标记的高度
    ),
    tooltip_opts=opts.TooltipOpts(
        trigger="item",
        formatter="{a} <br/>{b}: {c} ({d}%)"
    )
)

# 设置系列配置项
pie.set_series_opts(
    label_opts=opts.LabelOpts(
        formatter="{b}: {d}%",
        font_size=12,
        font_weight="bold",
        position="outside"  # 标签放在外侧
    )
)

# 渲染图表到文件
pie.render('weather_pie_chart.html')

# 5,词云
weather_data = list(zip(df_agg['tianqi'], df_agg['count']))

# 创建词云图
wordcloud = WordCloud()

# 添加数据
wordcloud.add(
    series_name="天气类型",  # 系列名称
    data_pair=weather_data,  # 数据项
    word_size_range=[15, 80],  # 字体大小范围
    shape='circle',  # 词云形状：circle, cardioid, diamond, triangle-forward, triangle, pentagon, star
)

# 设置全局配置项
wordcloud.set_global_opts(
    title_opts=opts.TitleOpts(
        title="长沙2024年天气类型词云图",

        pos_left="center"
    ),
    tooltip_opts=opts.TooltipOpts(
        is_show=True,
        formatter="{b}: {c}"
    )
)

# 渲染图表
wordcloud.render('weather_wordcloud.html')

