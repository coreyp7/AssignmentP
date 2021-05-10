class AssignmentClass:
    name = ""
    color = ""
    time = ""
    # due is a list of the days the class is on
    due = ""

    def __init__(self, name, color, time, days_list):
        self.name = name
        self.color = color
        self.time = time
        self.due = days_list

    def change_color(self, color=str):
        self.color = color

    def change_name(self, name=str):
        self.name = name

    def __str__(self):
        return self.name

    def get_color(self):
        return self.color

