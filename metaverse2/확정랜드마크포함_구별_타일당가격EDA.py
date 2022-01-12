## (메타) 구별 타일당 가격 구하기 

meta_guprice=df_meta_korea.groupby(by='구')[['시장가TP_원']].sum()

#구별 전체 TP SUM 구하기 

meta_guprice=meta_guprice.drop(['Hanam-si','Seongnam-si','Namyangju-si'.'08505','08647','Anyang-si','Bucheon-si','Gimpo-si','Goyang-si','Guri-si','Gwacheon-si','Gwangmyeong-si','Gwangmyeong-si','York'])

# 서울시가 아닌 불필요한 데이터 제거 

meta_guprice.nunique()
#서울특별시 구가 아닌 행을 삭세해주니 25개로 법정구 갯수가 맞음


##확정 랜드마크 포함된 구: 중구, 용산구, 성동구, 송파구, 종로구
##now_land_guprice 로 파생변수 생성.

now_land_guprice=meta_guprice.loc[['Jung-gu','Yongsan-gu','Seongdong-gu','Songpa-gu','Jongno-gu']]


index=['중구','용산구','성동구','송파구','종로구']

now_land_guprice.index=index

#구 명을 한글로 바꿔준 후, 인덱스로 변환 


##확정 랜드마크 포함된 구 지도면적과 타일수 변환
##real_land_gusize로 파생변수 생성.

real_price=pd.read_csv("finaldata/현실(구별)공시지가.csv")
#부동산 사이트에 있는 현실 가액 전처리한 데이터 불러오기.

real_price2=real_price[['시도','면적']]

real_price2=real_price2.set_index('시도')

real_land_gusize=real_price2.loc[['중구','용산구','성동구','송파구','종로구']]

#현실 가액 전처리 데이터에서 필요한 데이터만을 추출하여 파생변수에 담아주기

real_land_gusize['타일수변환']=real_land_gusize['면적']/2/100

#메타버스2 플랫폼 상 면적은 지도를 1/2로 축소함. 타일 한개는 10바이10미터의 크기를 가지고 있음. 


## 확정 랜드마크포함 구별 타일당 가격 구하기 최종 EDA 
## meta_nowland_gu로 파생변수 생성.

meta_nowland_gu=pd.concat([real_land_gusize,now_land_guprice],axis=1).drop('index',axis=1)

meta_nowland_gu['타일당가격']=meta_nowland_gu['시장가TP_원']/meta_nowland_gu['타일수변환']

meta_nowland_gu[['구','타일당가격']]

