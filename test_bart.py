import bart
import json

my_dict = json.loads(bart.test_json)
station_data = bart.StationData(my_dict['root']['station'][0]['etd'])

estimates = station_data.get_by_colors_and_direction(colors=[bart.Colors.YELLOW], direction=bart.Direction.NORTH)
print(estimates)
