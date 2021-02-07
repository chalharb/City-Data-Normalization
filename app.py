import csv
import os

#################################
# Read the CSV
def read_csv(file):
    dict_list = []

    with open(file, newline='\n') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            dict_list.append(row)

    return dict_list

#################################
# Write the CSV
def write_csv(file, header_keys, data_list):
    with open(file, 'w', newline='') as csvfile:
        fieldnames = header_keys
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)

        writer.writeheader()
        for item in data_list:
            writer.writerow(item)


#################################
# Current Working Directory
cwd = os.path.dirname(__file__)

#################################
# Input Files
data_input_folder = os.path.join(cwd, './data/in')
state_input = os.path.join(data_input_folder, './state_import.csv')
county_input = os.path.join(data_input_folder, './tn_county_initial.csv')
city_input = os.path.join(data_input_folder, './tn_city_initial.csv')

#################################
# Output Files
data_output_folder = os.path.join(cwd, './data/out')
state_output = os.path.join(data_output_folder, './all_states_import.csv')
county_output = os.path.join(data_output_folder, './tn_county_import.csv')
city_output = os.path.join(data_output_folder, './tn_city_import.csv')
zipcode_output = os.path.join(data_output_folder, './tn_zipcode_import.csv')

#################################
# store unique zipcode array so we can build a dictionary list
unique_zipcode_array = []

#################################
# Set our lists
state_list = read_csv(state_input)
county_list = read_csv(county_input)
city_list = read_csv(city_input)
zipcode_list = []

#################################
# Generate array of zipcodes
for row in city_list:
    if int(row['zipcode']) not in unique_zipcode_array:
        unique_zipcode_array.append(int(row['zipcode']))

#################################
# Generate a dict list for zipcodes
unique_zipcode_array.sort()
for idx, zipcode in enumerate(unique_zipcode_array):
    obj = {
        'id': idx + 1,
        'code': zipcode
    }

    zipcode_list.append(obj)

#################################
# loop through county list and change state to state id
for county_row in county_list:
    state_id = int(next(state['id'] for state in state_list if state['code'].lower(
    ) == county_row['state'].lower()))
    county_row['state'] = state_id

#################################
# loop through city list and exchange county, state, and zipcode with their respective IDs
for city_row in city_list:
    state_id = int(next(state['id'] for state in state_list if state['code'].lower() == city_row['state'].lower()))
    county_id = int(next(county['id'] for county in county_list if county['name'].lower() == city_row['county'].lower()))
    zipcode_id = int(next(zipcode['id'] for zipcode in zipcode_list if int(zipcode['code']) == int(city_row['zipcode'])))

    city_row['id'] = int(city_row['id'])
    city_row['state'] = state_id
    city_row['zipcode'] = zipcode_id
    city_row['county'] = county_id


#################################
# Copy over our states file
print('Creating States import file...')
write_csv(state_output, ['id', 'name', 'abbr', 'code'], state_list)

#################################
# Create our zipcode import file
print('Creating Zip Codes import file...')
write_csv(zipcode_output, ['id', 'code'], zipcode_list)

#################################
# Copy over our county file
print('Creating County import file...')
write_csv(county_output, ['id', 'name', 'state'], county_list)

#################################
# Create our city import file
print('Creating Cities import file...')
write_csv(city_output, ['id', 'city', 'zipcode', 'county', 'state'], city_list)
