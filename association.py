
# coding: utf-8

# In[1]:

import Orange

file1=open("./data/STATEN ISLAND.txt", "r+")
raw_data = file1.readlines()

#for raw_data in lines:
#    print raw_data
# write data to the text file: data.basket
f = open('data.basket', 'w')
for item in raw_data:
#    print item
    f.write(item + '\n')
f.close()

# Load data from the text file: data.basket
data = Orange.data.Table("data.basket")


# Identify association rules with supports at least 0.3
rules = Orange.associate.AssociationRulesSparseInducer(data, support = 0.05)


# print out rules
print ("%4s %4s  %s" % ("Supp", "Conf", "Rule"))
for r in rules[:]:
    print ("%4.1f %4.1f  %s" % (r.support, r.confidence, r))

#rule = rules[0]
#for idx, d in enumerate(data):
##    print '\nUser {0}: {1}'.format(idx, raw_data[idx])
#    for r in rules:
#        if r.applies_left(d) and not r.applies_right(d):
#            print "%4.1f %4.1f  %s" % (r.support, r.confidence, r)

