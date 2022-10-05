import numpy as np

num_flights = 20
cost_coefficients = np.array(np.random.randint(1, 20, num_flights))
airlines_name_list = ["A", "B", "C"]
airlines_name = np.random.choice(airlines_name_list, num_flights)
slots = range(num_flights)
new_slot_times = np.array(np.arange(0, num_flights * 2, 2))
