【功能介绍】
1. Collect_and_report
这是中文分词和词性标注模型的一个评测程序，通过将模型的标注结果与人工标注的正确答案相比对，按语言知识分项目测试该模型对这些语言知识的掌握情况，并可以自动生成针对该模型的错句集、错词集，以方便之后的迭代训练。
输入：人工标注的正确答案（txt文本文件）、模型的标注结果（txt文本文件）
输出：按错误类型分类的错句集（result/**/错句集）、错词集（result/**/错词集）、按错误类型分类的模型初步评测结果（result/**/report_**.txt）。

2. Overlap_error
这个程序旨在寻找评测项目和得到评测试题集，具体步骤如1.4.1所述。
输入：各种模型的标注结果（给出所在路径即可）
输出：评测项目及其词例（result/评测项目及其词例.txt）、按评测项目和词例分类的评测试题集（result/评测试题集.txt）


【使用方式】
在code目录下，运行python。在python环境下运行本程序：
$ python
>>> from main import *
首先运行collect_and_report对pkuseg、thulac等标注器进行错误搜集和评测：
>>> collect_and_report('pku', 'data/gold.txt', 'data/pku_18030.txt', 'data/fake_error.txt')
                         |            |                 |                      |
                      项目名称     正确答案位置      测试模型的答案位置       自定义伪错误的位置
>>> collect_and_report('thu', 'data/gold.txt', 'data/thu_18030.txt')
>>> collect_and_report('fool', 'data/gold.txt', 'data/fool_18030.txt')
>>> collect_and_report('snow', 'data/gold.txt', 'data/snow_18030.txt')
>>> collect_and_report('nlpir', 'data/gold.txt', 'data/nlpir_18030.txt')
>>> collect_and_report('jieba', 'data/gold.txt', 'data/jieba_18030.txt')
>>> overlap_error()
此时评测项目及其词例和按评测项目和词例分类的评测试题集就会输出到result文件夹中。


【内容介绍】
code
|- data                 # 这个文件夹用来存放所有数据和知识
|   |- fake_error.txt       # 用户自定义的伪错误
|   |- focus_error.txt       # 用户自定义的伪错误
|   |- gold.txt             # 人工标注的正确答案
|   |- pku_18030.txt        # pkuseg标注的答案
|   |- thu_18030.txt        # thulac标注的答案
|   |- jieba_18030.txt      # jieba标注的答案
|   ...                     # 用户可以加入更多答案
|- main.py              # 主函数
|- find_error.py
|- mistake_collection.py
|- report.py
|- start_pos.py           # 用最后的评测试题集评测各标注器的程序
|- result               # 这个文件夹用来存放输出的结果
|   |- 评测试题集.txt
|   |- 评测项目及其词例.txt
|   |- pku
|       |- 错词集
|       |- 错句集
|       |- error_pku.txt    # 该标注器标错的词对及其频率
|       |- error_sentence_pku.txt    # 该标注器标错的句子
|       |- report_pku.txt   # 对该标注器的报告
|   ...
|   |- 总错句集（试题）   # 方便找评测项目和词例
