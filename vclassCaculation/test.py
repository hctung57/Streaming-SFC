import csv

# example data in array format
data = [1.4]

# open a CSV file in write mode
with open('output.csv', 'w', newline='') as file:
    writer = csv.writer(file)
    
    # write each row from the data array to the CSV file
    writer.writerow(data)