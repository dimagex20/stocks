import numpy as np
import matplotlib.pyplot as plt
from scipy.datasets import electrocardiogram
from scipy.signal import find_peaks

import pprint
import csv



def get_csv_data():
    numbers_list = []

    csv_file_path = '/Users/ggale/Desktop/code/verizon/stocks/verizon/data/NHL_AmalieArena_FL_20240111.csv'
    with open(csv_file_path, 'r') as csv_file:
        # Create a CSV reader
        csv_reader = csv.reader(csv_file)

        # Iterate through each row in the CSV file
        for idx, row in enumerate(csv_reader):
            if idx == 0:
                continue

            print(row[1])
            numbers_list.append(row[1])

    return numbers_list

y = get_csv_data()
print(y)



# x = electrocardiogram()[2000:4000]


print(type(y))

pprint.pprint(y)

x = [idx for idx, i in enumerate(y)]
y_ints = [int(i) for idx, i in enumerate(y)]
y_array = np.array(y)

peaks, properties = find_peaks(y_array, prominence=10000, width=1)

print("x: ", x)
print("y: ", y)
print("y_array: ", y_array)
print("peaks: ", peaks)
print("properties: ", properties)


properties["prominences"], properties["widths"]

plt.plot(x, y_ints)
plt.plot(peaks, y_array[peaks], "x")
# plt.vlines(x=peaks, ymin=x[peaks] - properties["prominences"],
#            ymax = x[peaks], color = "C1")
# plt.hlines(y=properties["width_heights"], xmin=properties["left_ips"],
#            xmax=properties["right_ips"], color = "C1")
# x = [1, 2, 3, 4, 5, 6, 7]
# y = [2, 4, 6, 8, 10, 5, 2]

# Plot the line chart
# plt.plot(x, y)

# # Add labels and title
plt.xlabel('X-axis')
plt.ylabel('Y-axis')
plt.title('Simple Line Chart')

# Show the plot
plt.show()