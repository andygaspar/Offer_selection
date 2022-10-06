import numpy as np

num_flights = 15
interval = 5
interval_modifier = 2
cost_coefficients = np.array(np.random.randint(1, 20, num_flights))
airlines_name_list = ["A", "B", "C"]
airlines_name = np.random.choice(airlines_name_list, num_flights)
indexes = range(num_flights)
slots = np.array([interval * index for index in indexes])
new_slot_times = np.array([interval_modifier * slot for slot in slots])
