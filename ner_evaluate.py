import re
pattern=re.compile(r'\][a-z]+')
pattern_alpha=re.compile(r'[a-z]')
def select_ner(sentence):
    ners=[]
    stack=[]
    index=0
    while index<len(sentence.strip()):
        try:
            if sentence[index]==']':
                start=stack[-1]
                end=index
                stack.pop()
                index+=1
                while re.match(pattern_alpha,sentence[index])!=None and index<len(sentence.strip()):
                    index+=1
                ner_type=sentence[end+1:index]
                ner=sentence[start:end]
                ner=re.sub(pattern,'',ner)
                ner=ner.replace('[','').replace(' ','')
                ners.append(ner+ner_type)
            elif sentence[index]=='[':
                stack.append(index+1)
                index += 1
            else:
                index += 1
                pass
        except:
            print(sentence)
            index+=1

    return set(ners)

def data_compare(gold_data,cad_data):
    golden_count=0
    cad_count=0
    positive_count=0
    for g_line,c_line in zip(gold_data,cad_data):
        g_ners=select_ner(g_line)
        c_ners=select_ner(c_line)
        golden_count+=len(g_ners)
        cad_count+=len(c_ners)
        positive_count+=len(g_ners&c_ners)
    recall = positive_count/golden_count
    precise = positive_count/cad_count
    if recall+precise==0:
        f1=0
    else:
        f1=2*recall*precise/(recall+precise)
    return precise,recall,f1


if __name__ == '__main__':
    # refs is the ground truth pos data, cads is the candidate generated by your model.
    refs=open('ner_gold.txt',encoding='utf-8').readlines()
    output=[]
    cads=open('ner_test.txt',encoding='utf-8')
    precise, recall, f1=data_compare(refs,cads)
    print({'precise':precise,'recall':recall,'f1':f1})