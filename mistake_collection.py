from find_error import *

def get_fake_error(file):
    fake = []
    with open(file, 'r', encoding='gb18030') as fake_error:
        for line in fake_error:
            if line[0] == '[':
                fake.append(line.strip())
    return fake


def mistake_collection(name, threshold=5):
    file_error = 'result/%s/error_%s.txt' % (name, name)
    file_sentence_error = 'result/%s/error_sentence_%s.txt' % (name, name)
    error, error_word = wrong_pair(file_error)
    error_ = sorted(error.items(), key=lambda item: item[1])
    error_.reverse()
    path = 'result/%s/' % name
    file = 'report_%s.txt' % name
    mkdir(path)
    with open(path + file, 'a', encoding='gb18030') as f:
        f.write('分类型错误报告\r\n')
        f.write('错误类型\t\t\t\t\t错误数量\r\n')
        f.write('——————————————————————————————————————————————\r\n')
        total = 0
        for e in error_:
            t = '\t' * (5-int((len(e[0]) / 8)))
            f.write('%s%s%d\r\n' % (e[0], t, e[1]))
            total += e[1]
        f.write('错误实例总数：%d\r\n' % total)
        f.write('错误类型总数：%d\r\n' % len(error_))
        f.write('\r\n\r\n\r\n')


    from copy import deepcopy
    error_ = deepcopy(error)
    for label in error_:
        if error[label] <= threshold:
            del error[label]
            del error_word[label]

    collection = {}
    with open(file_sentence_error, 'r', encoding='gb18030') as error_sentence:
        last_line = ''
        for line in error_sentence:
            if line[:2] == '##':
                last_line = last_line.strip()

                for l in line.split('##'):
                    pair = l.split('||')
                    stop = [[''], ['\n']]
                    if pair not in stop:
                        answer = pair[1]
                        gold = pair[0]
                        answer_tags = []
                        gold_tags = []
                        for word in answer.split(' '):
                            answer_tags.append(word.split('/')[-1])
                        for word in gold.split(' '):
                            gold_tags.append(word.split('/')[-1])
                        tag_pair = str([gold_tags, answer_tags])
                        if tag_pair in error:
                            try:
                                if [last_line, line] not in collection[tag_pair]:
                                    collection[tag_pair].append([last_line, line])
                            except KeyError:
                                collection[tag_pair] = [[last_line, line]]

                last_line = line
            else:
                last_line = line

#     for label in collection:
#         path = 'result/总错句集（试题）/'
#         file = '%s.txt' % label
#         mkdir(path)
#         already_in = find_already_in(path, file)
#         with open(path + file, 'a', encoding='gb18030') as f:
#             for x in collection[label]:
#                 if x[0] not in already_in:
#                     f.write(x[0] + '\r\n')

    for label in collection:
        path = 'result/%s/错句集/' % name
        file = '%s.txt' % label
        mkdir(path)
        already_in = find_already_in(path, file)
        with open(path + file, 'a', encoding='gb18030') as f:
            for x in collection[label]:
                if x[0] not in already_in:
                    f.write(x[1] + x[0] + '\r\n')

        path = 'result/总错句集（试题）/%s/' % name
        file = '%s.txt' % label
        mkdir(path)
        with open(path + file, 'a', encoding='gb18030') as f:
            for x in collection[label]:
                if x[0] not in already_in:
                    f.write(x[1] + x[0] + '\r\n')

    for label in error_word:
        path = 'result/%s/错词集/' % name
        file = '%s.txt' % label
        mkdir(path)
        already_in = find_already_in(path, file)
        with open(path + file, 'a', encoding='gb18030') as f:
            for i in error_word[label][1:]:
                wrong = str(i[0]).replace('[', '').replace(']', '').replace("'", '').replace(', ', ' + ')
                right = str(i[1]).replace('[', '').replace(']', '').replace("'", '').replace(', ', ' + ')
                x = '%s  ==>  %s' % (wrong, right)
                if x not in already_in:
                    f.write(x + '\r\n')




