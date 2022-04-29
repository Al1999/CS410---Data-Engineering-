import pandas as pd
import re as r

data = pd.read_csv('books.csv')


d = data.drop(columns = ['Edition Statement', 'Corporate Author', 'Corporate Contributors', 'Former owner', 'Engraver', 'Issuance type', 'Shelfmarks'])

#df2  = pd.read_csv('books.csv', usecolm = ['Edition Statement', 'Corporate Author', 'Corporate Contributors', 'Former owner', 'Engraver', 'Issuance type', 'Shelfmarks'])

#print(d.head(5))

data1 = d['Date of Publication']
#rw  = data1.head(10)


#d1 = data1.str.strip(']')
#d2 = d.str.strip(']')
#print (d1 )

# Part B
regex = r'^(\d{4})' 
extr = d['Date of Publication'].str.extract(r'^(\d{4})', expand=False)

d['Date of Publication'] = pd.to_numeric(extr)
d['Date of Publication'].dtype

d['Date of Publication'].isnull().sum() / len(d)

print(d['Date of Publication'])

"""for r in data1 :
    f =  isinstance(r, str)
    if f:
        x = re.search("]$", r )
        if x:
            print(r)"""

#Part - C
uni_t = [] 

with open('uniplaces.txt') as file:
    for l in file:
        if '[edit]' in l:
            state = l
        else:
            uni_t.append((state, l))

uni_df1 = pd.DataFrame(uni_t, columns=['State', 'City'])
uni_df2 = pd.DataFrame(columns=['University'])
#print(uni_df1)

def state_city(data):
    if' (' in data:
        return data[:data.find(' (')]
    elif('[') in data:
        return data[:data.find('[')]
    else:
        return data


def univ(data):
    if ' (' in data:
        return data[data.find(' ('):]

uni_df3 = uni_df1.applymap(state_city)
uni_df2 = uni_df1.applymap(univ)
uni_df3['University'] = uni_df2['City']
regex2 = r'^([a-zA-Z\s])'
uni = uni_df3['University']
uni= uni.astype('string')

uni = uni_df3['University'].str.replace(r"[^a-zA-Z ]+"," ").str.strip()
uni_df3['University'] = uni

print(uni_df3)

