import os, shutil
from seqeval.metrics import accuracy_score, classification_report, f1_score, recall_score, precision_score

def find_error(annotator_name, goldfile, answerfile, fake, pre_fake=True):
    counterpart_dic = {}
    error_sentences = []
    gold_old = []  # 为了测f1之类的
    answer_old = []
    with open(goldfile, 'r', encoding='gb18030') as gold:
        with open(answerfile, 'r', encoding='gb18030') as answer:
            goldlines = gold.readlines()
            answerlines = answer.readlines()

            assert len(goldlines) == len(answerlines)
            for l in range(len(goldlines)):
                # l = 21
                goldline = []
                answerline = []
                for annotate in goldlines[l].replace('\n', '').replace('  ', ' ').split(' '):
                    goldline.append(annotate.replace('_', '/').split('/'))
                for annotate in answerlines[l].replace('\n', '').replace('  ', ' ').split(' '):
                    answerline.append(annotate.replace('_', '/').split('/'))

                def get_length(l):
                    length = 0
                    sentence = ''
                    for i in l:
                        length += len(i[0])
                        sentence += i[0]
                    return length, sentence

                _, sentence = get_length(answerline)

                g_start, g_end, a_start, a_end = 0, 1, 0, 1
                counterparts = []


                while g_start < len(goldline):
                    g_length, _ = get_length(goldline[g_start: g_end])
                    a_length, _ = get_length(answerline[a_start: a_end])

                    if g_length == a_length:
                        write = ''
                        for word in goldline[g_start: g_end]:
                            try:
                                w = word[0] + '/' + word[1] + ' '
                                write += w
                            except:
                                continue
                        write += '||'
                        for word in answerline[a_start: a_end]:
                            try:
                                w = ' ' + word[0] + '/' + word[1]
                                write += w
                            except:
                                continue
                        if write != '||':
                            write = write.replace(' || ', '||')
                            counterparts.append([goldline[g_start: g_end], answerline[a_start: a_end], write])
                        if len(goldline) == len(answerline):
                            try:
                                gold_old.append([goldline[x][1] for x in range(len(goldline))])
                                answer_old.append([answerline[x][1] for x in range(len(goldline))])
                            except:
                                goldline
                        g_start = g_end
                        g_end += 1
                        a_start = a_end
                        a_end += 1
                    elif g_length < a_length:
                        g_end += 1
                    elif g_length > a_length:
                        a_end += 1

                write = ''
                for counterpart in counterparts:
                    try:
                        answerparttags = [pair[1] for pair in counterpart[1]]
                        goldparttags = [pair[1] for pair in counterpart[0] if pair != ['']]
                        tags = str([goldparttags, answerparttags])
                    except:
                        print("错误格式:", counterpart)
                    tags_ls = tags.replace('[', '').replace(']', '').replace("'", '').split(', ')
                    pair = tags.split('], [')
                    wrong = pair[0].replace('[', '').replace(']', '').replace("'", '').split(', ')
                    right = pair[1].replace('[', '').replace(']', '').replace("'", '').split(', ')
                    if pre_fake:
                        if counterpart[0] != counterpart[1] and tags not in fake:
                            key = counterpart[2]
                            if key in counterpart_dic:
                                counterpart_dic[key] += 1
                            else:
                                counterpart_dic[key] = 1
                            w = '##' + counterpart[2] + '##'
                            write += w
                    else:
                        if counterpart[0] != counterpart[1]:
                            key = counterpart[2]
                            if key in counterpart_dic:
                                counterpart_dic[key] += 1
                            else:
                                counterpart_dic[key] = 1
                            w = '##' + counterpart[2] + '##'
                            write += w
                if write:
                    error_sentences.append(sentence)
                    error_sentences.append(write)

    path = 'result/%s/' % annotator_name
    file = 'error_%s.txt' % annotator_name
    mkdir(path)
    with open(path + file, 'w', encoding='gb18030') as f:
        for key in counterpart_dic:
            f.write(key + '  ' + str(counterpart_dic[key]) + '\r\n')

    file = 'error_sentence_%s.txt' % annotator_name
    with open(path + file, 'w', encoding='gb18030') as f:
        for x in error_sentences:
            f.write(x + '\r\n')

    print(classification_report(gold_old, answer_old, digits=4))



def find_already_in(path, file):
    already_in = []
    for i in range(1):
        try:
            with open(path + file, 'r', encoding='gb18030') as f:
                for line in f:
                    already_in.append(line.strip())
        except:
            continue
    return already_in

def wrong_pair(file):
    Wrong_Tag_Pair = {}
    Wrong_Word_Pair = {}
    with open(file, 'r', encoding='gb18030') as error:
        for line in error:
            line = line.replace('\n', '')
            aline = line.split('  ')
            fre = aline[-1]
            pair = aline[0].split('||')

            answer = pair[1]
            gold = pair[0]
            answer_tags = []
            answer_words = []
            gold_tags = []
            gold_words = []
            for word in answer.split(' '):
                answer_tags.append(word.split('/')[-1])
                answer_words.append(word.split('/')[0])
            for word in gold.split(' '):
                gold_tags.append(word.split('/')[-1])
                gold_words.append(word.split('/')[0])
            tag_pair = str([gold_tags, answer_tags])
            word_pair = [gold_words, answer_words]
            try:
                Wrong_Tag_Pair[tag_pair] += int(fre)
            except KeyError:
                Wrong_Tag_Pair[tag_pair] = int(fre)
            try:
                Wrong_Word_Pair[tag_pair][0] = Wrong_Tag_Pair[tag_pair]
            except KeyError:
                Wrong_Word_Pair[tag_pair] = [Wrong_Tag_Pair[tag_pair]]
            if word_pair not in Wrong_Word_Pair[tag_pair]:
                Wrong_Word_Pair[tag_pair].append(word_pair)
        Wrong_Tag_Pair_ = {}
        Wrong_Word_Pair_ = {}
        for key in sorted(Wrong_Tag_Pair):
            Wrong_Tag_Pair_[key] = Wrong_Tag_Pair[key]
        for key in sorted(Wrong_Word_Pair):
            Wrong_Word_Pair_[key] = Wrong_Word_Pair[key]
    return Wrong_Tag_Pair_, Wrong_Word_Pair_

def mkdir(path):
    # 引入模块

    # 去除首位空格
    path = path.strip()
    # 去除尾部 \ 符号
    path = path.rstrip('/')

    # 判断路径是否存在
    # 存在     True
    # 不存在   False
    isExists = os.path.exists(path)

    # 判断结果
    if not isExists:
        # 如果不存在则创建目录
        # 创建目录操作函数
        os.makedirs(path)

        print("正在创建路径：'%s'" % path)
        return True
    else:
        # 如果目录存在则不创建，并提示目录已存在
        # print(path+' 目录已存在')
        return False

def overlap_error(file_dir='result/总错句集（试题）'):
    fre_of_name = {}
    threshold = int(len(os.listdir(file_dir))/100*51)+1
    for dir in os.listdir(file_dir):
        if dir != 'overlap' and dir != '.DS_Store':
            for filename in os.listdir(file_dir+'/'+dir):
                try:
                    fre_of_name[filename] += 1
                except:
                    fre_of_name[filename] = 1

    name_seleted = []
    for filename in fre_of_name:
        if fre_of_name[filename] >= threshold:
            name_seleted.append(filename)

    overlap_dir = file_dir+'/overlap'
    if os.path.exists(overlap_dir):
        shutil.rmtree(overlap_dir)

    error_word = {}
    for dir in os.listdir(file_dir):
        if dir != 'overlap' and dir != '.DS_Store':
            srcpath = '%s/%s/' % (file_dir, dir)
            for file in name_seleted:
                filename = file[:-4]
                if filename != '.DS_Store':
                    srcfile = '%s.txt' % filename
                    src = srcpath + srcfile

                    if os.path.exists(src):
                        dstpath = '%s/%s/' % (overlap_dir, filename)
                        overlapfile = 'overlap_%s.txt' % filename

                        dstfile = '%s.txt' % dir
                        dst = dstpath + dstfile
                        mkdir(dstpath)
                        mycopyfile(src, dst)

                        with open(dstpath + overlapfile, 'a', encoding='gb18030') as w:
                            already_in = find_already_in(dstpath, overlapfile)
                            with open(src , 'r', encoding='gb18030') as r:
                                lastline = ''
                                for line in r:
                                    if line.strip() not in already_in and line[0] != '#':
                                        w.write(lastline)
                                        w.write(line)
                                    elif line[0] == '#':
                                        lastline = line

            file_error = 'result/%s/error_%s.txt' % (dir, dir)

            _, error_word_t = wrong_pair(file_error)
            for label in error_word_t:
                if label + '.txt' in name_seleted:
                    try:
                        ls = error_word[label][1:]
                        for pair in error_word_t[label][1:]:
                            if pair not in ls:
                                ls.append(pair)
                        error_word[label] = ls
                    except:
                        error_word[label] = error_word_t[label][1:]


    path = 'result/'
    file_word = '评测项目及其词例.txt'
    num_of_word_exm = 0
    with open(path + file_word, 'w', encoding='gb18030') as f:
        for label in error_word:
            if label + '.txt' in name_seleted:
                f.write(label + ' #')
                already_in = []
                for i in error_word[label]:
                    try:
                        word_exm = str(i[0]).replace('[', '').replace(']', '').replace("'", '').replace(', ', '')
                        # right = str(i[0]).replace('[', '').replace(']', '').replace("'", '').replace(', ', '+')
                        # wrong = str(i[1]).replace('[', '').replace(']', '').replace("'", '').replace(', ', '+')
                        # x = '%s  ==>  %s' % (right, wrong)
                        if word_exm not in already_in:
                            # f.write(x + '\r\n')
                            f.write(' ' + word_exm)
                            already_in.append(word_exm)
                    except:
                        print("!【格式错误】", i)
                        continue
                num_of_word_exm += len(already_in)
                f.write('\r\n')

    file_sentence = '评测试题集.txt'
    num_of_sentence = 0
    with open(file_word, 'r', encoding='gb18030') as f:
        with open(path + file_sentence, 'w', encoding='gb18030') as f2:
            for line in f:
                if line[0:2] == '[[':
                    label = line.strip().split(' # ')[0]
                    error_word = line.strip().split(' # ')[1].split(' ')
                    if label + '.txt' in name_seleted:
                        filename = label
                        dstpath = '%s/%s/' % (overlap_dir, filename)
                        overlapfile = 'overlap_%s.txt' % filename
                        with open(dstpath + overlapfile, 'r', encoding='gb18030') as f3:
                            f3_lines = f3.readlines()
                            f2.write('# ' + label + '\r\n')
                            already_in = []
                            for word_exm in error_word:
                                try:
                                    if word_exm not in already_in:
                                        # f.write(x + '\r\n')
                                        f2.write('## ' + word_exm + '\r\n')
                                        switch = 0
                                        for line in f3_lines:
                                            if switch == 0 and line[0] == '#' and word_exm in line:
                                                switch = 1
                                            elif switch == 1:
                                                f2.write(line)
                                                num_of_sentence += 1
                                                switch = 0
                                        already_in.append(word_exm)
                                except:
                                    print("!【格式错误】", word_exm)
                                    continue

    print("评测项目候选集规模: ", len(name_seleted))
    print("实例数:", num_of_word_exm)
    print("句子数:", num_of_sentence)
#                     with open(src, 'r', encoding='gb18030') as src_:
#                         with open(dst, 'a', encoding='gb18030') as dst_:
#                             for line in src_:
#                                 dst_.write(line + '\r\n')


def mycopyfile(srcfile,dstfile):
    if not os.path.isfile(srcfile):
        print("%s not exist!"%(srcfile))
    else:
        fpath,fname=os.path.split(dstfile)    #分离文件名和路径
        if not os.path.exists(fpath):
            os.makedirs(fpath)                #创建路径
            print(fpath)
        shutil.copy(srcfile,dstfile)      #复制文件
        print("copy %s -> %s"%(srcfile,dstfile))

# def all_same(l):
#     """
#     鉴别类似于"[['n', 'n'], ['n']]"的label
#     """
#     if l[0] == l[1]:
#         if len(l) == 2:
#             return True
#         return all_same(l[1:])
#     else:
#         return False
#
# def superior_or_inferior(l, wrong, right):
#     if len(l) == 2:
#         try:
#             if str(wrong[0][0]).lower() == str(right[0][0]).lower() or str(wrong[0][-1]).lower() == str(
#                     right[0][-1]).lower():
#                 return True
#             else:
#                 return False
#         except:
#             # print(l)
#             return True
#
# def n_and_v(l, wrong, right):
#     if len(wrong) <= 3 and len(right) <= 3 and (len(wrong) == 1 or len(right) == 1):
#         if 'u' not in l and 'y' not in l:
#             if 'n' in wrong and 'n' in right:
#                 return True
#             elif 'v' in wrong and 'v' in right:
#                 return True