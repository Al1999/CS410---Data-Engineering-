import pandas as pd 
import hashlib  
import numpy as np

df1 = pd.read_csv('/u/aya9/cs410/data_integ/acs2017_census_tract_data.csv',usecols=['State','County','TotalPop', 'Poverty','IncomePerCap'])
df2 = pd.read_csv('/u/aya9/cs410/data_integ/COVID_county_data.csv',usecols=['state','county','date','cases','deaths'], parse_dates=['date'])


df =  pd.DataFrame()
df = pd.concat([df1],ignore_index=True) 

#part A:

county_info = df[['County', 'State' ,'TotalPop','Poverty', 'IncomePerCap']]
aggregation_functions1 = { 'County':'first', 'State':'first' ,'TotalPop':'sum', 'Poverty':'mean', 'IncomePerCap':'mean' }
df_new = county_info.groupby(['State','County']).aggregate(aggregation_functions1)


df_new['Key_Id'] = df_new['County'] + ' ' + df_new['State']
for  n in df_new['Key_Id']:
    m = hashlib.md5()
    k = (n).encode('utf-8')
    m.update(k)
    id = str(int(m.hexdigest(), 16))[0:12]
    df_new['Key_Id'] = df_new['Key_Id'].replace([n],id)
    

#print(df_new['Key_Id'])


#print(df_new)
#print(df_new  [df_new ["County"] == "Loudoun County"])
#print(df_new  [df_new ["County"] == "Washington County"])
#print(df_new  [df_new ["County"] == "Harlan County"])
#print(df_new  [df_new ["County"] == "Malheur County"])
max =  df_new["TotalPop"].max()
#print( df_new[df_new ["TotalPop"] == max] )

min = df_new["TotalPop"].min()
#print( df_new[df_new ["TotalPop"] == min] )





#part B:

"""
covid = df2[['state','county','date','cases','deaths']]
aggregation_functions2 = { 'state': 'first', 'county' : 'first', 'date': 'last', 'cases':'sum', 'deaths':'sum' }
dfg = df2.groupby('county').get_group('Malheur')
dfs = dfg.groupby('state').get_group('Oregon')
dfnew = dfs.resample('M', on='date').aggregate(aggregation_functions2)

print(dfnew)
#print(dfnew[dfnew["county"] == "Malheur"])
"""
covid = df2[['state','county','date','cases','deaths']]
covid['Month'] = covid['date'].dt.strftime('%b')
covid['Year'] = covid['date'].dt.strftime('%Y')
covid['county']  = covid['county'] + ' County'

aggreagation_functions2 = {'state': 'first', 'county': 'first', 'Month': 'first', 'Year': 'first', 'cases' : 'sum', 'deaths': 'sum'}
covid_monthly = covid.groupby(['state', 'county', 'Month', 'Year']).aggregate(aggreagation_functions2)
#print(covid_monthly)

#print(covid_monthly[covid_monthly["county"] == "Malheur County"])

#creating a new special key Id based on the name of the state and the county which we already add County word to it so it matchs the acs2017 data set.
covid_monthly['Key_Id'] = covid_monthly['county'] + ' ' + covid_monthly['state']

for  n in covid_monthly['Key_Id']:
    m = hashlib.md5()
    k = (n).encode('utf-8')
    m.update(k)
    id = str(int(m.hexdigest(), 16))[0:12]
    covid_monthly['Key_Id'] = covid_monthly['Key_Id'].replace([n],id)

#print(covid_monthly['Key_Id'])


#Part C:

COVID_summary = pd.DataFrame()
covid_d = covid_monthly[['Key_Id','state','county','cases','deaths']]

aggreagation_functions3 = {'Key_Id': 'first', 'state': 'first', 'county': 'first', 'cases' : 'sum', 'deaths': 'sum'}
covid_d2 = covid_d.groupby(['Key_Id']).aggregate(aggreagation_functions3)

census_d = df_new[['Key_Id','County', 'State' ,'TotalPop','Poverty', 'IncomePerCap']]
covid_d3 = covid_d2[['Key_Id','county','state','cases','deaths']]
covid_d3.rename(columns = {'county':'County', 'state':'State'}, inplace = True)
frames = [census_d, covid_d3]


aggreagation_functions4 = {'Key_Id': 'first' ,'State': 'first', 'County': 'first', 'cases' : 'sum', 'deaths': 'sum','TotalPop':'sum', 'Poverty':'sum', 'IncomePerCap':'sum'}
COVID_summary = pd.concat(frames).groupby(['Key_Id']).aggregate(aggreagation_functions4)

#print(COVID_summary)
for n in COVID_summary['TotalPop']:
    c = int(n)
    COVID_summary['TotalPop'] = COVID_summary['TotalPop'].replace([n],c)

for n in COVID_summary['cases']:
    c = int(n)
    COVID_summary['cases'] = COVID_summary['cases'].replace([n],c)

for n in COVID_summary['deaths']:
    c = int(n)
    COVID_summary['deaths'] = COVID_summary['deaths'].replace([n],c)

COVID_summary['TotalCasesPer100K']= np.where(COVID_summary['TotalPop']!= 0.0, COVID_summary['cases']/(COVID_summary['TotalPop']/100000), np.nan)
COVID_summary['TotalDeathsPer100K']= np.where(COVID_summary['TotalPop']!= 0.0, COVID_summary['deaths']/(COVID_summary['TotalPop']/100000), np.nan)
#COVID_summary['TotalCasesPer100K']= COVID_summary.apply(lambda row: int(row.cases)/(int(row.TotalPop)/100000),  axis = 1) 
    
#print(COVID_summary.head(10))
print(COVID_summary.loc[(COVID_summary['County'] == 'Washington County') & (COVID_summary['State'] == 'Oregon')])
print(COVID_summary.loc[(COVID_summary['County'] == 'Malheur County') & (COVID_summary['State'] == 'Oregon')])
print(COVID_summary.loc[(COVID_summary['County'] == 'Loudoun County') & (COVID_summary['State'] == 'Virginia')])
print(COVID_summary.loc[(COVID_summary['County'] == 'Harlan County') & (COVID_summary['State'] == 'Kentucky')])
