##확정 랜드마크의 영향력에 대한 비교 분석

meta_landmark=pd.read_csv("finaldata/확정랜드마크_전처리.csv",encoding='cp949')
#확정랜드마크 가격 및 타일수 불러오기

meta_landmark['랜드마크_타일당가격']=meta_landmark['TP_원']/meta_landmark['타일수']

meta_nowland_gu['산강랜드마크제외_TP']=meta_nowland_gu['산강제외_시장가TP_원']-meta_landmark['TP_원']

meta_nowland_gu['산강랜드마크제외_타일당가격']=meta_nowland_gu['산강랜드마크제외_TP']/(meta_nowland_gu['타일수변환']-df_mr_nowland['타일수']-meta_landmark['타일수'])

#메타버스 내의 기본(아무것도 제외안함)타일수 및 시장가 & 산강제외 타일수 및 시장가 & 산강랜드마크제외 타일수 및 시장가


## 확정 랜드마크의 영향력 분석을 위한 최종 파생변수로 df_Y1 생성.

df_Y1=meta_nowland_gu[['구','타일당가격','산강제외_타일당가격','산강랜드마크제외_타일당가격']]

sns.barplot(data=df_Y1,x='구',y='산강제외_타일당가격')

sns.barplot(data=df_Y1,x='구',y='산강랜드마크제외_타일당가격')


## (메타) 25개 구(서울특별시) 대비 확정 랜드마크 5개 구 비교

구=['도봉구','동대문구','동작구','은평구','강북구','강동구','강남구','강서구','금천구','구로구','관악구','광진구','종로구','중구','중랑구','마포구','노원구','서초구','서대문구','성북구','성동구','송파구','양천구','영등포구','용산구']

meta_guprice=meta_guprice.reset_index()
#메타버스 내의 구 별 가격 구해둔 데이터셋

real_gusize=pd.read_csv('finaldata/구별현실면적')
#현실 면적 구해둔 데이터셋 

meta_all_gu=pd.merge(meta_guprice, real_gusize, how="left", left_on="구", right_on="시도")
#메타버스의 구당 가격과 구의 타일수를 합쳐주기 위한 병합

meta_all_gu=meta_all_gu.drop('시도',axis=1)

meta_all_gu['타일수']=meta_all_gu['면적']/2/100
#현실과 타일의 스케일 차이를 조정한 값

meta_all_gu['타일당가격']=meta_all_gu['시장가TP_원']/meta_all_gu['타일수']

meta_all_gu.set_index('index')

plt.figure(figsize=(30,6))
sns.barplot(data=meta_all_gu,x='구',y='타일당가격')
#아무것도 제외하지 않은 메타버스 구 타일당가격

test=pd.merge(meta_all_gu,df_Y1, how="left", left_on="구", right_on="구")
#meta_all_gu->메타버스 모든 구의 실제면적, 타일수와 가격 
##test는 랜드마크를 제외한 25개 구의 타일당 가격 관련 데이터셋 

#확정 랜드마크 포함한 5개구는 '타일당가격_x'에 산,강,메타버스가 제외된 값이 들어가 있음! 

plt.figure(figsize=(30,6))
plt.ylim([0,60000])
sns.barplot(data=meta_all_gu,x='구',y='타일당가격')
#아무것도 제외하지 않은 메타버스2 구 타일당가격 순위 

plt.figure(figsize=(30,6))
plt.ylim([0,60000])
sns.barplot(data=test,x='구',y='타일당가격_x')
#확정랜드마크 포함된 5개 구는 산강랜드마크 제외한 타일당 가격 순위 

##-> 랜드마크를 포함한 구별 시장가 순위와 랜드마크를 제외한 구별 시장가 순위 비교 
