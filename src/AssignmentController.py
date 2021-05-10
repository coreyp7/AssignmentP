import sys
import AssignmentViewTk
import Assignment
import AssignmentList
from tkinter import Tk, Label, Button


class AssignmentController:
    # model = None
    # view = None

    def __init__(self, model=AssignmentList, view=AssignmentViewTk):
        self.model = model
        self.view = view

    def add_assignment(self, assignment=Assignment):
        self.model.add_assignment(assignment)

    def add_class(self, class_name=str, class_color=str, time_=str, days_list=list):
        self.model.add_class(class_name, class_color, time_, days_list)

    def get_this_week(self, limit=int):
        return self.model.get_next_week(self.model.get_formatted_date(), limit)

    def get_last_week(self, limit=int):
        return self.model.get_last_week(self.model.get_formatted_date(), limit)

    def get_rca(self):
        return self.model.get_recently_completed_assignments()

    def set_view(self, view=AssignmentViewTk):
        self.view = view

    def test_hello(self):
        print("Hello!")

    def edit_class_str(self, class_to_edit=str, name=str, color=str):
        self.model.edit_class_str(class_to_edit, name, color)

    def edit_class_str_2(
        self, class_to_edit=str, name=str, color=str, time=str, days_list=str
    ):
        self.model.edit_class_str_2(class_to_edit, name, color, time, days_list)

    def get_all_assignments(self):
        self.model.organize_incomplete_assignments()
        return self.model.incomplete_assignments

    def get_classes(self):
        return self.model.get_classes_list()

    def get_class_str(self, theclass=str):
        return self.model.get_class_str(theclass)

    def get_assignment_w_str(self, assignment=str):
        return self.model.get_assignment_w_str(assignment)

    def delete_assignment_str(self, assignment=str):
        self.model.remove_assignment_str(assignment)

    def delete_class_str(self, class_str=str):
        self.model.remove_class_str(class_str)

    def complete_assignment_str(self, assignment=str):
        self.model.complete_assignment_str(assignment)

    def change_main_display_options(self, future_limit=int, past_limit=int):
        self.model.set_limits(future_limit, past_limit)

    def get_main_display_future_limit(self):
        return self.model.get_future_limit()

    def get_main_display_past_limit(self):
        return self.model.get_past_limit()

    def get_theme(self):
        return self.model.theme

    def save_no_exit(self):
        self.model.save()
        self.view.save()

    def save_exit(self):
        self.model.save()
        self.view.save()
        self.view.master.quit
        sys.exit(0)


def main():
    model = AssignmentList.AssignmentList()
    root = Tk()
    controller = AssignmentController(model, None)
    view = AssignmentViewTk.AssignmentViewTk(root, controller)
    controller.set_view(view)
    root.mainloop()


if __name__ == "__main__":
    main()

