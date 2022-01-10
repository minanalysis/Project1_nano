## 산,강 제외한 구별 타일당 가격 EDA 

## 확정 랜드마크 산, 강 불러오기 
## df_mr_nowland로 파생변수 생성. 

df_mr_nowland=pd.read_csv("finaldata/(확정랜드 구)산,강.csv", encoding='cp949')
df_mr_nowland.rename(columns={'Unnamed: 0':'구'})

##meta_nowland_gu(확정랜드마크 포함 구별 데이터프레임)에 필요한 데이터 병합해주기

meta_nowland_gu['산강제외_타일수']=meta_nowland_gu['타일수변환']-df_mr_nowland['타일수']

meta_nowland_gu['산강제외_시장가TP_원']=meta_nowland_gu['시장가TP_원']-df_mr_nowland['산강TP(won)']

meta_nowland_gu['산강제외_타일당가격']=meta_nowland_gu['산강제외_시장가TP_원']/meta_nowland_gu['산강제외_타일수']
