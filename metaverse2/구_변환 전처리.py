# # (메타) 메타버스 크롤링 데이터에서, 서울 & 서울 25개 구 별 시장 거래에 대한 데이터를 추출하기 위한 전처리 

import pandas as pd
import matplotlib.pyplot as plt 
import seaborn as sns


# +
df=pd.read_csv("metabus2_1226.csv")

#1226일자로 메타버스 내의 '빠른토지구매' 크롤링한 데이터불러오기

# +
df.drop('isMyTile',axis=1,inplace=True)
df.drop('lastPage',axis=1,inplace=True)
df.drop('allSellOrdersCount',axis=1,inplace=True)
df.drop(['createdAt','sellerId','currentPage','currentSellOrderCount','sellOrderId','uuid','sellerReferralCode'],axis=1,inplace=True)

#메타버스 크롤링 데이터 중 불필요한 데이터 삭제 

# +
df_meta_korea=df[df['address'].str.contains('Korea')==True]
#뉴욕 제외하기 위한 작업, korea 데이터셋 생성

# +
df_meta_korea['totalPrice']=df_meta_korea['totalPrice']/100*1200
df_meta_korea['boughtPrice']=df_meta_korea['totalPrice']/100*1200

#메타버스 크롤링 데이터에서, 센트로 되어있는 Price 단위를->원으로 환산 

# +
cols=['직전가TP_원','시장가TP_원','동','주소','위경도']

df_meta_korea.columns=cols

#컬럼명 보기 쉽게 바꿔주기

# +
meta_gu_list=df_meta_korea['주소'].to_list()

a=[]
for i in range(len(meta_gu_list)):
    temp=meta_gu_list[i].split(' ')[3]
    a.append(temp)

df_meta_korea['구']=a

#주소에서 '구 컬럼'을 새로 만들어주기 위한 작업   

