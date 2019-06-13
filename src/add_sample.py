import csv

"""
This function is used to ADD USER INPUT for a used car to make single price prediction in `prediction.py`
Input:
	user_input (:obj: list): a list of sample car features
Output:
	'sample_usedCar.csv': a csv file in 'data' folder containing the sample car data
							and will be taken into `prediction.py` for price prediction
"""

"""
8 entries required from user:

	index=0: `yearOfRegistration`, please enter a year >= 1999
				integer

	index=1: `powerPS`, horse power of the car
				integer

	index=2: `kilometer`, how many kilometers the car has driven
				integer
				if use 'miles', kilometer = 1.6 * miles
				for the webapp, input will be in miles, transform done automatically

	index=3: `brand_featrue`, the brand of your car, encoded in number labels here
				for the webapp, input will be text in drop-down menu

				0: alfa_romeo, 1: audi, 2: bmw, 3: chevrolet, 4: chryster, 5: citroen,
				6: dacia, 7: daewoo, 8: daihatsu, 9: fiat, 10: ford
				11: honda 12: hyundai, 13: jaguar, 14: jeep, 15: kia,
				16: lada, 17: lancia, 18: land_rover, 19: mazda, 20: mercedes_benz
				21: mini, 22: mitsubishi, 23: nissan, 24: opel, 25: peugeot
				26: porsche, 27: renault, 28: rover, 29: saab, 30: seat,
				31: skoda, 32: smart, 33: subaru, 34: suzuki, 35: toyota,
				36: volkswagen, 37: volvo

	index=4: `gearbox_feature`, the gearbox type of your car, encoded in number labels here
				for the webapp, input will be text in drop-down menu

				0: automatic, 1: manual

	index=5: `damageExist_feature`, if unrepaired damage exists on your car, encoded in number labels here
				for the webapp, input will be text in drop-down menu

				0: No damage exists, 1: Damage exist

	index=6: `fuelType_feature`, the fuel type of your car, encoded in number labels here
				for the webapp, input will be text in drop-down menu

				0: other, 1: gasoline, 2: cng, 3: diesel, 4: electric, 5: hybrid, 6: lpg

	index=7: `vehicleType_feature`: the vehicle type (shape) of your car, encoded in number labels here
				for the webapp, input will be text in drop-down menu

				0: other, 1: bus, 2: cabrio, 3: coupe, 4: sedan, 5: station wagon, 6: limousine


"""
user_input = [2015, 177, 10500, 14, 0, 0, 4, 7]

with open('data/sample_usedCar.csv', mode='w+') as sample:
    sample_writer = csv.writer(sample, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
    sample_writer.writerow(['yearOfRegistration', 'powerPS', 'kilometer', 'brand_feature',
          'gearbox_feature', 'damageExist_feature', 'fuelType_feature',
          'vehicleType_feature'])
    sample_writer.writerow(user_input)
