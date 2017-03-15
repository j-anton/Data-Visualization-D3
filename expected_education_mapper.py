import pandas
import numpy

#Determines expected level of education attained for a particular occupation
def expected_education(x,highest_educations_attained):
    sum = 0
    total = numpy.sum(x[1:])
    for i in xrange(0,len(x)-1):
        sum += i * x[highest_educations_attained[i]]
    expected_value = sum/total
    return highest_educations_attained[int(numpy.round(expected_value))]

#----------------------------------------------------------------------------------------------------------------------#

#Import csv
education_data = pandas.read_csv("data/education_attained_by_occupation.csv")

#Clean data
highest_educations_attained = education_data.columns.values[-5:]
education_data = education_data[numpy.hstack(([' '],highest_educations_attained))][1:481]

#Calculate expected highest level of education completed for each occupation
education_data['Expected Highest Education Level Completed'] = \
    education_data.apply(lambda x: expected_education(x,highest_educations_attained), axis = 1)

#Output to csv
education_data = education_data[[' ','Expected Highest Education Level Completed']]
education_data.columns = ['Occupation','Expected Highest Education Level Completed']
education_data.to_csv("data/expected_education_attained_by_occupation.csv")