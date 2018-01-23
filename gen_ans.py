import json
import jieba
jieba.load_userdict('./udic_jieba_dict.txt')
import requests
from operator import itemgetter


with open('./example.json', 'r') as rf:
    question = json.load(rf)

stopword_set = set()
with open('./stop_words.txt', 'r') as rf:
    for line in rf:
        stopword_set.add(line.replace('\n', ''))

# if '、' in stopword_set:
#     print('是sw')

def get_co_occur_set(value):
    counter = 0
    kcm_cooccur_terms = set()
    for item in value: # item為['高中生', 2]
        kcm_cooccur_terms.add(item[0])
        counter += 1
        if counter == 1000:
            break
    return kcm_cooccur_terms


answer_list = []
for item in question:
    seg_question = jieba.lcut(item['Question'], cut_all=False)
    score = {'A':0, 'B':0, 'C':0}
    for word in seg_question: # loop 過 題目所有詞
        if word in stopword_set:
            continue
        else:
            # print(word)
            kcm_response = requests.get('http://udiclab.cs.nchu.edu.tw/kcm/?keyword='\
                                      + word + '&lang=cht&num=10')
            kcm_result = kcm_response.json()
            co_occur_set = get_co_occur_set(kcm_result['value'])
            for option in ['A', 'B', 'C']:
                if item[option] in co_occur_set:
                    score[option] += 1
    answer_list.append(sorted(score.items(), key=itemgetter(1), reverse=True)[0][0])

print(str(answer_list).replace("'", '"'))


