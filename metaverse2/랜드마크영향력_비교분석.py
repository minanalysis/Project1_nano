

# # (메타)기본전처리

import pandas as pd
import matplotlib.pyplot as plt 
import seaborn as sns


# +
# 윈도우 : "Malgun Gothic"
# 맥 : "AppleGothic"
def get_font_family():
    """
    시스템 환경에 따른 기본 폰트명을 반환하는 함수
    """
    import platform
    system_name = platform.system()

    if system_name == "Darwin" :
        font_family = "AppleGothic"
    elif system_name == "Windows":
        font_family = "Malgun Gothic"
    else:
        # Linux(colab)
        # !apt-get install fonts-nanum -qq  > /dev/null
        # !fc-cache -fv

        import matplotlib as mpl
        mpl.font_manager._rebuild()
        findfont = mpl.font_manager.fontManager.findfont
        mpl.font_manager.findfont = findfont
        mpl.backends.backend_agg.findfont = findfont
        
        font_family = "NanumBarunGothic"
    return font_family

# 폰트설정
plt.rc("font", family=get_font_family())
# 마이너스폰트 설정
plt.rc("axes", unicode_minus=False)
# -

df=pd.read_csv("metabus2_1226.csv")

df.isnull().sum()

df.info()

df

df.drop('isMyTile',axis=1,inplace=True)
df.drop('lastPage',axis=1,inplace=True)
df.drop('allSellOrdersCount',axis=1,inplace=True)
df.drop(['createdAt','sellerId','currentPage','currentSellOrderCount','sellOrderId','uuid','sellerReferralCode'],axis=1,inplace=True)

df

df_meta_korea=df[df['address'].str.contains('Korea')==True]

df_meta_korea

# +
df_meta_korea['totalPrice']=df_meta_korea['totalPrice']/100*1200
df_meta_korea['boughtPrice']=df_meta_korea['totalPrice']/100*1200

#센트로 되어있는 Price 단위를->원으로 환산 

# +
cols=['직전가TP_원','시장가TP_원','동','주소','위경도']

#컬럼명 보기 쉽게 바꿔주기
# -

df_meta_korea.columns=cols

df_meta_korea

meta_gu_list=df_meta_korea['주소'].to_list()
meta_gu_list

# +
a=[]
for i in range(len(meta_gu_list)):
    temp=meta_gu_list[i].split(' ')[3]
    a.append(temp)
    
#주소에서 '구 컬럼'을 새로 만들어주기 위한 작업    
# -

df_meta_korea['구']=a

df_meta_korea

# # (메타) 구별 타일당 가격 구하기 

# ## (메타) 구별 전체 TP SUM 

df_meta_korea['구'].unique()

df_meta_korea.isnull().sum()

meta_guprice=df_meta_korea.groupby(by='구')[['시장가TP_원']].sum()

meta_guprice=meta_guprice.drop(['08505','08647','Anyang-si','Bucheon-si','Gimpo-si','Goyang-si','Guri-si','Gwacheon-si','Gwangmyeong-si','Gwangmyeong-si','York'])

meta_guprice=meta_guprice.drop(['Hanam-si','Seongnam-si','Namyangju-si'])

meta_guprice.nunique()

meta_guprice

# ## (메타) 확정 랜드마크 포함된 구 시장가TP 합

# +
#확정 랜드마크 포함된 구: 중구, 용산구, 성동구, 송파구, 종로구
##now_land_guprice
# -

now_land_guprice=meta_guprice.loc[['Jung-gu','Yongsan-gu','Seongdong-gu','Songpa-gu','Jongno-gu']]

now_land_guprice

index=['중구','용산구','성동구','송파구','종로구']

now_land_guprice.index=index

now_land_guprice.index


# ## (메타) 확정 랜드마크 포함된 구 면적과 타일수 변환

# +
#real_land_gusize
# -

real_price=pd.read_csv("finaldata/현실(구별)공시지가.csv")

real_price2=real_price[['시도','면적']]

real_price2=real_price2.set_index('시도')

real_land_gusize=real_price2.loc[['중구','용산구','성동구','송파구','종로구']]

real_land_gusize

real_land_gusize['타일수변환']=real_land_gusize['면적']/2/100

real_land_gusize.rename(columns={'시도':'구'})

# ##  (메타) 랜드마크포함 구별 타일당 가격 구하기 최종

now_land_guprice.reset_index(inplace=True)

real_land_gusize.reset_index(inplace=True)

now_land_guprice.rename(columns={'index':'구'})

meta_nowland_gu=pd.concat([real_land_gusize,now_land_guprice],axis=1).drop('index',axis=1)

meta_nowland_gu['타일당가격']=meta_nowland_gu['시장가TP_원']/meta_nowland_gu['타일수변환']

meta_nowland_gu[['시도','타일당가격']]

# # 산,강 제외한 구별 타일당 가격

# 확정 랜드마크 산, 강 불러오기 
df_mr_nowland=pd.read_csv("finaldata/(확정랜드 구)산,강.csv", encoding='cp949')
df_mr_nowland

df_mr_nowland.rename(columns={'Unnamed: 0':'구'})

meta_nowland_gu['산강제외_타일수']=meta_nowland_gu['타일수변환']-df_mr_nowland['타일수']

meta_nowland_gu

meta_nowland_gu['산강제외_시장가TP_원']=meta_nowland_gu['시장가TP_원']-df_mr_nowland['산강TP(won)']

meta_nowland_gu['산강제외_타일당가격']=meta_nowland_gu['산강제외_시장가TP_원']/meta_nowland_gu['산강제외_타일수']

meta_nowland_gu

meta_nowland_gu

# # 산, 강, 랜드마크 제외한 구별 타일당 가격

# +
#meta_landmark:랜드마크 타일수랑 가격 
# -

meta_landmark=pd.read_csv("finaldata/확정랜드마크_전처리.csv",encoding='cp949')
meta_landmark

meta_landmark['랜드마크_타일당가격']=meta_landmark['TP_원']/meta_landmark['타일수']

meta_landmark

meta_nowland_gu['산강랜드마크제외_TP']=meta_nowland_gu['산강제외_시장가TP_원']-meta_landmark['TP_원']

meta_nowland_gu

meta_nowland_gu['산강랜드마크제외_타일당가격']=meta_nowland_gu['산강랜드마크제외_TP']/(meta_nowland_gu['타일수변환']-df_mr_nowland['타일수']-meta_landmark['타일수'])

meta_nowland_gu.rename(columns={'시도':'구'},inplace=True)

meta_nowland_gu

# ## Y(영향력) 중 (1)번 비교 

df_Y1=meta_nowland_gu[['구','타일당가격','산강제외_타일당가격','산강랜드마크제외_타일당가격']]

df_Y1

sns.barplot(data=df_Y1,x='구',y='산강제외_타일당가격')

sns.barplot(data=df_Y1,x='구',y='산강랜드마크제외_타일당가격')

# # (메타) 25개 구 대비 확정 랜드마크 5개 구 

# +
#meta_all_gu->메타버스 모든 구의 실제면적, 타일수와 가격 
# -

구=['도봉구','동대문구','동작구','은평구','강북구','강동구','강남구','강서구','금천구','구로구','관악구','광진구','종로구','중구','중랑구','마포구','노원구','서초구','서대문구','성북구','성동구','송파구','양천구','영등포구','용산구']

meta_guprice=meta_guprice.reset_index()

meta_guprice['구']=구

meta_guprice

real_gusize

real_gusize=pd.read_csv('finaldata/구별현실면적')

meta_all_gu=pd.merge(meta_guprice, real_gusize, how="left", left_on="구", right_on="시도")

meta_all_gu=meta_all_gu.drop('시도',axis=1)

meta_all_gu['타일수']=meta_all_gu['면적']/2/100

meta_all_gu['타일당가격']=meta_all_gu['시장가TP_원']/meta_all_gu['타일수']

meta_all_gu.set_index('index')

plt.figure(figsize=(30,6))
sns.barplot(data=meta_all_gu,x='구',y='타일당가격')
#아무것도제외하지 않은 메타버스 구 타일당가격

df_Y1

test=pd.merge(meta_all_gu,df_Y1, how="left", left_on="구", right_on="구")

test

test['타일당가격_x']=[1129.3362019933688,
 1689.865745248529,
 10825.748246040353,
 1681.685910217615,
 1636.3231554623783,
 1346.3075466603336,
 14043.415820523034,
 4478.993649311763,
 1831.2506393885462,
 2615.153221933663,
 1942.2749949951562,
 2498.381562481858,
 19986.174466,
 32500.790867,
 1603.6490927594975,
 6256.33015610277,
 3479.6555602129374,
 8088.801051912382,
 2283.8561928834765,
 4163.937103547626,
 5237.222266,
 10905.248327,
 1933.2674063218806,
 14985.92518931901,
 11130.847324]

test

plt.figure(figsize=(30,6))
plt.ylim([0,60000])
sns.barplot(data=meta_all_gu,x='구',y='타일당가격')
#아무것도 제외하지 않은 메타버스2 구 타일당가격 순위 

plt.figure(figsize=(30,6))
plt.ylim([0,60000])
sns.barplot(data=test,x='구',y='타일당가격_x')
#확정랜드마크 포함된 5개 구는 산강랜드마크 제외한 타일당 가격 순위 

# # (메타) 예상랜드마크 

# ## (메타) 구별 전체 TP SUM

# +
## predict_land_guprice -> 예상 랜드마크를 포함한 구 가격 
## predict_landmark
# -

meta_guprice=meta_guprice.set_index('구')

predict_land_guprice=meta_guprice.loc[['중구','종로구','영등포구','동작구','서초구','강남구']]

predict_land_guprice

predict_landmark=pd.read_csv('finaldata/예상랜드마크_전처리.csv',encoding='cp949')

predict_landmark

meta_nowland_gu

real_predict_gu=real_price[(real_price['시도']=='강남구')|(real_price['시도']=='동작구')|(real_price['시도']=='서초구')|(real_price['시도']=='영등포구')|(real_price['시도']=='종로구')|(real_price['시도']=='중구')]

real_predict_gu=real_predict_gu[['시도','면적']]

real_predict_gu

real_predict_gu['타일수변환']=real_predict_gu['면적']/2/100

real_predict_gu=real_predict_gu.rename(columns=({'시도':'구'}))

real_predict_gu=real_predict_gu.sort_index()

meta_predict_gu=pd.concat([real_predict_gu,predict_land_guprice],axis=1)

meta_predict_gu=meta_predict_gu.sort_index()

mr_predict_land=pd.read_csv('finaldata/(예상랜드 구)산,강.csv',encoding='cp949')

mr_predict_land=mr_predict_land.sort_values('Unnamed: 0')

mr_predict_land=mr_predict_land.rename(columns={'Unnamed: 0':'구'})

mr_predict_land=mr_predict_land.set_index('구')

mr_predict_land

meta_predict_gu['타일당가격']=meta_predict_gu['시장가TP_원']/meta_predict_gu['타일수변환']

meta_predict_gu['산강제외_타일수']=meta_predict_gu['타일수변환']-mr_predict_land['타일수']

meta_predict_gu

meta_predict_gu['산강제외_시장가TP_원']=meta_predict_gu['시장가TP_원']-mr_predict_land['산강TP(won)']

meta_predict_gu['산강제외_타일당가격']=meta_predict_gu['산강제외_시장가TP_원']/meta_predict_gu['산강제외_타일수']

predict_landmark=predict_landmark.set_index('구')

meta_predict_gu['산강랜드마크제외_TP']=meta_predict_gu['산강제외_시장가TP_원']-predict_landmark['예상랜드TP_원']

meta_predict_gu['산강랜드마크제외_타일당가격']=meta_predict_gu['산강랜드마크제외_TP']/(meta_predict_gu['타일수변환']-mr_predict_land['타일수']-predict_landmark['타일수'])

# # 산,강 제외한 구별 예상랜드마크 타일당 가격

meta_predict_gu

(predict_landmark['예상랜드TP_원']/meta_predict_gu['시장가TP_원'])*100

# ## Y(영향력) 중 (2)번 비교

df_Y2=meta_predict_gu[['타일당가격','산강제외_타일당가격','산강랜드마크제외_타일당가격']]

df_Y2=df_Y2.reset_index()

df_Y2=df_Y2.rename(columns={'산강랜드마크제외_타일당가격':'산강예상랜드제외_타일당가격'})

df_Y2

plt.figure(figsize=(30,6))
sns.barplot(data=df_Y2,x='구',y='산강제외_타일당가격')

plt.figure(figsize=(30,6))
sns.barplot(data=df_Y2,x='구',y='산강예상랜드제외_타일당가격')

# # (메타)25개 구 대비 예상 랜드마크 6개 구 

real_gusize

meta_all_gu

df_Y2

test2=pd.merge(meta_all_gu,df_Y2, how="left", left_on="구", right_on="구")

test2=test2.drop(['타일당가격_y','산강제외_타일당가격'],axis=1)

test2['타일당가격_x']=[1129.3362019933688,
 1689.865745248529,
 10361.569333,
 1681.685910217615,
 1636.3231554623783,
 1346.3075466603336,
 12896.084835,
 4478.993649311763,
 1831.2506393885462,
 2615.153221933663,
 1942.2749949951562,
 2498.381562481858,
 41495.672772,
 60702.618637,
 1603.6490927594975,
 6256.33015610277,
 3479.6555602129374,
 9348.603023,
 2283.8561928834765,
 4163.937103547626,
 11750.842664830889,
 38063.7245604989,
 1933.2674063218806,
 16981.001643,
 27241.01235571753]

test2=test2.drop('산강예상랜드제외_타일당가격',axis=1)

test2

plt.figure(figsize=(30,6))
plt.ylim([0,80000])
sns.barplot(data=meta_all_gu,x='구',y='타일당가격')

plt.figure(figsize=(30,6))
plt.ylim([0,80000])
sns.barplot(data=test2,x='구',y='타일당가격_x')
#예상핸드마크 6개 구에서 6개구만.산강랜드뺀거. 

# +
#10퍼(예상랜드)가 빠졌는데, 단위면적당 순위 경향이 크게 많이 빠지지 않았다는 것은 애초에 주변시세 자체가 평균가격대가 있었다는 것. 
# -

# # Y(영향력) 중 (3)번 비교 

# +
# (랜드마크 8개 Total Price 합 / 랜드마크 8개 총 타일 수)  vs  (예상 랜드마크 8개 Total Price 합 / 예상 랜드마크 8개 총 타일 수)
# -

meta_landmark

predict_landmark

a=meta_landmark['TP_원'].sum()/meta_landmark['타일수'].sum()

b=predict_landmark['예상랜드TP_원'].sum()/meta_landmark['타일수'].sum()

a/b
