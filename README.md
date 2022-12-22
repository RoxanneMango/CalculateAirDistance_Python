## Contents

- `calculate_air_distance.py` script to calculate the air distance between places.
- `places.csv` list of places in the following format: Name,Latitude,Longitude.

The Python script uses the Haversine formula to calculate the air distance between two places.

---

## Running the Python script

Run the script via the command line:
- Windows: `> calculate_air_distance.py`

- Linux: `$ python3 calculate_air_distance.py`

The python script is written for python 3.6.

The python script will automatically use the `places.csv` file when no additional arguments are given.
You can call the script with an argument to use a randomly generated list of (n) places instead of those listed in `places.csv`. Input must be a number and that number will be the number of randomly generated places that will be used.

Places in the `places.csv` file are saved in the format: Name,Latitude,Longitude, where each new place is written on a new line. Example:
`London,51.50853,-0.12574`. Keep this in mind when adding new places.
