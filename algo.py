import csv
import random as r

def randomizeGroups():
  aList=[]
  with open('./static/uploads/data.csv', 'r') as f:
      reader = csv.reader(f, skipinitialspace=False,delimiter=',', quoting=csv.QUOTE_NONE)
      for row in reader:
          aList.append(row)
  
  boys=[]
  girls=[]
  for i in aList:
    if i[2]=="Male":
      boys.append(i)
    elif i[2]=="Female":
      girls.append(i)
  r.shuffle(boys)
  r.shuffle(girls)
  groupA=[]
  groupB=[]
  c1=0
  c2=0
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
  with open('./static/uploads/data.csv', 'w+') as file:
    writer=csv.writer(file)
    writer.writerows(groupA)
    writer.writerows(groupB)
    file.close()

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