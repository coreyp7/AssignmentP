import random
from copy import deepcopy
import time
import calendar
import os
import datetime
import calendar
import pickle
import Assignment
import AssignmentClass


class AssignmentList:
    incomplete_assignments = []
    # completed_assignments = []
    classes = []
    future_limit = None
    past_limit = None
    theme = ""

    def __init__(self):
        try:
            self.load()
        except:
            print("file is empty.")

        if self.future_limit is None:
            self.future_limit = 7
        if self.past_limit is None:
            self.past_limit = 2

        self.clear_old_assignments()

    # Will clear any assignments over a month old.
    def clear_old_assignments(self):
        date = self.get_formatted_date()
        date_list = date.split("/")
        value = int(f"{date_list[2]}{date_list[0]}{date_list[1]}")
        for assignment in self.incomplete_assignments:
            current_date_list = assignment.due.split("/")
            current_value = ""

            if int(current_date_list[0]) < 10:
                current_value = f"{current_date_list[2]}0{current_date_list[0]}"
            else:
                current_value = f"{current_date_list[2]}{current_date_list[0]}"

            if int(current_date_list[1]) < 10:
                current_value += f"0{current_date_list[1]}"
            else:
                current_value += f"{current_date_list[1]}"

            if (int(current_value) + 100) < value:
                self.remove_assignment(assignment)

    # !!!
    # This method is a fucking mess, please don't look at it.
    # !!!
    def organize_incomplete_assignments(self):
        arr = self.incomplete_assignments
        n = len(arr)
        # Traverse through all array elements
        for i in range(n):

            # Last i elements are already in place
            for j in range(0, n - i - 1):

                # traverse the array from 0 to n-i-1
                # Swap if the element found is greater
                # than the next element
                timej1 = arr[j].due.split("/")
                if int(timej1[0]) < 10:
                    timej15 = f"{timej1[2]}0{timej1[0]}"
                else:
                    timej15 = f"{timej1[2]}{timej1[0]}"

                if int(timej1[1]) < 10:
                    timej15 += f"0{timej1[1]}"
                else:
                    timej15 += f"{timej1[1]}"
                # timej2 = timej15.split[":"]
                # timej3 = str(timej2[0]) + str(timej2[1])

                timejj1 = arr[j + 1].due.split("/")
                if int(timejj1[0]) < 10:
                    timejj15 = f"{timejj1[2]}0{timejj1[0]}"
                else:
                    timejj15 = f"{timejj1[2]}{timejj1[0]}"

                if int(timejj1[1]) < 10:
                    timejj15 += f"0{timejj1[1]}"
                else:
                    timejj15 += f"{timejj1[1]}"
                # timejj15 = f"{timejj1[0]}{timejj1[1]}{timejj1[2]}"
                # timejj2 = timejj1.split[":"]
                # timejj3 = str(timejj2[0]) + str(timejj2[1])

                if int(timej15) > int(timejj15):
                    arr[j], arr[j + 1] = arr[j + 1], arr[j]

        self.incomplete_assignments = arr

    def get_past_limit(self):
        if self.past_limit is not None:
            return self.past_limit
        return 6

    def get_future_limit(self):
        if self.future_limit is not None:
            return self.future_limit
        return 6

    def set_past_limit(self, limit=int):
        self.past_limit = limit

    def set_future_limit(self, limit=int):
        self.future_limit = limit

    def set_limits(self, future=int, past=int):
        self.past_limit = past
        self.future_limit = future

    def add_assignment(self, new_assignment=Assignment):
        self.incomplete_assignments.append(new_assignment)

    def remove_assignment(self, deleted_assignment=Assignment):
        for assignment in self.incomplete_assignments:
            if assignment == deleted_assignment:
                self.incomplete_assignments.remove(assignment)

    # NOW returns all assignments and classes on said date
    # IF THERE ARE NO ASSIGNMENTS BUT CLASSES,
    # THE FIRST ELEMENT IS THE DATE STR.
    def get_assignments_by_date(self, date=str):
        assignments_today = []
        for assignment in self.incomplete_assignments:
            if assignment.due == date:
                assignments_today.append(assignment)

        day_formatted = date.split("/")
        day_formatted_final = (
            f"{day_formatted[1]} {day_formatted[0]} 20{day_formatted[2]}"
        )
        day_name = self.find_day(day_formatted_final)
        if not assignments_today:
            assignments_today.append(date)

        for each_class in self.classes:
            for day in each_class.due:
                if str(day) == str(day_name):
                    assignments_today.append(each_class)
                    print(f"added {each_class} on {day} {date}")
                    print(str(type(each_class)))
        return assignments_today

    def find_day(self, date):
        born = datetime.datetime.strptime(date, "%d %m %Y").weekday()
        return calendar.day_name[born]

    def get_rc_assignments_by_date(self, date=str):
        assignments_today = []
        for assignment in self.incomplete_assignments:
            if assignment.due == date:
                assignments_today.append(assignment)
        return assignments_today

    def get_next_week(self, date=str, limit=int):
        limit = self.future_limit + 1
        date_split = date.split("/")
        day = int(date_split[1])
        month = int(date_split[0])
        year = int(date_split[2])
        days_in_month = self.switch_month(month)
        days_remaining_this_month = days_in_month - day
        all_assignments = []
        # This is odd because of some rollover that can occur which was
        # skipping the final day of the month. The reason for this seems
        # ultimately due to the fact that the limit set is including the
        # given day. (If your limit is 1, it prints only the date given).
        if (day + limit - 1) <= days_in_month:
            # perform normally without any nonsense.
            for i in range(day, day + limit):
                all_assignments.append(
                    self.get_assignments_by_date(f"{month}/{i}/{year}")
                )
        else:
            if day - days_in_month == 0:
                all_assignments.append(
                    self.get_assignments_by_date(f"{month}/{day}/{year}")
                )

            for i in range(day, days_in_month + 1):
                all_assignments.append(
                    self.get_assignments_by_date(f"{month}/{i}/{year}")
                )
            # add days up until next month here
            days_next_month = limit - days_remaining_this_month
            next_month = month + 1
            for i in range(1, days_next_month):
                all_assignments.append(
                    self.get_assignments_by_date(f"{next_month}/{i}/{year}")
                )
        all_assignments_sorted = []
        for day in all_assignments:
            all_assignments_sorted.append(self.organize_day_by_time(day))
        return all_assignments_sorted

    def get_next_week_and_classes(self, date=str, limit=int):
        limit = self.future_limit + 1
        date_split = date.split("/")
        day = int(date_split[1])
        month = int(date_split[0])
        year = int(date_split[2])
        days_in_month = self.switch_month(month)
        days_remaining_this_month = days_in_month - day
        all_assignments = []
        # This is odd because of some rollover that can occur which was
        # skipping the final day of the month. The reason for this seems
        # ultimately due to the fact that the limit set is including the
        # given day. (If your limit is 1, it prints only the date given).
        if (day + limit - 1) <= days_in_month:
            # perform normally without any nonsense.
            for i in range(day, day + limit):
                all_assignments.append(
                    self.get_assignments_by_date(f"{month}/{i}/{year}")
                )
        else:
            for i in range(day, days_in_month):
                all_assignments.append(
                    self.get_assignments_by_date(f"{month}/{i}/{year}")
                )
            # add days up until next month here
            days_next_month = limit - days_remaining_this_month
            next_month = month + 1
            for i in range(1, days_next_month):
                all_assignments.append(
                    self.get_assignments_by_date(f"{next_month}/{i}/{year}")
                )
        ###

        ###
        all_assignments_sorted = []
        for day in all_assignments:
            all_assignments_sorted.append(self.organize_day_by_time(day))

        return all_assignments_sorted

    # THIS METHOD SHOULDN"T RETURN THE DATE YOU GIVE IT!!!!
    def get_last_week(self, date=str, limit=int):
        limit = self.past_limit
        date_split = date.split("/")
        day = int(date_split[1])
        month = int(date_split[0])
        year = int(date_split[2])
        if month == 1:
            days_in_last_month = self.switch_month(12)
        else:
            days_in_last_month = self.switch_month(month - 1)

        all_assignments = []
        if (day - limit - 1) > 0:
            # perform normally without any nonsense.
            for i in range(day - limit, day):
                all_assignments.append(
                    self.get_rc_assignments_by_date(f"{month}/{i}/{year}")
                )
        else:
            # handle weird stuff here.
            for i in range(1, day):
                all_assignments.append(
                    self.get_rc_assignments_by_date(f"{month}/{i}/{year}")
                )
            days_to_display_last_month = limit - day
            for i in range(days_in_last_month - (limit - day), days_in_last_month):
                all_assignments.append(
                    self.get_rc_assignments_by_date(f"{month-1}/{i}/{year}")
                )
        all_assignments_sorted = []
        for day in all_assignments:
            all_assignments_sorted.append(self.organize_day_by_time(day))
        return all_assignments_sorted

    def organize_day_by_time(self, assignments):
        am_list = []
        pm_list = []
        date = ""

        if not assignments:
            return assignments

        if str(type(assignments[0])) == "<class 'str'>":
            date = assignments.pop(0)

        for assignment in assignments:
            print(str(type(assignment)))
            if assignment.time.split(" ")[1] == "am":
                print(f"{assignment} added to am")
                am_list.append(assignment)
            else:
                print(f"{assignment} added to pm")
                pm_list.append(assignment)

        before_ten_am_list = []
        after_ten_am_list = []
        before_ten_pm_list = []
        after_ten_pm_list = []

        for i in am_list:
            if int(i.time.split(" ")[0].split(":")[0]) < 10:
                print(f"{int(i.time.split(':')[0])} <= 10")
                print(f"{i.time} added to before 10am")
                before_ten_am_list.append(i)
            else:
                print(int(i.time.split(" ")[0].split(":")[0]))
                print(f"{i.time} added to after 10am")
                after_ten_am_list.append(i)

        for i in pm_list:
            if int(i.time.split(" ")[0].split(":")[0]) < 10:
                before_ten_pm_list.append(i)
            else:
                after_ten_pm_list.append(i)

        for i in after_ten_pm_list:
            if int(i.time.split(":")[0]) == 12:
                after_ten_am_list.insert(
                    len(before_ten_am_list),
                    after_ten_pm_list.pop(after_ten_pm_list.index(i)),
                )

        # both_lists = [am_list, pm_list]
        both_lists = [
            before_ten_am_list,
            after_ten_am_list,
            before_ten_pm_list,
            after_ten_pm_list,
        ]
        sorted_list = []

        # return am_list
        for current in both_lists:
            arr = current
            n = len(arr)
            # Traverse through all array elements
            for i in range(n):

                # Last i elements are already in place
                for j in range(0, n - i - 1):

                    # traverse the array from 0 to n-i-1
                    # Swap if the element found is greater
                    # than the next element
                    timej1 = arr[j].time.split(" ")[0]
                    # timej2 = timej15.split[":"]
                    # timej3 = str(timej2[0]) + str(timej2[1])
                    timej12 = timej1.split(":")[0]
                    # timej13 = int(f"{str(timej12[0])}{str(timej12[1])}")

                    timejj1 = arr[j + 1].time.split(" ")[0]
                    # timejj2 = timejj1.split[":"]
                    # timejj3 = str(timejj2[0]) + str(timejj2[1])
                    timejj12 = timejj1.split(":")[0]
                    # timejj13 = int(f"{str(timejj12[0])}{str(timejj12[1])}")

                    if timej12 > timejj12:
                        print(f"SWITCHING {timej12}  {timejj12}")
                        arr[j], arr[j + 1] = arr[j + 1], arr[j]
            sorted_list += arr
            for i in arr:
                print(i)

        if date != "":
            sorted_list.insert(0, date)

        print(f"THE SORTED LIST IS : {sorted_list}")
        return sorted_list

    def switch_month(self, month=int):
        month_switcher = {
            1: 31,
            2: 28,
            3: 31,
            4: 30,
            5: 31,
            6: 30,
            7: 31,
            8: 31,
            9: 30,
            10: 31,
            11: 30,
            12: 31,
        }
        return month_switcher.get(month, -1)

    """I think this will be needed at one point.
    
    8/14/20: it was finally needed"""

    def refresh_rca(self):
        date = self.get_formatted_date()
        date_day = date[1]

    def get_formatted_date(self):
        date = datetime.datetime.now().date().strftime("%m/%d/%Y")
        date_string_final = date[0:6] + date[8:]
        return date_string_final

    def add_class(self, class_name=str, class_color=str, time=str, days_list=list):
        self.classes.append(
            AssignmentClass.AssignmentClass(class_name, class_color, time, days_list)
        )

    def remove_class(self, a_class=AssignmentClass):
        self.classes.remove(a_class)

    def clear_all_classes(self):
        self.classes = []

    def get_classes_list(self):
        return self.classes

    def get_class_str(self, classname=str):
        for i in self.classes:
            if i.name == classname:
                return i

    def get_assignment_w_str(self, assignment_str=str):
        for assignment in self.incomplete_assignments:
            if str(assignment) == assignment_str:
                return assignment

    def remove_assignment_str(self, del_assignment=str):
        for assignment in self.incomplete_assignments:
            if str(assignment) == del_assignment:
                self.incomplete_assignments.remove(assignment)

    def complete_assignment_str(self, completed_assignment=str):
        assignment = self.get_assignment_w_str(completed_assignment)
        self.incomplete_assignments[
            self.incomplete_assignments.index(assignment)
        ].completed = True

    def remove_class_str(self, class_str=str):
        self.remove_class(self.get_class_str(class_str))

    def edit_class_str(self, class_to_edit=str, name=str, color=str):
        for index, each_class in enumerate(self.classes):
            if str(each_class) == str(class_to_edit):
                self.classes[index].name = name
                self.classes[index].color = color

    def edit_class_str_2(
        self, class_to_edit=str, name=str, color=str, time=str, days_list=str
    ):
        for index, each_class in enumerate(self.classes):
            if str(each_class) == str(class_to_edit):
                self.classes[index].name = name
                self.classes[index].color = color
                self.classes[index].time = time
                self.classes[index].due = days_list

    def save(self):
        final_dump = [
            self.incomplete_assignments,
            # self.completed_assignments,
            self.classes,
            self.future_limit,
            self.past_limit,
            self.theme,
        ]
        pickle_file = open("model.txt", "wb")
        pickle_file.truncate(0)
        pickle.dump(final_dump, pickle_file)

    def load(self):
        all_lists = pickle.load(open("model.txt", "rb"))
        self.incomplete_assignments = all_lists[0]
        # self.completed_assignments = all_lists[1]
        self.classes = all_lists[1]
        self.future_limit = all_lists[2]
        self.past_limit = all_lists[3]
        self.theme = all_lists[4]

