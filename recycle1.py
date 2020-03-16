# -*- coding: utf-8 -*-
"""
Created on Mon Mar 11 13:13:47 2019

@author: v-yisun
"""

import pandas as pd
from janome.tokenizer import Tokenizer
from janome.analyzer import Analyzer
from janome.charfilter import *
from janome.tokenfilter import *
import re
import numpy as np


#ファイルの読み込み
df = pd.read_excel(r"D:\Documents\work\COMMENTS_CLASS\2019Dec\FY20_12.xlsx")
#空白の置き換え
m = df.Message
m2 = m.str.replace('\n','')
m3 = m2.str.replace(' ','')
m4 = m3.str.replace(' ','')
df['Tweet'] = m2
#必要な列名のみ抽出
df = df[["Tweet","CreatedTime","UniversalMessageId","SenderScreenName","SenderListedName","Sender Followers Count","MessageType","Permalink"]]

text = m2.values
char_filters = [UnicodeNormalizeCharFilter()]
tokenizer = Tokenizer()
token_filters = [CompoundNounFilter(), POSKeepFilter('名詞'), LowerCaseFilter()]
a = Analyzer(char_filters, tokenizer, token_filters)
num = []
for i in range(len(text)):
    newsen = ''
    #mySent = re.sub('[?•()（）_→【】|...”「、>:」!,."...%*-]', ' ', text[i])
    mySent = text[i]
    #mySent = mySent.replace('?',' ')
    try:
        sen = mySent.strip()
        tokens = a.analyze(sen)#,wakati=True)
        if '@aws_official' in newsen:
            num.append(i)            
    except:
        print('abnormal!')
        
m2.drop(num,inplace=True)

#Tweet内容に下記ワードが入っていたらカテゴリ分け(会社名)
def company_cate(x):
    # print(isinstance(x, str))
    # print(type(x))

    if isinstance(x, str) == False:
        return '00_Blank'
    elif  "Microsoft" in x or "マイクロソフト" in x or "MS" in x or "Azure" in x or "microsoft" in x or "Visual Studio" in x or "VS" in x or "Visualstudio" in x or "VisualStudio" in x or "Xamarin" in x or "xamarin" in x:
        return '01_MS'
    elif "AWS" in x or "アマゾン" in x or "amazon" in x or "Amazon" in x or "aws" in x:
        return '02_AWS'
    elif "google" in x or "グーグル" in x or "Google" in x or "GCP" in x or "Gsuite" in x:
        return '03_Google'
    else:
        return 'other'


#もとのファイルにない列を追加
company_category = m4.apply(company_cate)
df['Company']  = company_category
df['SprinklrTopic'] = 'MS_Competitor'

#Follower数でカテゴライズ
def follower_class(x):
    if x <= 500:
        return '05_Follower#<500'
    elif x <= 1000:
        return '04_500<Follower#<1000'
    elif x <= 5000:
        return '03_1000<Follower#<5000'
    elif x <= 10000:
        return '02_5000<Follower#<10000'
    elif x <= 100000:
        return '01_10000<Follower#<100000'
    elif x > 100000:
        return '00_Follower#>1000000'

follower = df['Sender Followers Count']

FollowerClass = follower.apply(follower_class)
df['Follower rank'] = FollowerClass

#JSTに変換したうえ、日時を各カラムに分割
import datetime
d = df.CreatedTime
d2 = d + datetime.timedelta(hours=9)
d3 = d2.dt.date
d4 = d2.dt.month
d5 = d2.dt.year
d6 = d2.dt.hour
df['CreatedDateJST'] = d3
df['CreatedMonthJST'] = d4
df['CreatedYearJST'] = d5
df['CreatedHourJST'] = d6
def left(text, n):
    return text[:n]

#Tweeet投稿の最初の30文字だけ取ってきて、別の新しい列に入れる
Retweet = left(m2.str, 30)
df['Retweet'] = Retweet

#Tweet内容に下記ワードが入っていたらカテゴリ分け(どの分野についての話題かカテゴリ分け)
def func_cate(x):
    if isinstance(x, str) == False:
        return '00_Blank'
    elif  "ディープラーニング" in x or "人工知能" in x or "シンギュラリティ" in x or "MachineLearning" in x or "FaceAPI" in x or "Bot" in x or "Analysis" in x or "Analytics" in x or "Translator" in x or "Machinelearning" in x or "Kinect" in x or "IoT" in x or "深層学習" in x or "AI機能" in x or "AI技術" in x or "AI研究" in x or "AIは" in x or "AIが" in x or "AIで" in x or "AIを" in x or "りんな" in x or "自動翻訳" in x or "機械学習" in x or "AIの" in x or "Sketch2code" in x or "sketch2code" in x or "Sketch2Code" in x or "顔認識" in x or "音声認識" in x or "画像認識" in x:
        return 'AI'
    elif "cloud" in x or "クラウド" in x or "Cloud" in x or "Azure" in x or "azure" in x or "AWS" in x or "aws" in x or "Aws"in x or "GCP" in x or "gcp" in x:
        return 'Cloud'
    elif "働き方" in x or "残業" in x or "ワークスタイル" in x or "workstyle" in x or "時短" in x or "リモートワーク" in x or "育児" in x or "ワークライフバランス" in x or "Loft" in x or "テレワーク" in x or "週休三日" in x or "週休3日" in x or "他で必要とされる人がここで働きたいと思える環境を作る" in x or '週休３日' in x or 'マイクロソフト澤氏が' in x:	
        return 'Workstyle'
    elif " セキュリティ" in x or "脆弱性" in x or "ウィルス" in x or "マルウェア" in x or "ランサムウェア" in x or "ファイヤーウォール" in x or "緊急パッチ" in x or "感染" in x or "アップデート" in x or "更新" in x:
        return 'Security'
    elif "Microsoft365" in x or "M365" in x or "O365" in x or "office365" in x or "MicrosoftOffice" in x or "MicrosoftAccess" in x or "Office365" in x or ("Office" and "365") in x or "excel" in x or "Excel" in x or "word" in x or "Word" in x or "Powerpoint" in x or "powerpoint" in x or "パワポ" in x or "windows" in x or "Windows" in x or "Skype" in x or "skype" in x or "surface" in x or "Surface" in x or "Teams" in x or "teams" in x or "Edge" in x or "IME" in x or "flow" in x or "Flow" in x or "ティラノサウルス" in x or 'IE' in x or 'ハードウェアの安全な取り外し' in x:
        return 'MS product'
    elif "Googlehome" in x or "GoogleHome" in x or "googlehome" in x or "echo" in x or "Echo" in x:
        return 'Smart Speaker'
    elif "OK,Google" in x or "OK,google" in x or "Alexa" in x or "alexa" in x or "cortana" in x or "Cortana" in x:
        return 'Smart Speaker'
    elif "VirtualReality" in x or "MixedReality" in x or "Hololens" in x or "ホロレンズ" in x:
        return 'VR'
    elif "GoogleCloudNext" in x or "TechSummit" in x or "テックサミット" in x or "Summit" in x or "イベント" in x:
        return 'Event'
    elif "株式市場" in x:
        return 'Stock Market'
    elif "買収" in x or "合併" in x or "提携" in x or "経営" in x:
        return 'Business News'
    elif "ブロックチェーン" in x or "blockchain" in x or "ビットコイン" in x or "仮想通貨" in x or "リップル" in x:
        return 'ブロックチェーン'
    elif "オープンソース" in x or ("OSS" and "親和性") in x or "Github" in x or "github" in x:
        return 'オープンソース'
    elif "Googlepay" in x or "GooglePay"in x or "googlepay"in x:
        return 'Google Pay'
    elif "minecraft" in x or "Minecraft" in x or "マインクラフト" in x or "ビデオゲーム" in x or "videogame" in x or "MicrosoftFlightSimulator" in x:
        return "Game"
    elif "タイトルを発表" in x or "タイトル発表" in x or "project scarlett" in x or "プロジェクト スカーレット" in x:
        return "Xbox"
    else:
        return 'other'

#新しい列（カテゴリ）を作って上記のカテゴリを入れる
category2 = m4.apply(func_cate)
df['Category'] = category2.copy()


#df.drop(df.index[(df['Category']=='other') & (df['Tweet'].str.contains('グーグル社長'))],inplace = True)
#df.reset_index()

#df1 = df[0:60000].copy()
#df2 = df[60001:120000].copy()
#df3 = df[120001:].copy()

#df1[df1['Company'].str.contains('01_MS|02_AWS|03_Google')].to_csv(r"D:\Documents\work\COMMENTS_CLASS\Listening_Competitor_FY1006Feb_test_1.csv", index=False, encoding='UTF-16')
#df2[df2['Company'].str.contains('01_MS|02_AWS|03_Google')].to_csv(r"D:\Documents\work\COMMENTS_CLASS\Listening_Competitor_FY1006Feb_test_2.csv", index=False, encoding='UTF-16')
#df3[df3['Company'].str.contains('01_MS|02_AWS|03_Google')].to_csv(r"D:\Documents\work\COMMENTS_CLASS\Listening_Competitor_FY1006Feb_test_3.csv", index=False, encoding='UTF-16')

######################################
category3 = df['Category'].copy()
index = [i for i in range(len(category3))]
df['index'] = index.copy()
new = df[['Tweet','index']][df['Category']=='other'].copy()
texto = new['Tweet'].values
mark = new['index'].values
#textm = np.unique(texto)
text = []
nmark = []
for i in range(len(texto)):
    if '投稿日' not in texto[i]:
        text.append(texto[i])
        nmark.append(mark[i])
#######tokenize####################
char_filters = [UnicodeNormalizeCharFilter()]
tokenizer = Tokenizer()
token_filters = [CompoundNounFilter(), POSKeepFilter('名詞'), LowerCaseFilter()]
a = Analyzer(char_filters, tokenizer, token_filters)
tdesc = []
filt = ['月','日','年','の','投稿']
for i in range(len(text)):
    newsen = ''
    #mySent = re.sub('[?•()（）_→【】|...”「、>:」!,."...%*-]', ' ', text[i])
    mySent = text[i]
    #mySent = mySent.replace('?',' ')
    try:
        sen = mySent.strip()
        tokens = a.analyze(sen)#,wakati=True)
        for j in tokens:
            if ('\\' not in j.surface) and ('/' not in j.surface):
                newsen = newsen + j.surface +' '
        tdesc.append(newsen)
        print(newsen)            
    except:
        tdesc.append('NaN')
    
char_filters = [UnicodeNormalizeCharFilter()]
tokenizer = Tokenizer()
token_filters = [CompoundNounFilter(), POSKeepFilter('名詞'), LowerCaseFilter()]
a = Analyzer(char_filters, tokenizer, token_filters)
ndesc = []
filt = ['月','日','年','の','投稿','月日']
for i in range(len(tdesc)):
    newsen = ''
    mySent = re.sub('[@=#¥~^<。$;+⇒•()（）_→【】{}|...”「、>:」!,."...%*-]', ' ', tdesc[i])
    mySent = mySent.replace('?',' ').replace('[',' ').replace(']',' ').replace("'",' ')
    sen = mySent.strip()
    tokens = a.analyze(sen)#,wakati=True)
    for j in tokens:
        if j.surface not in filt:
            newsen = newsen + j.surface +' '
    #newsen = re.sub(r'[0-9]+', '', newsen)
    print(newsen)
    ndesc.append(newsen)

IDEOGRAPHIC_SPACE = 0x3000
def is_asian(char):
    """Is the character Asian?"""

    # 0x3000 is ideographic space (i.e. double-byte space)
    # Anything over is an Asian character
    return ord(char) > IDEOGRAPHIC_SPACE

def cutwords(word):
    sent = ''
    w = word[0]
    a = is_asian(word[0])
    for i in range(1,len(word)):
        b = is_asian(word[i])
        if a ==b:
            w = w+word[i]
        else:
            sent = sent+w+' '
            a = b
            w = word[i]
    sent = sent+w
    return sent

fdesc = []        
for tex in ndesc:
    sent = ''
    s = tex.split()
    for tok in s:
        sent = sent + cutwords(tok)+' '
    fdesc.append(sent) 

##############function#############
keywords = pd.read_excel(r"D:\Documents\work\COMMENTS_CLASS\category_words.xlsx")  
kw = keywords.values
 
def func_cate_sy(x,kw):
    #if isinstance(x, str) == False:
        #return 'other'
    for word in kw[:,0]:
        if pd.isnull(word):
            break
        else:
            if word in x:
                return 'AI'
    for word in kw[:,1]:
        if pd.isnull(word):
            break
        else:
            if word in x:
                return 'Cloud'
    for word in kw[:,2]:
        if pd.isnull(word):
            break
        else:
            if word in x:
                return 'Workstyle'
    for word in kw[:,3]:
        if pd.isnull(word):
            break
        else:
            if word in x:
                return 'Security'
    for word in kw[:,4]:
        if pd.isnull(word):
            break
        else:
            if word in x or (("office" in x) and ("microsoft" in x)) or (("office" in x) and ("365" in x)) or (("internet" in x) and ("explorer" in x)) or (("visual" in x) and ("studio" in x)) or (("microsoft" in x) and ("store" in x)):
                return 'MS product'
    for word in kw[:,5]:
        if pd.isnull(word):
            break
        else:
            if word in x or (("google" in x) and ("home" in x)) or (('ok' in x) and ('google' in x)):
                return 'Smart Speaker'
    for word in kw[:,6]:
        if pd.isnull(word):
            break
        else:
            if word in x:
                return 'VR'
    for word in kw[:,7]:
        if pd.isnull(word):
            break
        else:
            if word in x:
                return 'Event'
    for word in kw[:,8]:
        if pd.isnull(word):
            break
        else:
            if word in x:
                return 'Stock Market'
    for word in kw[:,9]:
        if pd.isnull(word):
            break
        else:
            if word in x:
                return 'Business News'
    for word in kw[:,10]:
        if pd.isnull(word):
            break
        else:
            if word in x:
                return 'ブロックチェーン'
    for word in kw[:,11]:
        if pd.isnull(word):
            break
        else:
            if word in x or (("oss" in x) and ("親和性" in x)):
                return 'オープンソース'
    for word in kw[:,12]:
        if pd.isnull(word):
            break
        else:
            if word in x or (('google' in x) and ('pay' in x)):
                return 'Google Pay'
    return 'other'
    
#############recycle###################
regroup = []
for sent in fdesc:
    regroup.append(func_cate_sy(sent,kw))
    
regroup = np.array(regroup)
nmark = np.array(nmark)

group = np.unique(regroup)
category3 = list(category3)
category3 = np.array(category3)

for name in group:
    category3[nmark[regroup==name].tolist()] = name
    
df['Category'] = category3.copy()
df.drop(['index'], axis=1)
df=df[df['Company'] !='00_Blank'].copy()

extract = df[['Tweet','Permalink','Company','Category','MessageType']];
extract1 = extract[extract['Company']=='01_MS']

extract2 = extract1[extract1['Category']=='other']
extract3 = extract2[extract2['MessageType']!='Forums']

extract4 = extract3[['Tweet','Permalink']]
extract4.to_csv(r"D:\Documents\work\COMMENTS_CLASS\2019Dec\other.csv",index = False);

df1 = df[0:50000].copy()
df2 = df[50001:100000].copy()
df3 = df[100001:150000].copy()
df4 = df[150001:200000].copy()
df5 = df[200001:].copy()
#df6 = df[250001:].copy()
#df7 = df[300001:350000].copy()
#df8 = df[350001:400000].copy()
#df9 = df[400001:450000].copy()
#df10 = df[450001:].copy()


df1[df1['Company'].str.contains('01_MS|02_AWS|03_Google')].to_csv(r"D:\Documents\work\COMMENTS_CLASS\2019Dec\Listening_Competitor_FY20_12_1.csv", index=False, encoding='UTF-16')
df2[df2['Company'].str.contains('01_MS|02_AWS|03_Google')].to_csv(r"D:\Documents\work\COMMENTS_CLASS\2019Dec\Listening_Competitor_FY20_12_2.csv", index=False, encoding='UTF-16')
df3[df3['Company'].str.contains('01_MS|02_AWS|03_Google')].to_csv(r"D:\Documents\work\COMMENTS_CLASS\2019Dec\Listening_Competitor_FY20_12_3.csv", index=False, encoding='UTF-16')
df4[df4['Company'].str.contains('01_MS|02_AWS|03_Google')].to_csv(r"D:\Documents\work\COMMENTS_CLASS\2019Dec\Listening_Competitor_FY20_12_4.csv", index=False, encoding='UTF-16')
df5[df5['Company'].str.contains('01_MS|02_AWS|03_Google')].to_csv(r"D:\Documents\work\COMMENTS_CLASS\2019Dec\Listening_Competitor_FY20_12_5.csv", index=False, encoding='UTF-16')
df6[df6['Company'].str.contains('01_MS|02_AWS|03_Google')].to_csv(r"D:\Documents\work\COMMENTS_CLASS\Jul\Listening_Competitor_FY20_07_6.csv", index=False, encoding='UTF-16')
#df7[df7['Company'].str.contains('01_MS|02_AWS|03_Google')].to_csv(r"D:\Documents\work\COMMENTS_CLASS\Aug\Listening_Competitor_FY20_08_7.csv", index=False, encoding='UTF-16')
#df8[df8['Company'].str.contains('01_MS|02_AWS|03_Google')].to_csv(r"D:\Documents\work\COMMENTS_CLASS\Aug\Listening_Competitor_FY20_08_8.csv", index=False, encoding='UTF-16')
#df9[df9['Company'].str.contains('01_MS|02_AWS|03_Google')].to_csv(r"D:\Documents\work\COMMENTS_CLASS\Aug\Listening_Competitor_FY20_08_9.csv", index=False, encoding='UTF-16')
#df10[df10['Company'].str.contains('01_MS|02_AWS|03_Google')].to_csv(r"D:\Documents\work\COMMENTS_CLASS\Aug\Listening_Competitor_FY20_08_10.csv", index=False, encoding='UTF-16')
