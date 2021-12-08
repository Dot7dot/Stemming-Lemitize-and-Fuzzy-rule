import json, re, csv
import pandas as pd
import nltk

#Loading json file
with open('path', 'r', encoding = 'utf-8') as f:
    followers = json.load(f)

sdatalist=[]
ldatalist=[]
stemmer = nltk.stem.porter.PorterStemmer()
#Washing Rule
name = re.compile('(@[^\\s]*)')
url = re.compile('([a-zA-Z]+:\\/\\/[^\\s]*)')
spacechar = re.compile('(\\s){1,}')
# amp = re.compile('(&amp)')

lemmatizer = nltk.stem.wordnet.WordNetLemmatizer()

#lemmatize 和 stemming 參考自：https://ithelp.ithome.com.tw/articles/10214221
def lemmatize(word):#vna 目測 anv 的表現比好一些
    lemma = lemmatizer.lemmatize(word,'v')#verb
    if lemma == word:
        lemma = lemmatizer.lemmatize(word,'n')#noun
        if lemma == word:
            lemma = lemmatizer.lemmatize(word, 'a')#adjective
    return lemma

def fuzzy_rule(word):
    score = 0
    fuck = bool(re.search(r'\b(F|f)uck\b', word))  # 1509
    bitch = bool(re.search(r'\b(B|b)itch\b', word))  # 493
    shot = bool(re.search(r'\b(S|s)hot\b', word))  # 1434

    if (fuck | bitch | shot):
        score += 1

    return score


for f in followers:

    content = re.sub(url, "@url", f['content'])
    content = re.sub(spacechar, " ", f['content'])
    content = re.sub(name, "@user", f['content'])
    stemmer = nltk.stem.porter.PorterStemmer()
    stemming = ""
    lemmatized = ""
    sscore = 0
    lscore = 0
    for token in content.split(' '):
        new_content = stemmer.stem(token)
        new_contents = lemmatize(token)

        stemming += " " + new_content
        # print(stemming)
        lemmatized += " " + new_contents
        # print(lemmatized)

    for word in stemming.split(' '):
        sscore += fuzzy_rule(word)

    for word in lemmatized.split(' '):
        lscore += fuzzy_rule(word)

    sdata = dict(account=f['account'].lower(), id=f['id'], content=stemming.lower(), score=sscore)
    ldata = dict(account=f['account'].lower(), id=f['id'], content=lemmatized.lower(), score=lscore)
    sdatalist.append(sdata)
    ldatalist.append(ldata)

with open('Stemming.json', 'w', encoding='utf-8') as f:
    json.dump(sdatalist, f, ensure_ascii=False, indent=4)

with open('Lemmatize.json', 'w', encoding='utf-8') as f:
    json.dump(ldatalist, f, ensure_ascii=False, indent=4)





