import csv
with open('Attendance.csv') as csvfile:
    reader=csv.reader(x.replace('\0', '') for x in csvfile)
    count=0
    newList=[]

    for row in reader:
        count=count+1
        print(row)
        newList.append(row)
    totalList=len(newList)
    print(totalList)