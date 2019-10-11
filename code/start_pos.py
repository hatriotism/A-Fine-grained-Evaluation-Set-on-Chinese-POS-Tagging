from find_error import *

tags_dic = {}
with open('data/tags.txt', encoding='gb18030') as tags:
    for line in tags:
        tags_dic[line.strip().split(',')[1]] = line.split(',')[0]

def pku_pos(srcfile='data/raw_utf.txt', dstfile='data/pku_utf.txt'):
    import pkuseg
    pkuseg.test(srcfile, dstfile, postag=True, nthread=20)

def thu_pos(srcfile='data/raw_utf.txt', dstfile='data/thu_utf.txt'):
    import thulac
    thu = thulac.thulac(deli='/')
    thu.cut_f(srcfile, dstfile)

def fool_pos(srcfile='data/raw_utf.txt', dstfile='data/fool_18030.txt'):
    import fool
    with open(srcfile, 'r') as src:
        with open(dstfile, 'w', encoding='gb18030') as dst:
            src_ls_striped = []
            for line in src:
                if line.strip():
                    src_ls_striped.append(line.strip())
                else:
                    src_ls_striped.append(' ')
            ls = fool.pos_cut(src_ls_striped)
            for ls_line in ls:
                dstline = ''
                for word in ls_line:
                    try:
                        x = word[0] + '/' + tags_dic[word[1]] + ' '
                    except:
                        x = word[0] + '/' + word[1] + ' '
                    dstline += x
                if dstline[0] == " ":
                    dst.write('\r\n')
                else:
                    dst.write(dstline + '\r\n')

def snow_pos(srcfile='data/raw_utf.txt', dstfile='data/snow_18030.txt'):
    """
    TnT 3-gram 隐马
    :param srcfile:
    :param dstfile:
    :return:
    """
    import snownlp
    with open(srcfile, 'r') as src:
        with open(dstfile, 'w', encoding='gb18030') as dst:
            for line in src:
                try:
                    l = line.strip()
                    s = snownlp.SnowNLP(l)
                    ls = s.tags
                    dstline = ''
                    for word in ls:
                        try:
                            x = word[0] + '/' + tags_dic[word[1]] + ' '
                        except:
                            x = word[0] + '/' + word[1] + ' '
                        dstline += x
                    dst.write(dstline + '\r\n')
                except:
                    dst.write('\r\n')

def nlpir_pos(srcfile='data/raw.txt', dstfile='data/nlpir_18030.txt'):
    import pynlpir
    pynlpir.open()
    with open(srcfile, 'r', encoding='gb18030') as src:
        with open(dstfile, 'w', encoding='gb18030') as dst:
            for line in src:
                #try:
                l = line.strip()
                if l:
                    ls = pynlpir.segment(l, pos_english=False, pos_names='child')
                    dstline = ''
                    for word in ls:
                        if word[1]:
                            x = word[0] + '/' + tags_dic[word[1]] + ' '
                        else:
                            x = word[0] + '/n '
                        dstline += x
                    dst.write(dstline + '\r\n')
                else:
                    dst.write('\r\n')
                #except:
                #    dst.write('\r\n')
    pynlpir.close()

import pkuseg, thulac, fool, snownlp, pynlpir
seg = pkuseg.pkuseg(postag=True)
thu1 = thulac.thulac()
pynlpir.open()

def pku_(line):
    l = line.strip()
    ls = seg.cut(l)  # 进行分词
    new_ls = []
    for word in ls:
        try:
            new_ls.append((word[0], tags_dic[word[1]]))
        except:
            new_ls.append((word[0], word[1]))
    return new_ls

def thu_(line):
    l = line.strip()
    ls = thu1.cut(l)  # 进行一句话分词
    new_ls = []
    for word in ls:
        try:
            new_ls.append((word[0], tags_dic[word[1]]))
        except:
            new_ls.append((word[0], word[1]))
    return new_ls

def fool_(line):
    l = line.strip()
    ls = fool.pos_cut(l)
    new_ls = []
    for word in ls[0]:
        try:
            new_ls.append((word[0], tags_dic[word[1]]))
        except:
            new_ls.append((word[0], word[1]))
    return new_ls

def snow(line):
    l = line.strip()
    s = snownlp.SnowNLP(l)
    ls = s.tags
    new_ls = []
    for word in ls:
        try:
            new_ls.append((word[0], tags_dic[word[1]]))
        except:
            new_ls.append((word[0], word[1]))
    return new_ls

def nlpir_(line):
    ls_pre = pynlpir.segment(line, pos_english=False, pos_names='child')
    ls = []
    for word in ls_pre:
        if word[1]:
            ls.append((word[0], tags_dic[word[1]]))
        else:
            ls.append((word[0], 'n'))
    return ls

def eval(model):

    with open('result/评测数据集.txt', 'r', encoding='gb18030') as r:
        word_exm = ''
        right_num = 1
        total_num = 1
        label = ''
        label_num = 0

        path = 'result/评测报告/'
        file = 'evalreport_%s.txt' % str(model).split(' ')[1].strip("'")
        mkdir(path)
        with open(path + file, 'w', encoding='gb18030') as f:
            f.write('【评测报告】\r\n\r\n')
            f.write('评测项目\t\t\t\t\t正确率\r\n')
            f.write('—————————————————————————————————————————————————\r\n')
            for line in r:
                if line[0:2] == '# ':
                    if label != '':
                        try:
                            accuracy = right_num / total_num
                            t = '\t' * (5 - int((len(label) / 8)))
                            f.write('%s%s%.2f%s\r\n' % (label, t, accuracy*100, '%'))
                        except:
                            continue
                    label = line[2:].strip()
                    pair = label.split('], [')
                    left = pair[0].replace('[', '').replace(']', '').replace("'", '').split(', ')
                    # right = pair[1].replace('[', '').replace(']', '').replace("'", '').split(', ')
                    right_num = 0
                    total_num = 0
                    label_num += 1
                elif line[0:2] == '##':
                    word_exm = line[2:].strip()
                else:
                    ls = model(line)
                    if len(left) == 1:
                        total_num += 1
                        right_switch = 0
                        for annotate in ls:
                            # print(word[0], word_exm)
                            # print(word[1], left[0])
                            if annotate[0] == word_exm and annotate[1] == left[0] and right_switch == 0:
                                right_num += 1
                                right_switch = 1
                    else:
                        word = []
                        for i in range(len(left)):
                            word.append(['', ''])
                        total_num += 1
                        right_switch = 0
                        for annotate in ls:
                            for i in range(len(left)):
                                try:
                                    word[i] = [word[i+1][0], word[i+1][1]]
                                except:
                                    word[i] = [annotate[0], annotate[1]]
                            word_of_window = ''
                            tag_of_window = []
                            for i in range(len(word)):
                                word_of_window += word[i][0]
                                tag_of_window.append(word[i][1])
                                if word_of_window == word_exm and tag_of_window == left and right_switch == 0:
                                    right_num += 1
                                    right_switch = 1


        print("评测项目数:", label_num)

