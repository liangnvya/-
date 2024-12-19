#-*- coding: utf-8 -*-

# 数据分析 读取 处理 存储
import pandas as pd
from pyecharts import options as opts
from pyecharts.charts import Pie ,Bar,Timeline

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


