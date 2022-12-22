import sys
import csv
import random
from math import sin, cos, sqrt, atan2, radians

# Calculate the air distance between two places using their latitudes and longitudes
# takes the latitude (lat1) and longitude (lon1) for the first place and the
# latitude (lat2) and longitude (lon2) for the second place
# returns the distance between the two places in kilometers (km)
def calculateAirDistance(lat1, lon1, lat2, lon2):
	R = 6373.0;				# declare constant: Circumference of the earth

	lat1 = radians(lat1);	# convert the latitudes and longitudes of
	lon1 = radians(lon1);	# the two places into radians so they can
	lat2 = radians(lat2);	# be plugged into the Haversine formula.
	lon2 = radians(lon2);	# ...

	dlon = lon2 - lon1;		# calculate difference between longitudes
	dlat = lat2 - lat1;		# calculate difference between latitudes

	a = sin(dlat / 2)**2 + cos(lat1) * cos(lat2) * sin(dlon / 2)**2;	# Haversine formula implementation
	c = 2 * atan2(sqrt(a), sqrt(1-a));									# ...
	distance = R*c;													# calculate distance
	return distance;												# return distance between the two places

# Recursive function that calculates the air distance between places
# takes a [name, latitude, longitude] list of places as function argument,
# and an empty [place A, place B, Distance] list that gets populated as the function calls itself recursively
# returns a [Place A, place B, Distance] list of distances between places
def calculateDistances(places, distances = []):
	if(len(places) == 0):											# if the list of places is empty
		distances = sorted(distances, key=lambda x: float(x[2]));	# Sort the list of distances
		distances.insert(0, ["Place A", "Place B", "Distance in"]);	# Insert the header to the distances list
		return distances;											# return distances
	if(len(distances) == 0):											# if list of distances is empty
		places.pop(0);													# pop the header off the list of places
		if(len(places) == 1):											# if list of places only contains one place ...
			distances.insert(0, ["Place A", "Place B", "Distance in"]);	# insert the header to the distances list
			distances.append([places[0][0], "--", "0"]);				# add the place with distance 0 to distances
			return distances;											# return distances
	p1 = places[0];																				# place1 = first place in list
	for p2 in places:																			# loop through all places ...
		if(p1[0] != p2[0]):																		# if place1 != place2 ...
			d = calculateAirDistance(float(p1[1]), float(p1[2]), float(p2[1]), float(p2[2]));	# calculate distance between
			distances.append([p1[0], p2[0], round(d, 1)]);										# add distance to distances
	return calculateDistances(places[1:], distances);		# recursively call itself again but remove one place from places

# Prints the average air distance between a list of paired places
# and prints the pair with the closest matching distance between each other
# takes a [name, latitude, longitude] list of places as function argument
# returns nothing
def printAverageDistance(places):
	if(len(places) <= 1):					# if list is empty or only contains a header ...
		print(f"List contains no places."); # print error message
		return;								# end return	
	average = 0;								# initialize average as 0
	for place in places[1:]:					# loop through all places
		average += float(place[2]);				# and add their distance to average
	if(average > 0):									# if average > 0 (prevent 0 division)
		average = average / (len(places)-1);			# calculate the average by dividing it with the number of places
		distance = abs(average - float(places[1][2]));	# Get the distance between the first pair of places in the list
		pair = places[1];								# Initialize pair with the first pair in the list of paired places
		for place in places[1:]:				# Loop through all place pairs (ignore header)
			d = abs(average - place[2]);		# Calculate how much each pair distance deviates from the average
			if(d < distance):					# if the deviation is less than that in the distance variable ...
				distance = d;					# assign the deviation as the new closest distance to the average
				pair = place;					# assign corresponding pair as the pair with the closest average distance
		print(f"Average distance: {round(average, 1)} km. Closest pair: {pair[0]} - {pair[1]} {pair[2]} km");
	else:
		print(f"Average distance: {round(average, 1)} km. Not enough places to make a pair.");

# Generate a random list of places
# takes number of places that need to be randomly generated as function argument
# returns a random [name, latitude, longitude] list of places
def constructPlaces(number : int):
	# List of name fragments to randomly generate a city name
	nameFragments = [
	"shi", "slarby", "fast", "knob", "le", "kle", "tje", 
	"je", "naa", "dør", "bly", "wo", "ma", "plez", "zio", 
	"gla", "yo", "que", "alber", "fi", "re", "ra", "to"
	];

	places = [];										# Define empty list of (to be) generated places
	places.append(["Name", "Latitude", "Longitude"]);	# Append the header to the list as the first element
	for n in range(number):					# For (number) of times ...
		townName = "";							# Start with empty name
		soundNum = random.randint(1, 3);		# Determine random number of name fragments ranging between 1 ~ 3
		for sounds in range(soundNum):											# For (n) number of name fragments ...
			townName += nameFragments[random.randint(0, len(nameFragments)-1)];	# Append random name fragment from list
		latitude = round(random.uniform(-90, 90), 5);					# Generate random latitude ranging between -90 ~ 90
		longitude = round(random.uniform(-180, 180), 5);				# Generate random longitude ranging between -180 ~ 180
		places.append([townName.capitalize(), latitude, longitude]); 	# Capitalize first letter of town name		
	return places;													# return list of randomly generated places
		
def printPlaces(placeList, unit = ""):
	line_count = 0;															# Start counting at 0
	print("+" + '-'*26 + "+" + '-'*26 + "+" + '-'*16 + "+");				# Print top of table
	for row in placeList:													# For each row in the list of places...
		print(f"| {row[0]:<25}| {row[1]:<25}| {str(row[2]) + unit :<15}|");	# Print the row in formatted columns
		if(line_count == 0):												# if it is the first row in the list ...
			print("+" + '-'*26 + "+" + '-'*26 + "+" + '-'*16 + "+");		# Print extra divider between header and contents
			line_count += 1;												# Increment line_count so its only done once
	print("+" + '-'*26 + "+" + '-'*26 + "+" + '-'*16 + "+");				# Print bottom of table

# main function
# takes argument vector from command line (argv) as function parameter
def main(argv):
	try:															# enter try-catch block
		places = None;												# declare places variable		
		if(len(argv) > 1):											# if a command line argument was given ...
			if(int(argv[1]) > 0):									# and argument is > 0
				places = (constructPlaces(int(argv[1])));			# places = list of (n) random number of places
			else:													# else ...
				raise Exception("input must be larger than zero");	# Raise exception
		else:														# if no command line argument was given ...
			file_name = "places.csv";								# define default places file
			csv_file = open(file_name, 'r', encoding='utf-8');		# Open places file
			places = list(csv.reader(csv_file, delimiter=','));		# places = csv reader as list object
			
		places = calculateDistances(places);	# calculate distance between places
		printPlaces(places, unit=" km");		# print distance between places
		printAverageDistance(places);			# calculate average distance and match it with place with closest match
	except Exception as e:					# If an exception occured ...
		print(f"An error occured: {e}");	# Print the exception
		return -1;							# and return with error code -1
	return 0;

main(sys.argv);		# call main function