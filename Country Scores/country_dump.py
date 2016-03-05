''' Code to dump Country names and Nationality'''

from csv import DictReader, DictWriter
import cPickle as pickle, string

country_dict = {}
transtab = string.maketrans("", "")

countries_csv = DictReader(open("countries2.csv",'rU'))


# Updates dictionary with Country and Nationality
for ii in countries_csv:
	country_name = ii['Country'].lower().split(",")
	nationality = ii['Adjective'].lower().split(",")
	country_dict.update({tuple(country_name) : country_name + nationality})


with open("countries_dump.txt", 'a') as tgd:
    pickle.dump(country_dict, tgd)
tgd.close()


