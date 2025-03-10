import csv
import random
from tkinter import *
from functools import partial  # To prevent unwanted windows


# helper functions go here

class StartGame:
    """"
    Initial Game interface (asks users how many rounds they would like to play)
     """

    def __init__(self):
        # self.play_box = Toplevel()

        self.start_frame = Frame(padx=10, pady=10)
        self.start_frame.grid()

        # Create play button..
        # self.play_button = Button(self.start_frame, font=("Arial", "16", "bold"),
        #                           fg="#FFFFFF", bg="#990000", text="Play", width="10",
        #                           command=self.check_rounds)
        # self.play_button.grid(row=0, column=1)

        # Strings for labels
        intro_string = "In each round you will be invited to choose a colour. Your goal i" \
                       "to beat the target score and win the round (and keep your points)."

        # choosing_string = "Oops - PLease choose a whole number more than zero."
        choose_string = "How many rounds do you want to play?"

        # List of labels to be made (text | font | fg)
        start_label_list = [
            ["Colour Quest", ("Arial", "16", "bold"), None],
            [intro_string, ("Arial", "12"), None],
            [choose_string, ("Arial", "12", "bold"), "#009900"]
        ]

        # create labels and add them to the reference list...

        start_label_ref = []
        for count, item in enumerate(start_label_list):
            make_label = Label(self.start_frame, text=item[0], font=item[1],
                               fg=item[2],
                               wraplength=350, justify="left", pady=10, padx=20)
            make_label.grid(row=count)

            start_label_ref.append(make_label)

        # extract choice label to that it can be changed to an
        # error message if necessary.
        self.choose_label = start_label_ref[2]

        # Frame so that entry box and button can be in the same row.
        self.entry_area_frame = Frame(self.start_frame)
        self.entry_area_frame.grid(row=3)

        self.num_rounds_entry = Entry(self.entry_area_frame, font=("Arial", "20", "bold"),
                                      width=10)
        self.num_rounds_entry.grid(row=0, column=0, padx=10, pady=10)

        # create play button...
        self.play_button = Button(self.entry_area_frame, font=("Arial", "16", "bold"),
                                  fg="#FFFFFF", bg="#0057D8", text="play", width=10,
                                  command=self.check_rounds)
        self.play_button.grid(row=0, column=1)

    def check_rounds(self):
        """
            Checks users have entered 1 or more rounds
        """

        # Retrieve temperature to be converted
        rounds_wanted = self.num_rounds_entry.get()

        # Reset label and entry box (for when users come back to home screen)
        self.choose_label.config(fg="#009900", font=("Arial", "12", "bold"))
        self.num_rounds_entry.config(bg="#FFFFFF")

        error = "Oops - Please choose a whole number more than zero."
        has_errors = "no"

        # checks that amount to be converted is a number above absolute zero
        try:
            rounds_wanted = int(rounds_wanted)
            if rounds_wanted > 0:
                # Invoke PLay Class (and take across number of rounds)
                Play(rounds_wanted)
                # Hide root window (ie: hide rounds choice window).
                root.withdraw()

            else:
                has_errors = "yes"

        except ValueError:
            has_errors = "yes"

        # display the error if necessary
        if has_errors == "yes":
            self.choose_label.config(text=error, fg="#990000", font=("Arial", "10", "bold"))
            self.num_rounds_entry.config(bg="#F4CCCC")
            self.num_rounds_entry.delete(0, END)


# Classes start here
class Play:
    """
    Interface for playing the Colour Quest Game
    """

    def __init__(self, how_many):
        self.rounds_won = IntVar()

        # Lists for stats component

        # Highest Score Test Data...
        # self.all_scores_list = [20, 20, 20, 16, 19]
        # self.all_high_scores_list = [20, 20, 20, 16, 19]
        # self.rounds_won.set(5)

        # Lowest Score Test Data...
        # self.all_scores_list = [0, 0, 0, 0, 0]
        # self.all_high_score_list = [20, 20, 20, 16, 19]
        # self.rounds_won.set(0)

        # Random Score Test Data...
        self.all_scores_list = [0, 15, 16, 0, 16]
        self.all_high_score_list = [20, 19, 18, 20, 20]
        self.rounds_won.set(3)

        self.play_box = Toplevel()

        self.game_frame = Frame(self.play_box)
        self.game_frame.grid(padx=10, pady=10)

        self.heading_label = Label(self.game_frame, font=("Arial", "14", "bold"),
                                   text="Stats", width=15, fg="#FFFFFF",
                                   bg="#FF8000", padx=10, pady=10, compound=self.to_stats)
        self.stats_button.grid(row=1)

    def to_stats(self):
        """
        Retrieves everything we need to display the game / round statistics
        """
        # IMPORTANT: retrieve number of rounds
        # won as a number (rather than the 'self' container)
        rounds_won = self.rounds_won.get()
        stats_bundle = [rounds_won, self.all_scores_list,
                        self.all_high_score_list]
        
        Stats(self, stats_bundle)

class Stats:
        """
        Display stats for Colour Quest Game
        """ 

        def __init__(self, partner, all_stats_info):
            
            # Extract information from master list...
            rounds_won = all_stats_info[0]
            user_scores = all_stats_info[1]
            high_scores = all_stats_info[2]

            # sort user scores to find high score...
            user_scores.sort()

            self.stats_box = Toplevel()

            # disable help button
            partner.stats_button.config(state=DISABLED)

            # If users press cross at top, closes help and
            # 'releases' help button
            self.stats_box.protocol('WM_DELETE_WINDOW',
                                    partial(self.close_stats, partner))
            
            self.stats_frame = Frame(self.stats_box, width=350)
            self.stats_frame.grid()

            # Math to populate stats dialogue...
            rounds_played = len(user_scores)

            success_rate = rounds_won / rounds_played * 100
            total_score = sum(user_scores)
            max_possible = sum(high_scores)

            best_score = user_scores[-1]
            average_score = total_score / rounds_played

            # Strings for stats labels...

            success_string = (f"Success Rate: {rounds_won} / {rounds_played}"
                              f" ({success_rate:.0f}%)")
            total_score_string = f"Total Score: {total_score}"
            max_possible_string = f"Maximum Possible Score: {max_possible}"
            best_score_string = f"Best Score: {best_score}"

            # custom comment text and formatting
            if total_score == max_possible:
                 comment_string = ("Amazing! You got the highest "
                                   "possible score!")
                 comment_colour = "#D5E8D4"

            elif total_score == 0:
                 comment_string = ("Oops - You've lost every round! "
                                   "You might want to look at the hints!")
                 comment_colour = "#F8CECC"
                 best_score_string = f"Best score: n/a"
            else:
                 comment_string = ""
                 comment_colour = "F0F0F0"

            average_score_string = f"Average Score: {average_score:.0f}\n"

            heading_font = ("Arial", "16", "bold")
            normal_font = ("Arial", "14")
            comment_font = ("Arial", "13")

            # Label list (text | font | 'Sticky')
            all_stats_strings = [
                 ["Statistics", heading_font, ""],
                 [success_string, normal_font, "w"],
                 [total_score_string,normal_font, "w"],
                 [max_possible_string,normal_font, "w"],
                 [comment_string, comment_font, "w"],
                 ["\nRound Stats", heading_font, ""],
                 [best_score_string, normal_font, "w"],
                 [average_score_string, normal_font, "w"]
            ]

            stats_label_ref_list = []
            for count, item in enumerate(all_stats_strings):
                 self.stats_label = Label(self.stats_frame, text=item[0], font=item[1]
                                          anchor="w", justify="left",
                                          padx=30, pady=5)
                 self.stats_label.grid(row=count, sticky=item[2], padx=10)
                 stats_label_ref_list.append(self.stats_label)

                 # Configure comment label background (for all won / all lost)
                 stats_comment_label = stats_label_ref_list[4]
                 stats_comment_label.config(bg=comment_colour)

                 self.dismiss_button.grid(row=8, padx=10, pady=10)

                 # closes help dialogue (used by button and x at top of dialogue)


    def close_stats(self, partner):
        # Put help button back to normal...
        partner.stats_button.config(state=NORMAL)
        self.stats_box.destroy()

# main routine
if __name__ == '__main__':
    root = Tk()
    root.title("Colour Quest")
    StartGame()
    root.mainloop()
