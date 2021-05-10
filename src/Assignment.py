import random
from copy import deepcopy
import time
import os
import datetime
import calendar
import AssignmentClass


class Assignment:
    # a_class = None
    title = ""
    desc = ""
    time = ""
    due = ""
    completed = False
    # constructor
    def __init__(self, title, desc, time, due, a_class=AssignmentClass):
        self.a_class = a_class
        self.title = title
        self.desc = desc
        self.time = time
        self.due = due

    def __str__(self):
        return "%s : %s : %s : %s" % (self.due, self.a_class, self.title, self.desc)

    """def __str__(self):
        return "%s : %s : %s" % (self.due, self.a_class, self.title)"""

    def get_month(self):
        split_date = self.due.split("/")
        return split_date[0]

    def get_day(self):
        split_date = self.due.split("/")
        return split_date[1]

    def get_color(self):
        return self.a_class.get_color()

