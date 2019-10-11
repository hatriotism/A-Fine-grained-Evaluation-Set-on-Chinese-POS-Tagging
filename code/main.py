from mistake_collection import *
from report import *

def collect_and_report(annotator_name, goldfile, answerfile, fake_error_file = 'data/fake_error.txt', threshold=1):
    """
    annotator_name: string. the name of annotator that you want to test.
    goldfile: string. the path and filename of the gold answer.
    answerfile: string. the path and filename of the annotator's answer.
    """

    assert isinstance(annotator_name, str), 'annotator_name must be string'
    assert isinstance(goldfile, str), 'goldfile must be string'
    assert isinstance(answerfile, str), 'goldfile must be string'
    assert goldfile[-3:] == 'txt' and answerfile[-3:] == 'txt', 'both goldfile and answerfile must end with txt'

    fake = get_fake_error(fake_error_file)
    find_error(annotator_name, goldfile, answerfile, fake)
    lin_lan(annotator_name, goldfile, answerfile)
    mistake_collection(annotator_name, threshold=threshold)


if __name__ == '__main__':
#     from start_pos import *
    collect_and_report('pku', 'data/gold.txt', 'data/pku_18030.txt')
#     collect_and_report('thu', 'data/gold.txt', 'data/thu_18030.txt')
#     collect_and_report('fool', 'data/gold.txt', 'data/fool_18030.txt')
#     collect_and_report('snow', 'data/gold.txt', 'data/snow_18030.txt')
#     collect_and_report('nlpir', 'data/gold.txt', 'data/nlpir_18030.txt')
#     collect_and_report('jieba', 'data/gold.txt', 'data/jieba_18030.txt')
#     overlap_error(file_dir='result/总错句集（试题）')