import csv
import random


def round_ans(val):
    """
    Rounds numbers to nearest integer
    :param val: number to be rounded
    :return: Rounded number (on integer)
    """

    var_rounded = (val * 2 + 1) // 2
    raw_rounded = "{:.0f}".format(var_rounded)
    return int(raw_rounded)


# Retrieve colours from csv file and put them in a list
file = open("00_colour_list_hex_v3.csv", "r")
all_colors = list(csv.reader(file, delimiter=","))
file.close()

# remove the first row
all_colors.pop(0)

round_colours = []
colours_scores = []

# loop until we have four colours with different scores
while len(round_colours) < 4:
    potential_colour = random.choice(all_colors)

    # Fet the score and check it's not a duplicate
    if potential_colour[1] not in colours_scores:
        round_colours.append(potential_colour)
        colours_scores.append(potential_colour[1])

print(round_colours)
print(colours_scores)

# find target score (median)

# change scores to integers
int_scores = [int(x) for x in colours_scores]
int_scores.sort()

medain = (int_scores[1] + int_scores[2]) / 2
medain = round_ans(medain)
print("Medain", medain)
