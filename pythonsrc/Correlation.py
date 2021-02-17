### CSV Paths for Data
symbol1 = 'BTCUSDT'
symbol2 = 'BCHUSDT'
tick_interval = '15m'
symbol1Path = 'D:/AD/pythonsrc/data/'+symbol1+'_'+tick_interval+'.csv'
symbol2Path = 'D:/AD/pythonsrc/data/'+symbol2+'_'+tick_interval+'.csv'

s1 = pd.read_csv(symbol1Path)
s2 = pd.read_csv(symbol2Path)

s = pd.concat([s1.close,s2.close],axis=1,keys=['s1','s2'])

s = s.dropna()

s[['s1','s2']]  =scaler.fit_transform(s[['s1','s2']])
s.corr(method='pearson')