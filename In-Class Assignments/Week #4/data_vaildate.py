import pandas as pd 

df = pd.read_csv('/u/aya9/cs410/data.csv')
c = df.head(10)
 
d = c.filter(regex = 'Record Type')

CrashesDF = df[df['Record Type'] == 1]
countc = CrashesDF.count()
VehiclesDF = df[df['Record Type'] == 2]
ParticipantsDF = df[df['Record Type'] == 3]


CrashesDF = CrashesDF.dropna(axis=1,how='all')
VehiclesDF = VehiclesDF.dropna(axis=1,how='all')
ParticipantsDF = ParticipantsDF.dropna(axis=1,how='all')

#1st assertion "Every crash has Urban Area code." - there are 508 crashes, which should be there 508 urban area code  
Urban_Area_code = CrashesDF['Urban Area Code']
count = Urban_Area_code.count()
if count == 508:
    print("Vaild")
else:
    print("Error: assertion violation")

#2nd assertion "Every crash ID has only 1 row of record types(1) no more than that."
id1 = CrashesDF["Crash ID"]
c1 = id1.count()
if c1 == 508:
    print("vaild")
else:
    print("Error: assertion violation")

#3rd assertion "Every crash has a unique crash ID." .. we could use the previous assertion as type1 would have only one crash Id
id2 = CrashesDF["Crash ID"]
c2 = id1.count()
if c2 == 508:
    print("vaild")
else:
    print("Error: assertion violation")

#4th assertion "Every crash type 3 had at least one person with Participant ID"
par = ParticipantsDF['Participant ID']
r3 = ParticipantsDF['Record Type']
c3 = par.count()
c4 = r3.count()

if c3 == c4 :
    print("Vaild")
else:
    print("Error: assertion violation")

#5th assertion "There were thousands of crashes but not millions"
id3 = CrashesDF["Crash ID"]
c5 = id1.count()

if c5 < 1000000 :
    print("Vaild")
else:
    print("Error: assertion violation")

#6th assertion "Most crashes happen in a rainy day" - Weather condition - Rainy day code = 3
we = CrashesDF["Weather Condition"]
rain = we.filter(regex = "3")
c6 = rain.count()

if c6 > 56:
    print("Vaild")
else:
    print("Error: assertion violation")

#7th assertion "Most crashes occur between two vehicles or more"
car = VehiclesDF["Record Type"]
c7= car.count()

if c7 > (508+(508/2)):
    print("Vaild")
else:
    print("Error: assertion violation")