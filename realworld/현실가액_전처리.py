df=pd.read_csv("data/현실가액.csv",encoding='cp949')

df=df.drop(['민유지', 'Unnamed: 6',
       'Unnamed: 7', '국유지', 'Unnamed: 9', 'Unnamed: 10', '시,도유지',
       'Unnamed: 12', 'Unnamed: 13', '군유지', 'Unnamed: 15', 'Unnamed: 16', '법인',
       'Unnamed: 18', 'Unnamed: 19', '비법인', 'Unnamed: 21', 'Unnamed: 22', '기타',
       'Unnamed: 24', 'Unnamed: 25'],axis=1)
#필요없는 컬럼 지우기 

df
#면적은 키로미터제곱, 가액은 = 면적*(지분)*개별공시지가*(50/100) , 단위는 십억원

df.set_index('시군구')
#인덱스 정리하기 

df.columns=['시군구','시도','면적','지번수','가액']

df=df.drop('시군구',axis=1)

df=df.drop(index=[0,1,2])
#필요없는 행 삭제 

df.set_index('시도')
#시도명으로 인덱스 설정
