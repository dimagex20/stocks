import random

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

class FindPeak:
    def __init__(self, drop_pct, numbers):
        self.numbers = numbers
        self.drop_pct = drop_pct
        self._find_high()
        self._find_left_limit()
        self._find_right_limit()


    def _find_high(self):
        self.max_number = max(self.numbers)
        self.drop_limt = self.max_number * self.drop_pct
        self.max_index = self.numbers.index(self.max_number)
        print(self.max_number, self.max_index)

    def _find_left_limit(self):
        curr_index = self.max_index
        self.left_bound_index = 0

        while curr_index >= 0:
            print(curr_index, self.drop_limt, self.numbers[curr_index - 1])
            if curr_index == 0:
                return

            if self.numbers[curr_index - 1] < self.drop_limt:
                self.left_bound_index = curr_index - 1
                return

            curr_index -= 1

    def _find_right_limit(self):
        curr_index = self.max_index
        right_bound_cap = len(self.numbers) - 1
        self.right_bound_index = len(self.numbers) - 1

        while curr_index <= right_bound_cap:
            if curr_index == right_bound_cap:
                return

            print(curr_index, self.drop_limt, self.numbers[curr_index + 1])

            if self.numbers[curr_index + 1] < self.drop_limt:
                self.right_bound_index = curr_index + 1 
                return

            curr_index += 1 

    def print_peak_range(self):
        range_txt = "{} - {}".format(self.left_bound_index, self.right_bound_index)
        print("the range of the peak is " + range_txt)


if __name__ == "__main__":

    # Generate random time series data
    numbers = [45, 144, 145, 143, 137, 55, 132, 132, 135, 132, 132, 130, 126, 130, 130, 125, 126, 125, 130, 130, 131, 133, 133, 135, 136, 135, 135, 138, 141, 143, 142, 144, 146, 143, 144, 145, 151, 155, 152, 155, 152, 151, 151, 154, 153, 155, 154, 153, 148, 149, 149, 147, 148, 147, 145, 146, 151, 154, 152, 153, 151, 149, 150, 153, 153, 156, 155, 157, 159, 158, 159, 160, 158, 158, 161, 162, 165, 166, 166, 164, 165, 162, 161, 160, 166, 165, 165, 166, 168, 167, 165, 165, 164, 164, 168, 170, 170, 169, 167, 166, 174, 174, 172, 174, 174, 173, 172, 172, 173, 175, 175, 174, 172, 172, 173, 175, 177, 177, 180, 181, 180, 179, 178, 181, 181, 184, 183, 184, 186, 185, 185, 184, 187, 187, 185, 188, 189, 190, 194, 192, 191, 192, 191, 189, 188, 190, 191, 191, 194, 194, 195, 193, 192, 193, 194, 195, 193, 196, 196, 196, 193, 191, 182, 179, 180, 178, 178, 178, 179, 177, 177, 174, 174, 176, 177, 181, 176, 179, 180, 184, 188, 188, 189, 190, 183, 178, 178, 179, 176, 174, 176, 175, 178, 179, 175, 174, 175, 176, 172, 170, 171, 171, 174, 172, 174, 175, 177, 179, 180, 181, 179, 179, 177, 176, 175, 173, 173, 173, 171, 167, 168, 170, 50, 174, 178, 177, 179, 182, 183, 182, 186, 185]


    plt.plot(numbers, label='Numbers')
    plt.xlabel('Index')
    plt.ylabel('Values')
    plt.title('Plot of Numbers')
    plt.legend()  # Show legend if labels are provided

    # Show the grid
    plt.grid(True)

    # Show the plot
    plt.show()



    fp = FindPeak(.5, numbers)
    fp.print_peak_range()

