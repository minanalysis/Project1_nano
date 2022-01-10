##예상 랜드마크의 영향력에 대한 비교 분석 

predict_land_guprice=meta_guprice.loc[['중구','종로구','영등포구','동작구','서초구','강남구']]
#predict_land_guprice: 예상 랜드마크를 포함한 구의 시장가 

predict_landmark=pd.read_csv('finaldata/예상랜드마크_전처리.csv',encoding='cp949')
#예상 랜드마크를 포함함 구의 시장가를 predict_landmark로 불러오기

real_predict_gu=real_price[(real_price['시도']=='강남구')|(real_price['시도']=='동작구')|(real_price['시도']=='서초구')|(real_price['시도']=='영등포구')|(real_price['시도']=='종로구')|(real_price['시도']=='중구')]

real_predict_gu=real_predict_gu[['시도','면적']]

real_predict_gu['타일수변환']=real_predict_gu['면적']/2/100

real_predict_gu=real_predict_gu.rename(columns=({'시도':'구'}))

real_predict_gu=real_predict_gu.sort_index()

real_predict_gu
#예상 랜드마크가 포함된 구의 실면적과 타일수변환 전처리한 데이터셋 

meta_predict_gu=pd.concat([real_predict_gu,predict_land_guprice],axis=1)

meta_predict_gu=meta_predict_gu.sort_index()

mr_predict_land=pd.read_csv('finaldata/(예상랜드 구)산,강.csv',encoding='cp949')
#mr_predict_land: 예상 랜드마크가 포함된 구의 산,강 데이터셋


meta_predict_gu['타일당가격']=meta_predict_gu['시장가TP_원']/meta_predict_gu['타일수변환']

meta_predict_gu['산강제외_타일수']=meta_predict_gu['타일수변환']-mr_predict_land['타일수']

meta_predict_gu['산강제외_시장가TP_원']=meta_predict_gu['시장가TP_원']-mr_predict_land['산강TP(won)']

meta_predict_gu['산강제외_타일당가격']=meta_predict_gu['산강제외_시장가TP_원']/meta_predict_gu['산강제외_타일수']

predict_landmark=predict_landmark.set_index('구')

meta_predict_gu['산강랜드마크제외_TP']=meta_predict_gu['산강제외_시장가TP_원']-predict_landmark['예상랜드TP_원']

meta_predict_gu['산강랜드마크제외_타일당가격']=meta_predict_gu['산강랜드마크제외_TP']/(meta_predict_gu['타일수변환']-mr_predict_land['타일수']-predict_landmark['타일수'])

meta_predict_gu
##메타버스 내의 기본(아무것도 제외안함)타일수 및 시장가 & 산강제외 타일수 및 시장가 & 산,강,예상랜드마크제외 타일수 및 시장가 


##예상 랜드마크의 영향력 분석을 위한 최종 파생변수로 df_Y2 생성.

df_Y2=meta_predict_gu[['타일당가격','산강제외_타일당가격','산강랜드마크제외_타일당가격']]

df_Y2=df_Y2.reset_index()

df_Y2=df_Y2.rename(columns={'산강랜드마크제외_타일당가격':'산강예상랜드제외_타일당가격'})

plt.figure(figsize=(30,6))
sns.barplot(data=df_Y2,x='구',y='산강제외_타일당가격')

plt.figure(figsize=(30,6))
sns.barplot(data=df_Y2,x='구',y='산강예상랜드제외_타일당가격')


test2=pd.merge(meta_all_gu,df_Y2, how="left", left_on="구", right_on="구")
##test2는 랜드마크를 제외한 25개 구의 타일당 가격 관련 데이터셋  

test2=test2.drop(['타일당가격_y','산강제외_타일당가격'],axis=1)

plt.figure(figsize=(30,6))
plt.ylim([0,80000])
sns.barplot(data=meta_all_gu,x='구',y='타일당가격')

plt.figure(figsize=(30,6))
plt.ylim([0,80000])
sns.barplot(data=test2,x='구',y='타일당가격_x')
##-> 예상 랜드마크를 포함한 구별 시장가 순위와 예상 랜드마크를 제외한 구별 시장가 순위 비교 

## 추가 분석 : 확정 랜드마크 타일당 가격 대비 예상 랜드마크 타일 당 가격 

meta_landmark  

predict_landmark  

a=meta_landmark['TP_원'].sum()/meta_landmark['타일수'].sum() 

b=predict_landmark['예상랜드TP_원'].sum()/meta_landmark['타일수'].sum()

a/b


