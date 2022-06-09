import csv
import random as r

#Algorithm function for creating random groups
def randomizeGroups():
  aList=[]
  #Ridding of whitespace and converting csv to a list
  with open('./static/uploads/data.csv', 'r') as f:
      reader = csv.reader(f, skipinitialspace=False,delimiter=',', quoting=csv.QUOTE_NONE)
      for row in reader:
          aList.append(row)
  
  boys=[]
  girls=[]
  other=[]
  #More parsing
  for i in aList:
    if i[2]=="Male":
      boys.append(i)
    elif i[2]=="Female":
      girls.append(i)
    elif i[2]=="Other":
      other.append(i)
  r.shuffle(boys)
  r.shuffle(girls)
  r.shuffle(other)
  groupA=[]
  groupB=[]
  c1=0
  c2=0
  c3=0
  #Creating groups
  for i in boys:
    if i[3]=='A':
      if c1%2==0:
        groupA.append(i)
        i[3]='A'
      else:
        groupB.append(i)
        i[3]='B'
    else:
      if c1%2==0:
        groupA.append(i)
        i[3]='A'
      else:
        groupB.append(i)
        i[3]='B'
    c1+=1
  for i in girls:
    if i[3]=='A':
      if c2%2==0:
        groupA.append(i)
        i[3]='A'
      else:
        groupB.append(i)
        i[3]='B'
    else:
      if c2%2==0:
        groupA.append(i)
        i[3]='A'
      else:
        groupB.append(i)
        i[3]='B'
    c2+=1
  for i in other:
    if i[3]=='A':
      if c3%2==0:
        groupA.append(i)
        i[3]='A'
      else:
        groupB.append(i)
        i[3]='B'
    else:
      if c3%2==0:
        groupA.append(i)
        i[3]='A'
      else:
        groupB.append(i)
        i[3]='B'
    c3+=1
  #Rewriting csv with new groups
  with open('./static/uploads/data.csv', 'w+') as file:
    writer=csv.writer(file)
    writer.writerows(groupA)
    writer.writerows(groupB)
    file.close()

#Function that copies all data from the input csv to the data csv
def copyInitData():
  bList=[]
  with open('./static/uploads/initial input data.csv', 'r') as f:
      reader = csv.reader(f, skipinitialspace=False,delimiter=',', quoting=csv.QUOTE_NONE)
      for row in reader:
          bList.append(row)
  with open('./static/uploads/data.csv', 'w+') as file:
    writer=csv.writer(file)
    writer.writerows(bList)
    file.close()