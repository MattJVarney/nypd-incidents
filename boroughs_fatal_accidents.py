'''
ICSI 531 - Data Mining
Amith Kumar Singh
'''
import csv
from time import strftime
from dateutil import parser
import matplotlib.pyplot as plt


def main():
    print('***** NYPD COLLISION *****')
    mylist = []
    accidents = {}
    x = []
    y = []
    with open("data/NYPD_Motor_Vehicle_Collisions.csv") as f:
        reader = csv.reader(f)
        firstline = True
        alcohol_night_ctr=0
        alcohol_normal_ctr=0
        ctr=0
        for row in reader:
            if firstline:  # skip first line
                firstline = False
                continue
            # normalizes the data
            # dt = parser.parse (row[0])   #parser pasrses the data in a default format and then we arrange it in required format before storing back in the col.
            # print dt.strftime ("%m")
            # row[0] = dt.strftime ('%Y-%m-%d')
            if row[10] and row[11] and row[12] and row[13] and row[14] and row[15] and row[16] and row[17]:
                count = int(row[10]) + int(row[11]) + int(row[12]) + int(row[13]) + int(row[14]) + int(row[15]) + int(row[16]) + int(row[17])
            else:
                continue
            if row[2] not in accidents:      # Getting total number of accidents for each borough from the entire dataset
                accidents[row[2]] = count
            else:
                accidents[row[2]] += count

            if row[1]:
                H,M = row[1].split(':')
                if 'Inattention' or 'Distraction' in row[18]:
                    ctr +=1
                if int(H)==(16 or 17 or 18 or 19 or 20) and 'Inattention' or 'Distraction' in row[18]:
                    alcohol_night_ctr +=1
                if int(H)!=(16 or 17 or 18 or 19 or 20) and 'Inattention' or 'Distraction' in row[18]:
                    alcohol_normal_ctr +=1


        print (alcohol_night_ctr)
        print (alcohol_normal_ctr)
        print (ctr)

        print (accidents)

        for k,v in accidents.items():
            mylist.append((k,v))
            x.append(k)
            y.append(v)
            # plt.plot(k,v,linestyle='-',marker='o')
        print (mylist)

        plt.bar(x, y, color = 'orange')
        plt.plot(x, y, linestyle = '-', marker = 'o')
        plt.xlabel("Boroughs")
        plt.ylabel("Accident Counts")
        plt.title("Boroughs - Total Accidents")
        plt.savefig("Boroughs_TotalAccidents.png")
        plt.show()


if __name__ == '__main__':
    main()