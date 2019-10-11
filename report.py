from find_error import *

def fre_of_tag(file):
    fre_of_tags_gold = {}
    with open(file, 'r', encoding='gb18030') as gold:
        for line in gold:
            pairs = line.split(' ')
            for pair in pairs:
                tag = pair.split('/')[-1]
                if tag[-1:] == '\n':
                    tag = tag[:-1]
                if tag != '':
                    try:
                        fre_of_tags_gold[tag] += 1
                    except KeyError:
                        fre_of_tags_gold[tag] = 1
    return fre_of_tags_gold

tags = []
def lin_lan(annotator_name, goldfile, answerfile):
    global tags
    pair_dic = {}
    lin = 0
    lan = 0
    fre_of_gold = fre_of_tag(goldfile)
    answer = fre_of_tag(answerfile)
    for gold_key in fre_of_gold:
        if gold_key not in tags:
            tags.append(gold_key)
        for key in answer:
            if key not in tags:
                tags.append(key)
            if gold_key == key:
                x = answer[key] - fre_of_gold[key]
                pair_dic[key] = [x, round((x) / fre_of_gold[key], 4)] # 若正则滥标，若负则吝标
            elif key not in fre_of_gold and key not in pair_dic:
                k = '+' + key  # tag前带正号，表示gold的标注体系没有、answer的标注体系有的tag
                x = answer[key] - 0
                pair_dic[k] = [x, 1.0]
            elif gold_key not in answer and gold_key not in pair_dic:
                k = '-' + gold_key  # tag前带负号，表示gold的标注体系有、answer的标注体系没有的tag
                x = 0 - fre_of_gold[gold_key]
                pair_dic[k] = [x, round((x) / fre_of_gold[gold_key], 4)]
    lin_dic={}
    lan_dic={}
    for key in pair_dic:
        if pair_dic[key][0] < 0:
            lin += pair_dic[key][0]
            lin_dic[key] = pair_dic[key]
        elif pair_dic[key][0] > 0:
            lan += pair_dic[key][0]
            lan_dic[key] = pair_dic[key]


    path = 'result/%s/' % annotator_name
    file = 'report_%s.txt' % annotator_name
    mkdir(path)
    with open(path + file, 'w', encoding='gb18030') as f:
        f.write('吝标报告\r\n')
        f.write('词性\t吝标指数\t吝标比例\r\n')
        f.write('———————————————————————\r\n')
        for key in lin_dic:
            f.write('%s\t%d\t%f\r\n' % (key, abs(lin_dic[key][0]), abs(lin_dic[key][1])))
        f.write('吝标总指数：%d\r\n' % abs(lin))
        f.write('\r\n\r\n\r\n')
        f.write('滥标报告\r\n')
        f.write('词性\t滥标指数\t滥标比例\r\n')
        f.write('———————————————————————\r\n')
        for key in lan_dic:
            f.write('%s\t%d\t%f\r\n' % (key, abs(lan_dic[key][0]), abs(lan_dic[key][1])))
        f.write('滥标总指数：%d\r\n' % abs(lan))
        f.write('\r\n\r\n\r\n')
    return lin_dic, lan_dic




