import Assignment
import AssignmentController
from tkinter import (
    Tk,
    Label,
    Button,
    ttk,
    Toplevel,
    Entry,
    Menu,
    font,
    Radiobutton,
    Scrollbar,
    Listbox,
    Checkbutton,
)
import tkinter
import random
import pickle
import datetime
import calendar


class AssignmentViewTk:
    controller = None

    theme = ""
    text_color = ""
    background_color = ""
    class_text_color = ""
    main_display_date_font = ""
    main_display_assignment_font = ""
    class_display_check = True

    version = "10/14/20"

    def __init__(self, master, controller=AssignmentController):
        try:
            self.load()
        except:
            pass

        if self.theme == "":
            self.set_light_theme()

        if self.main_display_assignment_font == "":
            self.main_display_assignment_font = "14"

        if self.main_display_date_font == "":
            self.main_display_date_font = "24"

        self.master = master
        master.title(self.version)
        self.controller = controller

        self.master.geometry("650x650")

        self.refresh_main()

    def set_controller(self, controller=AssignmentController):
        self.controller = controller

    def edit_classes_window(self):
        win = Toplevel()
        win.configure(background=self.background_color)
        win.wm_title("Edit: Class List")
        win.geometry("350x195")
        win.resizable(width=True, height=False)

        label = Label(
            win,
            text="Select an assignment to edit.",
            fg=self.text_color,
            bg=self.background_color,
            font="TkDefaultFont 12",
        )
        label.pack(side=tkinter.TOP)

        scroll = Scrollbar(win, orient=tkinter.VERTICAL)
        scroll.pack(side=tkinter.RIGHT, fill=tkinter.Y)

        scrollbar_list = Listbox(
            win,
            yscrollcommand=scroll.set,
            width=20,
            fg=self.text_color,
            bg=self.background_color,
            font="TkDefaultFont 12",
        )
        classes = self.controller.get_classes()
        for i in classes:
            scrollbar_list.insert(tkinter.END, str(i))
        scrollbar_list.pack(side=tkinter.TOP, fill=tkinter.BOTH)
        scroll.config(command=scrollbar_list.yview)

        scrollbar_list.bind(
            "<Double-1>",
            lambda x: self.edit_single_class_window(scrollbar_list.get(tkinter.ACTIVE)),
        )

    def edit_single_class_window(self, class_str=str):
        win = Toplevel()
        win.configure(bg=self.background_color)
        win.wm_title("Edit: Class")
        win.geometry("500x250")
        topframe = tkinter.Frame(win, bg=self.background_color)
        topframe.grid(column=0, row=0)
        bottomframe = tkinter.Frame(win, bg=self.background_color)
        bottomframe.grid(column=0, row=1)
        win.columnconfigure(0, weight=1)
        win.rowconfigure(0, weight=1)

        class_label = Label(
            topframe, text="Class Name: ", bg=self.background_color, fg=self.text_color
        )
        class_label.grid(row=0, column=0)

        class_info = self.controller.get_class_str(class_str)

        class_entry_var = tkinter.StringVar()
        class_entry_var.set(class_info.name)
        class_entry = Entry(topframe, textvariable=class_entry_var)
        class_entry.grid(row=0, column=1)

        color_label = Label(
            topframe, text="Color: ", bg=self.background_color, fg=self.text_color
        )
        color_label.grid(row=1, column=0)

        color_box_var = tkinter.StringVar()
        color_box = ttk.Combobox(
            topframe, state="readonly", textvariable=color_box_var, width=15
        )
        color_box["values"] = [
            "firebrick3",
            "orange",
            "yellow2",
            "green2",
            "cyan",
            "deep sky blue",
            "medium purple",
            "snow",
        ]
        color_box.grid(row=1, column=1)

        for i in color_box["values"]:
            if i == class_info.color:
                color_box.current(color_box["values"].index(i))
                break
        ####################

        time_frame = tkinter.Frame(topframe, bg=self.background_color,)
        time_frame.grid(row=2, column=1)

        time_label = Label(
            topframe, text="Time:", bg=self.background_color, fg=self.text_color
        )
        time_label.grid(row=2, column=0)

        time_hour_var = tkinter.StringVar()
        time_hour_combo = ttk.Combobox(
            time_frame, state="readonly", textvariable=time_hour_var, width=5
        )
        time_hour_combo["values"] = [
            "1",
            "2",
            "3",
            "4",
            "5",
            "6",
            "7",
            "8",
            "9",
            "10",
            "11",
            "12",
        ]
        time_hour_combo.grid(row=0, column=0)

        time_semicolon_label = Label(
            time_frame, text=":", bg=self.background_color, fg=self.text_color
        )
        time_semicolon_label.grid(row=0, column=1)

        time_min_var = tkinter.StringVar()
        time_min_combo = ttk.Combobox(
            time_frame, state="readonly", textvariable=time_min_var, width=5
        )
        time_min_combo["values"] = ["00", "15", "30", "45"]
        time_min_combo.grid(row=0, column=2)

        time_ampm_var = tkinter.StringVar()
        time_ampm_combo = ttk.Combobox(
            time_frame, state="readonly", textvariable=time_ampm_var, width=5
        )
        time_ampm_combo["values"] = ["am", "pm"]
        time_ampm_combo.grid(row=0, column=3)

        ####################
        day_of_week_label = Label(
            topframe, text="Class Days:", fg=self.text_color, bg=self.background_color
        )
        day_of_week_label.grid(row=3, column=0)

        day_of_week_frame = tkinter.Frame(topframe, bg=self.background_color)
        day_of_week_frame.grid(row=3, column=1)

        monday_label = Label(
            day_of_week_frame, text="M", fg=self.text_color, bg=self.background_color,
        )
        monday_label.grid(row=0, column=0)
        monday_var = tkinter.StringVar()
        Checkbutton(
            day_of_week_frame,
            text="",
            variable=monday_var,
            fg=self.text_color,
            bg=self.background_color,
            onvalue="Monday",
            offvalue="",
            selectcolor=self.background_color,
            activeforeground=self.background_color,
        ).grid(row=1, column=0)

        tuesday_label = Label(
            day_of_week_frame, text="T", fg=self.text_color, bg=self.background_color,
        )
        tuesday_label.grid(row=0, column=1)
        tuesday_var = tkinter.StringVar()
        Checkbutton(
            day_of_week_frame,
            text="",
            variable=tuesday_var,
            fg=self.text_color,
            bg=self.background_color,
            onvalue="Tuesday",
            offvalue="",
            selectcolor=self.background_color,
            activeforeground=self.background_color,
        ).grid(row=1, column=1)

        wed_label = Label(
            day_of_week_frame, text="W", fg=self.text_color, bg=self.background_color,
        )
        wed_label.grid(row=0, column=2)
        wed_var = tkinter.StringVar()
        Checkbutton(
            day_of_week_frame,
            text="",
            variable=wed_var,
            fg=self.text_color,
            bg=self.background_color,
            onvalue="Wednesday",
            offvalue="",
            selectcolor=self.background_color,
            activeforeground=self.background_color,
        ).grid(row=1, column=2)

        thur_label = Label(
            day_of_week_frame, text="R", fg=self.text_color, bg=self.background_color,
        )
        thur_label.grid(row=0, column=3)
        thur_var = tkinter.StringVar()
        Checkbutton(
            day_of_week_frame,
            text="",
            variable=thur_var,
            fg=self.text_color,
            bg=self.background_color,
            onvalue="Thursday",
            offvalue="",
            selectcolor=self.background_color,
            activeforeground=self.background_color,
        ).grid(row=1, column=3)

        fri_label = Label(
            day_of_week_frame, text="F", fg=self.text_color, bg=self.background_color,
        )
        fri_label.grid(row=0, column=4)
        fri_var = tkinter.StringVar()
        Checkbutton(
            day_of_week_frame,
            text="",
            variable=fri_var,
            fg=self.text_color,
            bg=self.background_color,
            onvalue="Friday",
            offvalue="",
            selectcolor=self.background_color,
            activeforeground=self.background_color,
        ).grid(row=1, column=4)

        sat_label = Label(
            day_of_week_frame, text="S", fg=self.text_color, bg=self.background_color,
        )
        sat_label.grid(row=0, column=5)
        sat_var = tkinter.StringVar()
        Checkbutton(
            day_of_week_frame,
            text="",
            variable=sat_var,
            fg=self.text_color,
            bg=self.background_color,
            onvalue="Saturday",
            offvalue="",
            selectcolor=self.background_color,
            activeforeground=self.background_color,
        ).grid(row=1, column=5)

        def add_and_close_window():
            days_list = [
                monday_var.get(),
                tuesday_var.get(),
                wed_var.get(),
                thur_var.get(),
                fri_var.get(),
                sat_var.get(),
            ]
            days_list_final = []
            for i in days_list:
                if i != "":
                    days_list_final.append(i)

            self.controller.edit_class_str_2(
                class_str,
                class_entry_var.get(),
                color_box_var.get(),
                f"{time_hour_var.get()}:{time_min_var.get()} {time_ampm_var.get()}",
                days_list_final,
            )
            win.destroy()
            self.refresh_main()

        ok_button = Button(
            bottomframe,
            text="Ok",
            command=add_and_close_window,
            bg=self.background_color,
            fg=self.text_color,
        )
        ok_button.grid(row=0, column=0)

        cancel_button = Button(
            bottomframe,
            text="Cancel",
            command=win.destroy,
            bg=self.background_color,
            fg=self.text_color,
        )
        cancel_button.grid(row=0, column=1)

    def edit_assignment_window(self):
        win = Toplevel()
        win.configure(background=self.background_color)
        win.wm_title("Edit: Assignment List")
        win.geometry("350x195")
        win.resizable(width=True, height=False)

        label = Label(
            win,
            text="Select an assignment to edit.",
            fg=self.text_color,
            bg=self.background_color,
            font="TkDefaultFont 12",
        )
        label.pack(side=tkinter.TOP)

        scroll = Scrollbar(win, orient=tkinter.VERTICAL)
        scroll.pack(side=tkinter.RIGHT, fill=tkinter.Y)

        list_box = Listbox(
            win,
            yscrollcommand=scroll.set,
            width=20,
            fg=self.text_color,
            bg=self.background_color,
            font="TkDefaultFont 12",
            selectmode="browse",
        )
        assignments = self.controller.get_all_assignments()
        for i in assignments:
            list_box.insert(tkinter.END, str(i))
        list_box.pack(side=tkinter.TOP, fill=tkinter.BOTH)
        scroll.config(command=list_box.yview)

        # selected_assignment = list_box.curselection()

        list_box.bind(
            "<Double-1>", lambda x: self.edit_window(list_box.get(tkinter.ACTIVE)),
        )

    def version_window(self):
        win = Toplevel()
        win.configure(bg=self.background_color)
        win.wm_title("Version Details")
        win.geometry("700x250")
        topframe = tkinter.Frame(win, bg=self.background_color)
        topframe.grid(column=0, row=0)
        win.columnconfigure(0, weight=1)
        win.rowconfigure(0, weight=1)

        Label(
            topframe,
            text="8_25_20: first actual executable. Doesn't display classes on feed, +although you can edit which day classes are",
            bg=self.background_color,
            fg=self.text_color,
        ).grid(row=0)
        Label(
            topframe,
            text="8_31_20 v2: functional class display when they are in the day. Aswell as changing default window size.",
            bg=self.background_color,
            fg=self.text_color,
        ).grid(row=1)
        Label(
            topframe,
            text="9_2_20 : fixed main display so that it displays assignments in the proper order according to the time variable.",
            bg=self.background_color,
            fg=self.text_color,
        ).grid(row=2)
        Label(
            topframe,
            text="9_9_20 : displays 'Today', added info tab, save button",
            bg=self.background_color,
            fg=self.text_color,
        ).grid(row=3)
        Label(
            topframe,
            text="9_12_20 : bugs menu and messing with build options",
            bg=self.background_color,
            fg=self.text_color,
        ).grid(row=4)
        Label(
            topframe,
            text="""10_13_20 : \n1. You can configure if an assignment is complete or not in the 'edit assignment window.
            \n2. You can now turn off displaying classes in the main display.
            \nAlong with these, some logic fixes that seems to fix the problem of not properly displaying days at the
            end of the month. Lastly, you can now set an assignment to be due at '11:59', since I'm anal.""",
            bg=self.background_color,
            fg=self.text_color,
        ).grid(row=5)

    def about_window(self):
        root = Toplevel()
        root.resizable(width=False, height=False)
        root.geometry("720x250")
        container = ttk.Frame(root)
        canvas = tkinter.Canvas(container)
        canvas.config(width=700, height=250)
        scrollbar = ttk.Scrollbar(container, orient="vertical", command=canvas.yview)
        scrollable_frame = ttk.Frame(canvas)

        scrollable_frame.bind(
            "<Configure>", lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
        )

        canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")

        canvas.configure(yscrollcommand=scrollbar.set)

        long_ass_text = """9/7/20 @ 8ishpm:\n-Planning is key: planning is everything. You won't really have to write any code at all if you already think about general operations and structure of the program. Which leads into the next thing.
-Staying organized takes precedant over everything else. Making exceptions and makeshift ideas are okay when trying to get something to work for the first time; do not leave them in! Maintaining stable code becomes more and more difficult as time goes on. At this point, I feel like I should drop this project because of how awful it is at this point.
-Keeping a log of ideas was very helpful and important in letting my ideas flow. Also just like having a daily log of my activities.
-Although at times it feels like you don't know where to start, just do it in anyway at all. Honestly halting too much because you want to do something 'right' will be more time consuming and detrimental. Make the thing. Improve upon it. Keep doing that.

Lastly, in reference to this project. Yes, it has flaws. It's a fucking mess, actually. But, I've become comfortable in Python 3.x, and have had a more independent experience in making simple guis. In the process, I made a program that I'll use for the next 6 months and is something I'm happy I've made.

To summerize:
Planning and foresight is important.
Keeping your code OOP and organized is top priority.
Write a log of things getting done.
Start right now.

9/8/20 @ 10:59pmish: 
I feel like in the future I should try to do better research on more dynamic and clean gui techniques and plans.
Looking back, maybe learning how pack works instead of only grid will give me insight on different methods to similar goals.
Although I've understood grids this whole time, it's resulted in a more ameteur-ish style (I think).
"""

        """for i in range(50):
            ttk.Label(scrollable_frame, text="Sample scrolling label").pack()"""
        Label(
            scrollable_frame,
            text=long_ass_text,
            fg=self.text_color,
            bg=self.background_color,
            wraplength=700,
        ).pack()

        container.pack()
        canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")

    def bugs_window(self):
        win = Toplevel()
        win.configure(bg=self.background_color)
        win.wm_title("Known bugs")
        win.geometry("700x450")
        topframe = tkinter.Frame(win, bg=self.background_color)
        topframe.grid(column=0, row=0)
        win.columnconfigure(0, weight=1)
        win.rowconfigure(0, weight=1)

        Label(
            topframe,
            text=f"Current known bugs in {self.version}:",
            bg=self.background_color,
            fg=self.text_color,
            font="Bold",
        ).grid(row=0)
        Label(
            topframe,
            bg=self.background_color,
            fg=self.text_color,
            wraplength=450,
            text="""If there's a 12:30 class, it is sorted by time correctly. However, if there's a 12:30 class and an assignment in that class at the same time, it sends the 12:30 class to the end of the list (of that day).\n""",
        ).grid(row=1)
        Label(
            topframe,
            bg=self.background_color,
            fg=self.text_color,
            wraplength=450,
            text="""There is no error checking in any submission window. It doesn't even check if it's empty before taking it as data.\n""",
        ).grid(row=2)
        Label(
            topframe,
            bg=self.background_color,
            fg=self.text_color,
            # wraplength=450,
            text="""If two assignments have the same time, class, and title, it confuses the program on which assignment
            is trying to be modified. So, if you try to complete either of them, it will defualt to whichever one
            has a lower value (I believe). This is because the view figures out which of the assignments in the main display
            are selected via the assignment as a string. Since my tostring function only incorporates these three and not the
            description, this problem happens. However, changing tostring in assignment will break other segments of code.""",
        ).grid(row=3)

    def refresh_main(self):
        # Before, I was having issues with "leftover" text when an assignment was removed.
        # It seems this was becuase I was placing a frame into master/root, instead of deleting
        # it outright. So, if you place a frame ontop of another, the remnants will remain.
        # So, although this feels lazy, this loop literally deleted all children of master/root.
        # However, it isn't noticable at all so I'm fine with it.
        for widget in self.master.winfo_children():
            widget.destroy()
        self.master.configure(background=self.background_color)
        mainframe = tkinter.Frame(self.master, bg=self.background_color)
        mainframe.grid(column=0, row=0)
        buttonframe = tkinter.Frame(self.master, bg=self.background_color)
        buttonframe.grid(column=0, row=1)
        """rcaframe = ttk.Frame(self.master, padding="3 3 12 12", height=100)
        rcaframe.grid(column=0, row=2)"""
        self.master.columnconfigure(0, weight=1)
        self.master.rowconfigure(0, weight=1)

        menubar = Menu(self.master, bg=self.background_color, fg=self.text_color)
        self.master.config(menu=menubar)
        file_menu = Menu(
            menubar, tearoff=0, bg=self.background_color, fg=self.text_color
        )
        file_menu.add_command(
            label="New Assignment", command=self.add_assignment_window
        )
        file_menu.add_command(label="New Class", command=self.add_class_window)
        file_menu.add_separator()

        file_menu.add_command(label="Save", command=self.controller.save_no_exit)
        file_menu.add_command(label="Save & Exit", command=self.controller.save_exit)

        options_menu = Menu(
            menubar, tearoff=0, bg=self.background_color, fg=self.text_color
        )
        options_menu.add_command(
            label="Main Display", command=self.options_config_main_window
        )
        options_menu.add_command(label="Theme", command=self.options_theme_window)

        view_menu = Menu(
            menubar, tearoff=0, bg=self.background_color, fg=self.text_color
        )
        view_menu.add_command(
            label="All Assignments", command=self.view_all_assignments_window
        )
        view_menu.add_command(label="All Classes", command=self.view_all_classes_window)

        edit_menu = Menu(
            menubar, tearoff=0, bg=self.background_color, fg=self.text_color
        )
        edit_menu.add_command(
            label="Edit Assignment", command=self.edit_assignment_window
        )
        edit_menu.add_command(label="Edit Classes", command=self.edit_classes_window)

        info_menu = Menu(
            menubar, tearoff=0, bg=self.background_color, fg=self.text_color
        )
        info_menu.add_command(label="Version Info", command=self.version_window)
        info_menu.add_command(label="About", command=self.about_window)
        info_menu.add_command(label="Known Bugs", command=self.bugs_window)

        menubar.add_cascade(label="File", menu=file_menu)
        menubar.add_cascade(label="Edit", menu=edit_menu)
        menubar.add_cascade(label="View", menu=view_menu)
        menubar.add_cascade(label="Options", menu=options_menu)
        menubar.add_cascade(label="Info", menu=info_menu)

        week_of_assignments = self.controller.get_this_week(7)
        last_week_of_assignments = self.controller.get_last_week(2)

        row_number = 0

        measure_system = tkinter.StringVar()

        def switch_button_state():
            if delete_button["state"] == tkinter.DISABLED:
                delete_button["state"] = tkinter.NORMAL

            if edit_button["state"] == tkinter.DISABLED:
                edit_button["state"] = tkinter.NORMAL

            if complete_button["state"] == tkinter.DISABLED:
                complete_button["state"] = tkinter.NORMAL

        empty = None
        for i in week_of_assignments:
            for j in i:
                if str(type(j)) == "<class 'Assignment.Assignment'>":
                    empty = False
                    break
                if str(type(j)) == "<class 'AssignmentClass.AssignmentClass'>":
                    empty = False
                    break
        for i in last_week_of_assignments:
            for j in i:
                if str(type(j)) == "<class 'Assignment.Assignment'>":
                    empty = False
                    break
                if str(type(j)) == "<class 'AssignmentClass.AssignmentClass'>":
                    empty = False
                    break

        if empty == None:
            empty = True
            print("THERE IS NOTHING HERE APPARENTLY")

        # LOL
        nothing_here = True

        if empty:
            Label(
                mainframe,
                text="No assignments to display.\nTo add an assignment, go to File/New Assignment",
                font=(32),
                bg=self.background_color,
                fg=self.text_color,
            ).grid(row=0, column=0)
            print("EMPTY")
        else:
            all_assignments = last_week_of_assignments + week_of_assignments
            for day in all_assignments:
                # if the day is empty (has no assignments), don't do anything.

                # I MUST ADD CLASSES BEFORE CHECKING IF EMPTY !!!!!!!!!

                if not day:
                    print(f"List {day} is empty.")
                else:

                    continue_operations = True
                    # check if there's only a date
                    if str(type(day[0])) == "<class 'str'>":
                        if len(day) == 1:
                            print(f"DAY {day[0]} HAS BEEN SKIPPED")
                            continue_operations = False

                    # WEIRD STUFF SINCE WE HAVE TO GET THE DATE FROM LIST
                    # IF THERE ARE NO ASSIGNMENTS BUT CLASSES
                    ########################
                    if continue_operations:
                        todays_date = ""
                        day_formatted = ""

                        if str(type(day[0])) == "<class 'str'>":
                            todays_date = day[0]
                            day.pop(0)

                        # If there was no date, that means there's an assignment in there.
                        # Look for it.
                        # Otherwise, get the date from the string at index 0.
                        if todays_date == "":
                            for i in day:
                                if str(type(i)) == "<class 'Assignment.Assignment'>":
                                    day_formatted = i.due.split("/")
                        else:
                            day_formatted = todays_date.split("/")

                        ##########
                        day_formatted_final = f"{int(day_formatted[1])} {int(day_formatted[0])} 20{day_formatted[2]}"
                        day_numb = day_formatted[1]
                        day_name = self.find_day(day_formatted_final)
                        month_name = calendar.month_name[int(day_formatted[0])]
                        print(f"DAY_FORMATTED_FINAL: {day_formatted_final}")

                        date = datetime.datetime.now().date().strftime("%m/%d/%Y")
                        date_string_final = date[0:6] + date[8:]
                        date_string_final_2 = date_string_final.split("/")
                        today_formatted_final = f"{int(date_string_final_2[1])} {int(date_string_final_2[0])} 20{date_string_final_2[2]}"
                        tomorrow_formatted_final = f"{int(date_string_final_2[1])} {int(date_string_final_2[0])} 20{date_string_final_2[2]}"
                        print(f"TODAY_FORMATTED_FINAL: {today_formatted_final}")

                        if today_formatted_final == day_formatted_final:
                            date_label = Label(
                                mainframe,
                                # "Today ({day_name}, {month_name} {day_numb})",
                                text=f"Today",
                                font=(
                                    f"Tahoma {self.main_display_date_font + 16} underline bold"
                                ),
                                bg=self.background_color,
                                fg=self.text_color,
                            )
                        else:
                            date_label = Label(
                                mainframe,
                                text=f"{day_name}, {month_name} {day_numb}",
                                font=(
                                    f"Tahoma {self.main_display_date_font} underline"
                                ),
                                bg=self.background_color,
                                fg=self.text_color,
                            )

                        gross_check_for_assignment = False
                        if not self.class_display_check:
                            for thing in day:
                                if (
                                    str(type(thing))
                                    == "<class 'Assignment.Assignment'>"
                                ):
                                    gross_check_for_assignment = True
                                    nothing_here = False

                        # if gross_check_for_assignment:

                        if gross_check_for_assignment or self.class_display_check:
                            date_label.grid(column=0, row=row_number)
                            row_number += 1

                        day_organized = self.organize_day_by_time(day)

                        for assignment in day_organized:
                            the_type = str(type(assignment))

                            if the_type == "<class 'Assignment.Assignment'>":
                                nothing_here = False

                                assignment_font = None
                                if assignment.completed:
                                    assignment_font = font.Font(
                                        family="Helvetica",
                                        size=self.main_display_assignment_font,
                                        overstrike=1,
                                    )
                                else:
                                    assignment_font = font.Font(
                                        family="Helvetica",
                                        size=self.main_display_assignment_font,
                                        overstrike=0,
                                    )

                                Label(
                                    mainframe,
                                    text=f"{assignment.time}",
                                    font=assignment_font,
                                    bg=self.background_color,
                                    fg=self.text_color,
                                ).grid(column=0, row=row_number)
                                Label(
                                    mainframe,
                                    text=f"{assignment.a_class.name}",
                                    font=assignment_font,
                                    background=f"{assignment.a_class.color}",
                                    fg=self.class_text_color,
                                ).grid(column=1, row=row_number)
                                Label(
                                    mainframe,
                                    text=f"{assignment.title}",
                                    font=assignment_font,
                                    bg=self.background_color,
                                    fg=self.text_color,
                                ).grid(column=2, row=row_number)
                                if assignment.desc != "":
                                    Label(
                                        mainframe,
                                        text=f"{assignment.desc}",
                                        wraplength=100,
                                        justify="center",
                                        font=assignment_font,
                                        bg=self.background_color,
                                        fg=self.text_color,
                                    ).grid(column=3, row=row_number)
                                #####

                                if not assignment.completed:
                                    check = Radiobutton(
                                        mainframe,
                                        variable=measure_system,
                                        value=str(assignment),
                                        text=" ",
                                        command=switch_button_state,
                                        bg=self.background_color,
                                        fg=self.text_color,
                                        selectcolor=self.background_color,
                                        activeforeground=self.background_color,
                                        tristatevalue=0,
                                    )
                                    check.grid(column=4, row=row_number)

                                #####
                            else:
                                if self.class_display_check:
                                    nothing_here = False
                                    class_font = font.Font(
                                        family="Helvetica",
                                        size=self.main_display_assignment_font,
                                        overstrike=0,
                                    )
                                    Label(
                                        mainframe,
                                        text=f"{assignment.time}",
                                        font=class_font,
                                        bg=self.background_color,
                                        fg=self.text_color,
                                    ).grid(column=0, row=row_number)

                                    Label(
                                        mainframe,
                                        text=f"{assignment.name}",
                                        # text="????",
                                        font=class_font,
                                        background=f"{assignment.color}",
                                        fg=self.class_text_color,
                                    ).grid(column=1, row=row_number)
                                    Label(
                                        mainframe,
                                        text=f"CLASS",
                                        font=class_font,
                                        background=self.background_color,
                                        fg=self.text_color,
                                    ).grid(column=2, row=row_number)

                            row_number += 1
                row_number += 1

        if nothing_here:
            Label(
                mainframe,
                text="No assignments to display.\nTo add an assignment, go to File/New Assignment",
                font=(32),
                bg=self.background_color,
                fg=self.text_color,
            ).grid(row=0, column=0)

        delete_button = Button(
            buttonframe,
            text="Delete",
            command=lambda: self.delete_window(measure_system.get()),
            state=tkinter.DISABLED,
            fg=self.text_color,
            bg=self.background_color,
        )
        delete_button.grid(column=2, row=0)

        edit_button = Button(
            buttonframe,
            text="Edit",
            command=lambda: self.edit_window(measure_system.get()),
            state=tkinter.DISABLED,
            fg=self.text_color,
            bg=self.background_color,
        )
        edit_button.grid(column=0, row=0)

        complete_button = Button(
            buttonframe,
            text="Complete",
            command=lambda: self.complete_window(measure_system.get()),
            state=tkinter.DISABLED,
            fg=self.text_color,
            bg=self.background_color,
        )
        complete_button.grid(column=1, row=0)

    def add_assignment_window(self):

        win = Toplevel()
        win.configure(background=self.background_color)
        win.wm_title("Create New Assignment")
        win.geometry("500x250")
        topframe = tkinter.Frame(win, bg=self.background_color)
        topframe.grid(column=0, row=0)
        leftframe = tkinter.Frame(topframe, bg=self.background_color)
        leftframe.grid(column=0, row=0)
        rightframe = tkinter.Frame(topframe, bg=self.background_color)
        rightframe.grid(column=1, row=0)
        bottomframe = tkinter.Frame(win, bg=self.background_color)
        bottomframe.grid(column=0, row=1)

        win.columnconfigure(0, weight=1)
        win.rowconfigure(0, weight=1)

        class_label = Label(
            rightframe, text="Class:", bg=self.background_color, fg=self.text_color
        )
        class_label.grid(row=0, column=0)

        class_name_var = tkinter.StringVar()
        class_box = ttk.Combobox(
            rightframe, state="readonly", textvariable=class_name_var
        )
        class_box["values"] = self.controller.get_classes()
        class_box.grid(row=0, column=1)

        title_label = Label(
            leftframe, text="Title:", bg=self.background_color, fg=self.text_color
        )
        title_label.grid(row=1, column=0)

        title_var = tkinter.StringVar()
        title_entry = ttk.Entry(leftframe, textvariable=title_var)
        title_entry.grid(row=1, column=1)

        desc_label = Label(
            leftframe, text="Description:", bg=self.background_color, fg=self.text_color
        )
        desc_label.grid(row=2, column=0)

        desc_var = tkinter.StringVar()
        desc_textbox = tkinter.Text(
            leftframe, wrap="word", width=20, height=5, font="TkDefaultFont",
        )
        desc_textbox.grid(row=2, column=1)

        ###############
        time_label = Label(
            rightframe, text="Time:", bg=self.background_color, fg=self.text_color
        )
        time_label.grid(row=3, column=0)

        time_frame = tkinter.Frame(rightframe, bg=self.background_color)
        time_frame.grid(row=3, column=1)

        time_hour_var = tkinter.StringVar()
        time_hour_combo = ttk.Combobox(
            time_frame, state="readonly", textvariable=time_hour_var, width=5
        )
        time_hour_combo["values"] = [
            "1",
            "2",
            "3",
            "4",
            "5",
            "6",
            "7",
            "8",
            "9",
            "10",
            "11",
            "12",
        ]
        time_hour_combo.grid(row=0, column=0)

        time_semicolon_label = Label(
            time_frame, text=":", bg=self.background_color, fg=self.text_color
        )
        time_semicolon_label.grid(row=0, column=1)

        time_min_var = tkinter.StringVar()
        time_min_combo = ttk.Combobox(
            time_frame, state="readonly", textvariable=time_min_var, width=5
        )
        time_min_combo["values"] = ["00", "15", "30", "45", "59"]
        time_min_combo.grid(row=0, column=2)

        time_ampm_var = tkinter.StringVar()
        time_ampm_combo = ttk.Combobox(
            time_frame, state="readonly", textvariable=time_ampm_var, width=5
        )
        time_ampm_combo["values"] = ["am", "pm"]
        time_ampm_combo.grid(row=0, column=3)

        ##################
        date_label = Label(
            rightframe, text="Date Due:", bg=self.background_color, fg=self.text_color
        )
        date_label.grid(row=4, column=0)

        date_frame = tkinter.Frame(rightframe, bg=self.background_color)
        date_frame.grid(row=4, column=1)

        date_month_var = tkinter.StringVar()
        date_month_combo = ttk.Combobox(
            date_frame, state="readonly", textvariable=date_month_var, width=3
        )
        date_month_combo["values"] = [
            "1",
            "2",
            "3",
            "4",
            "5",
            "6",
            "7",
            "8",
            "9",
            "10",
            "11",
            "12",
        ]
        date_month_combo.grid(row=0, column=0)

        date_slash_label = Label(
            date_frame, text=" / ", bg=self.background_color, fg=self.text_color
        )
        date_slash_label.grid(row=0, column=1)

        date_day_var = tkinter.StringVar()
        date_day_combo = ttk.Combobox(
            date_frame, state="readonly", textvariable=date_day_var, width=3
        )
        temp_list = []
        for i in range(1, 32):
            temp_list.append(f"{i}")
        date_day_combo["values"] = temp_list
        date_day_combo.grid(row=0, column=2)

        date_slash_label_2 = Label(
            date_frame, text=" / 20", bg=self.background_color, fg=self.text_color
        )
        date_slash_label_2.grid(row=0, column=3)

        date_year_var = tkinter.StringVar()
        date_year_combo = ttk.Combobox(
            date_frame, state="readonly", textvariable=date_year_var, width=3
        )
        date_year_combo["values"] = ["20", "21", "22"]
        date_year_combo.grid(row=0, column=4)

        ##########################
        # FIX THIS SHIT
        ##########################
        def add_and_close_window():
            self.controller.add_assignment(
                Assignment.Assignment(
                    title_entry.get(),
                    desc_textbox.get("1.0", "end-1c"),
                    f"{time_hour_var.get()}:{time_min_var.get()} {time_ampm_var.get()}",
                    f"{date_month_var.get()}/{date_day_var.get()}/{date_year_var.get()}",
                    self.controller.get_class_str(class_name_var.get()),
                )
            )
            win.destroy()
            self.refresh_main()

        ok_button = Button(
            bottomframe,
            text="Ok",
            command=add_and_close_window,
            bg=self.background_color,
            fg=self.text_color,
        )
        ok_button.grid(row=0, column=0)

        cancel_button = Button(
            bottomframe,
            text="Cancel",
            command=win.destroy,
            bg=self.background_color,
            fg=self.text_color,
        )
        cancel_button.grid(row=0, column=1)

    def edit_window(self, assignment=str):
        if assignment == "":
            print("No value, so no window!")
            return
        else:
            # In here, we'll pop up the create assignment window
            # (pretty much the same), except with all of the
            # assignments' information already filled out.
            assignment_being_edited = self.controller.get_assignment_w_str(assignment)
            a_class = assignment_being_edited.a_class
            title = assignment_being_edited.title
            desc = assignment_being_edited.desc
            time = assignment_being_edited.time
            time2 = time.split(":")
            time_list = [time2[0], time2[1].split(" ")[0], time2[1].split(" ")[1]]
            print(time_list)
            due = assignment_being_edited.due
            due_list = due.split("/")

            win = Toplevel()
            win.configure(background=self.background_color)
            win.wm_title("Edit: Edit Assignment")
            win.geometry("500x250")
            topframe = tkinter.Frame(win, bg=self.background_color)
            topframe.grid(column=0, row=0)
            leftframe = tkinter.Frame(topframe, bg=self.background_color)
            leftframe.grid(column=0, row=0)
            rightframe = tkinter.Frame(topframe, bg=self.background_color)
            rightframe.grid(column=1, row=0)
            bottomframe = tkinter.Frame(win, bg=self.background_color)
            bottomframe.grid(column=0, row=1)

            win.columnconfigure(0, weight=1)
            win.rowconfigure(0, weight=1)

            class_label = Label(
                rightframe, text="Class:", bg=self.background_color, fg=self.text_color
            )
            class_label.grid(row=0, column=0)

            class_name_var = tkinter.StringVar()
            class_box = ttk.Combobox(
                rightframe, state="readonly", textvariable=class_name_var
            )
            class_box["values"] = self.controller.get_classes()
            ####
            for i in class_box["values"]:
                if i == a_class.name:
                    class_box.current(class_box["values"].index(i))
                    break
            ####
            class_box.grid(row=0, column=1)

            title_label = Label(
                leftframe, text="Title:", bg=self.background_color, fg=self.text_color
            )
            title_label.grid(row=1, column=0)

            title_var = tkinter.StringVar()
            title_var.set(title)
            title_entry = ttk.Entry(leftframe, textvariable=title_var)
            title_entry.grid(row=1, column=1)

            desc_label = Label(
                leftframe,
                text="Description:",
                bg=self.background_color,
                fg=self.text_color,
            )
            desc_label.grid(row=2, column=0)

            desc_textbox = tkinter.Text(
                leftframe, wrap="word", width=20, height=5, font="TkDefaultFont",
            )
            desc_textbox.insert(tkinter.END, desc)
            desc_textbox.grid(row=2, column=1)

            time_label = Label(
                rightframe, text="Time:", bg=self.background_color, fg=self.text_color
            )
            time_label.grid(row=3, column=0)

            time_frame = tkinter.Frame(rightframe, bg=self.background_color)
            time_frame.grid(row=3, column=1)

            time_hour_var = tkinter.StringVar()
            time_hour_combo = ttk.Combobox(
                time_frame, state="readonly", textvariable=time_hour_var, width=5
            )
            time_hour_combo["values"] = [
                "1",
                "2",
                "3",
                "4",
                "5",
                "6",
                "7",
                "8",
                "9",
                "10",
                "11",
                "12",
            ]
            #
            time_hour = time_list[0]
            for i in time_hour_combo["values"]:
                if i == time_hour:
                    time_hour_combo.current(time_hour_combo["values"].index(i))
                    break
            #
            time_hour_combo.grid(row=0, column=0)

            time_semicolon_label = Label(
                time_frame, text=":", bg=self.background_color, fg=self.text_color
            )
            time_semicolon_label.grid(row=0, column=1)

            time_min_var = tkinter.StringVar()
            time_min_combo = ttk.Combobox(
                time_frame, state="readonly", textvariable=time_min_var, width=5
            )
            time_min_combo["values"] = ["00", "15", "30", "45", "59"]
            #
            time_min = time_list[1]
            for i in time_min_combo["values"]:
                if i == time_min:
                    time_min_combo.current(time_min_combo["values"].index(i))
                    break
            #
            time_min_combo.grid(row=0, column=2)

            time_ampm_var = tkinter.StringVar()
            time_ampm_combo = ttk.Combobox(
                time_frame, state="readonly", textvariable=time_ampm_var, width=5
            )
            time_ampm_combo["values"] = ["am", "pm"]
            #
            time_ampm = time_list[2]
            if time_ampm_combo["values"][0] == time_ampm:
                time_ampm_combo.current(0)
            else:
                time_ampm_combo.current(1)
            #
            time_ampm_combo.grid(row=0, column=3)
            ##################
            date_label = Label(
                rightframe,
                text="Date Due:",
                bg=self.background_color,
                fg=self.text_color,
            )
            date_label.grid(row=4, column=0)

            date_frame = tkinter.Frame(rightframe, bg=self.background_color)
            date_frame.grid(row=4, column=1)

            date_month_var = tkinter.StringVar()
            date_month_combo = ttk.Combobox(
                date_frame, state="readonly", textvariable=date_month_var, width=3
            )
            date_month_combo["values"] = [
                "1",
                "2",
                "3",
                "4",
                "5",
                "6",
                "7",
                "8",
                "9",
                "10",
                "11",
                "12",
            ]
            #
            date_month = due_list[0]
            for i in date_month_combo["values"]:
                if i == date_month:
                    date_month_combo.current(date_month_combo["values"].index(i))
                    break
            #
            date_month_combo.grid(row=0, column=0)

            date_slash_label = Label(
                date_frame, text=" / ", bg=self.background_color, fg=self.text_color
            )
            date_slash_label.grid(row=0, column=1)

            date_day_var = tkinter.StringVar()
            date_day_combo = ttk.Combobox(
                date_frame, state="readonly", textvariable=date_day_var, width=3
            )
            temp_list = []
            for i in range(1, 32):
                temp_list.append(f"{i}")
            date_day_combo["values"] = temp_list
            #
            date_day = due_list[1]
            for i in date_day_combo["values"]:
                if i == date_day:
                    date_day_combo.current(date_day_combo["values"].index(i))
                    break
            #
            date_day_combo.grid(row=0, column=2)

            date_slash_label_2 = Label(
                date_frame, text=" / 20", bg=self.background_color, fg=self.text_color
            )
            date_slash_label_2.grid(row=0, column=3)

            date_year_var = tkinter.StringVar()
            date_year_combo = ttk.Combobox(
                date_frame, state="readonly", textvariable=date_year_var, width=3
            )
            date_year_combo["values"] = ["20", "21", "22"]
            #
            date_year = due_list[2]
            for i in date_year_combo["values"]:
                if i == date_year:
                    date_year_combo.current(date_year_combo["values"].index(i))
                    break
            #
            date_year_combo.grid(row=0, column=4)

            completed_var = tkinter.BooleanVar()
            # completed_var.set()
            Checkbutton(
                topframe,
                text="Assignment is completed",
                variable=completed_var,
                fg=self.text_color,
                bg=self.background_color,
                onvalue=True,
                offvalue=False,
                selectcolor=self.background_color,
                activeforeground=self.background_color,
            ).grid(row=5, column=1)

        ##########################
        # FIX THIS SHIT
        ##########################
        def edit_and_close_window():
            self.controller.delete_assignment_str(assignment)
            assignment_to_add = Assignment.Assignment(
                title_var.get(),  # was title.entry()
                desc_textbox.get("1.0", "end-1c"),
                f"{time_hour_var.get()}:{time_min_var.get()} {time_ampm_var.get()}",
                f"{date_month_var.get()}/{date_day_var.get()}/{date_year_var.get()}",
                self.controller.get_class_str(class_name_var.get()),
            )
            assignment_to_add.completed = completed_var.get()
            self.controller.add_assignment(assignment_to_add)
            win.destroy()
            self.refresh_main()

        ok_button = Button(
            bottomframe,
            text="Ok",
            command=edit_and_close_window,
            bg=self.background_color,
            fg=self.text_color,
        )
        ok_button.grid(row=0, column=0)

        cancel_button = Button(
            bottomframe,
            text="Cancel",
            command=win.destroy,
            bg=self.background_color,
            fg=self.text_color,
        )
        cancel_button.grid(row=0, column=1)

    def delete_window(self, assignment=str):
        if assignment == "":
            print("No value, so no window!")
            return
        else:
            print(assignment)
            # In here, pop up window that says are you sure?
            # Then on button hit on "yes", send str(assignment)
            # to controller method that removes assignment via
            # string ( make methods in model & controller).
            # THEN refresh main.
            win = Toplevel()
            win.configure(bg=self.background_color)
            win.wm_title("Edit: Delete Assignment")
            win.geometry("500x250")
            topframe = tkinter.Frame(win, bg=self.background_color)
            topframe.grid(column=0, row=0)
            bottomframe = tkinter.Frame(win, bg=self.background_color)
            bottomframe.grid(column=0, row=1)
            win.columnconfigure(0, weight=1)
            win.rowconfigure(0, weight=1)
            assignment_name = assignment.split(":")
            assignment_being_deleted = f"{assignment_name[0]} - {assignment_name[1]}"

            label = Label(
                topframe,
                text=f"Are you sure you want to delete '{assignment_being_deleted}'?",
                bg=self.background_color,
                fg=self.text_color,
            )
            label.grid(row=0, column=0)

            def del_and_close_window():
                self.controller.delete_assignment_str(assignment)
                win.destroy()
                self.refresh_main()

            ok_button = Button(
                bottomframe,
                text="Ok",
                command=del_and_close_window,
                bg=self.background_color,
                fg=self.text_color,
            )
            ok_button.grid(row=0, column=0)

            cancel_button = Button(
                bottomframe,
                text="Cancel",
                command=win.destroy,
                bg=self.background_color,
                fg=self.text_color,
            )
            cancel_button.grid(row=0, column=1)

    def add_class_window(self):

        win = Toplevel()
        win.configure(bg=self.background_color)
        win.wm_title("Create New Class")
        win.geometry("500x250")
        topframe = tkinter.Frame(win, bg=self.background_color)
        topframe.grid(column=0, row=0)
        bottomframe = tkinter.Frame(win, bg=self.background_color)
        bottomframe.grid(column=0, row=1)
        win.columnconfigure(0, weight=1)
        win.rowconfigure(0, weight=1)

        class_label = Label(
            topframe, text="Class Name: ", bg=self.background_color, fg=self.text_color
        )
        class_label.grid(row=0, column=0)

        class_entry_var = tkinter.StringVar()
        class_entry = Entry(topframe, textvariable=class_entry_var)
        class_entry.grid(row=0, column=1)

        color_label = Label(
            topframe, text="Color: ", bg=self.background_color, fg=self.text_color
        )
        color_label.grid(row=1, column=0)

        time_frame = tkinter.Frame(topframe, bg=self.background_color,)
        time_frame.grid(row=2, column=1)

        time_label = Label(
            topframe, text="Time:", bg=self.background_color, fg=self.text_color
        )
        time_label.grid(row=2, column=0)

        time_hour_var = tkinter.StringVar()
        time_hour_combo = ttk.Combobox(
            time_frame, state="readonly", textvariable=time_hour_var, width=5
        )
        time_hour_combo["values"] = [
            "1",
            "2",
            "3",
            "4",
            "5",
            "6",
            "7",
            "8",
            "9",
            "10",
            "11",
            "12",
        ]
        time_hour_combo.grid(row=0, column=0)

        time_semicolon_label = Label(
            time_frame, text=":", bg=self.background_color, fg=self.text_color
        )
        time_semicolon_label.grid(row=0, column=1)

        time_min_var = tkinter.StringVar()
        time_min_combo = ttk.Combobox(
            time_frame, state="readonly", textvariable=time_min_var, width=5
        )
        time_min_combo["values"] = ["00", "15", "30", "45"]
        time_min_combo.grid(row=0, column=2)

        time_ampm_var = tkinter.StringVar()
        time_ampm_combo = ttk.Combobox(
            time_frame, state="readonly", textvariable=time_ampm_var, width=5
        )
        time_ampm_combo["values"] = ["am", "pm"]
        time_ampm_combo.grid(row=0, column=3)

        """color_entry_var = tkinter.StringVar()
        class_entry = Entry(topframe, textvariable=color_entry_var)
        class_entry.grid(row=1, column=1)"""

        color_box_var = tkinter.StringVar()
        color_box = ttk.Combobox(
            topframe, state="readonly", textvariable=color_box_var, width=15
        )
        color_box["values"] = [
            "firebrick3",
            "orange",
            "yellow2",
            "green2",
            "cyan",
            "deep sky blue",
            "medium purple",
            "snow",
        ]
        color_box.grid(row=1, column=1)

        ####################

        day_of_week_label = Label(
            topframe, text="Class Days:", fg=self.text_color, bg=self.background_color
        )
        day_of_week_label.grid(row=3, column=0)

        day_of_week_frame = tkinter.Frame(topframe, bg=self.background_color)
        day_of_week_frame.grid(row=3, column=1)

        monday_label = Label(
            day_of_week_frame, text="M", fg=self.text_color, bg=self.background_color,
        )
        monday_label.grid(row=0, column=0)
        monday_var = tkinter.StringVar()
        Checkbutton(
            day_of_week_frame,
            text="",
            variable=monday_var,
            fg=self.text_color,
            bg=self.background_color,
            onvalue="Monday",
            offvalue="",
            selectcolor=self.background_color,
            activeforeground=self.background_color,
        ).grid(row=1, column=0)

        tuesday_label = Label(
            day_of_week_frame, text="T", fg=self.text_color, bg=self.background_color,
        )
        tuesday_label.grid(row=0, column=1)
        tuesday_var = tkinter.StringVar()
        Checkbutton(
            day_of_week_frame,
            text="",
            variable=tuesday_var,
            fg=self.text_color,
            bg=self.background_color,
            onvalue="Tuesday",
            offvalue="",
            selectcolor=self.background_color,
            activeforeground=self.background_color,
        ).grid(row=1, column=1)

        wed_label = Label(
            day_of_week_frame, text="W", fg=self.text_color, bg=self.background_color,
        )
        wed_label.grid(row=0, column=2)
        wed_var = tkinter.StringVar()
        Checkbutton(
            day_of_week_frame,
            text="",
            variable=wed_var,
            fg=self.text_color,
            bg=self.background_color,
            onvalue="Wednesday",
            offvalue="",
            selectcolor=self.background_color,
            activeforeground=self.background_color,
        ).grid(row=1, column=2)

        thur_label = Label(
            day_of_week_frame, text="R", fg=self.text_color, bg=self.background_color,
        )
        thur_label.grid(row=0, column=3)
        thur_var = tkinter.StringVar()
        Checkbutton(
            day_of_week_frame,
            text="",
            variable=thur_var,
            fg=self.text_color,
            bg=self.background_color,
            onvalue="Thursday",
            offvalue="",
            selectcolor=self.background_color,
            activeforeground=self.background_color,
        ).grid(row=1, column=3)

        fri_label = Label(
            day_of_week_frame, text="F", fg=self.text_color, bg=self.background_color,
        )
        fri_label.grid(row=0, column=4)
        fri_var = tkinter.StringVar()
        Checkbutton(
            day_of_week_frame,
            text="",
            variable=fri_var,
            fg=self.text_color,
            bg=self.background_color,
            onvalue="Friday",
            offvalue="",
            selectcolor=self.background_color,
            activeforeground=self.background_color,
        ).grid(row=1, column=4)

        sat_label = Label(
            day_of_week_frame, text="S", fg=self.text_color, bg=self.background_color,
        )
        sat_label.grid(row=0, column=5)
        sat_var = tkinter.StringVar()
        Checkbutton(
            day_of_week_frame,
            text="",
            variable=sat_var,
            fg=self.text_color,
            bg=self.background_color,
            onvalue="Saturday",
            offvalue="",
            selectcolor=self.background_color,
            activeforeground=self.background_color,
        ).grid(row=1, column=5)

        def add_and_close_window():
            days_list = [
                monday_var.get(),
                tuesday_var.get(),
                wed_var.get(),
                thur_var.get(),
                fri_var.get(),
                sat_var.get(),
            ]
            days_list_final = []
            for i in days_list:
                if i != "":
                    days_list_final.append(i)

            self.controller.add_class(
                class_entry_var.get(),
                color_box_var.get(),
                f"{time_hour_var.get()}:{time_min_var.get()} {time_ampm_var.get()}",
                days_list_final,
            )
            win.destroy()
            self.refresh_main()

        ok_button = Button(
            bottomframe,
            text="Ok",
            command=add_and_close_window,
            bg=self.background_color,
            fg=self.text_color,
        )
        ok_button.grid(row=0, column=0)

        cancel_button = Button(
            bottomframe,
            text="Cancel",
            command=win.destroy,
            bg=self.background_color,
            fg=self.text_color,
        )
        cancel_button.grid(row=0, column=1)

    def complete_window(self, assignment=str):
        if assignment == "":
            print("No value, so no window!")
            return
        else:
            win = Toplevel()
            win.configure(bg=self.background_color)
            win.wm_title("Complete Assignment")
            win.geometry("500x250")
            topframe = tkinter.Frame(win, bg=self.background_color)
            topframe.grid(column=0, row=0)
            bottomframe = tkinter.Frame(win, bg=self.background_color)
            bottomframe.grid(column=0, row=1)
            win.columnconfigure(0, weight=1)
            win.rowconfigure(0, weight=1)
            assignment_name = assignment.split(":")
            assignment_being_completed = f"{assignment_name[0]} - {assignment_name[1]}"

            label = Label(
                topframe,
                text=f"Are you sure you've completed '{assignment_being_completed}'?",
                bg=self.background_color,
                fg=self.text_color,
            )
            label.grid(row=0, column=0)

            def complete_and_close_window():
                self.controller.complete_assignment_str(assignment)
                win.destroy()
                self.refresh_main()

            ok_button = Button(
                bottomframe,
                text="Ok",
                command=complete_and_close_window,
                bg=self.background_color,
                fg=self.text_color,
            )
            ok_button.grid(row=0, column=0)

            cancel_button = Button(
                bottomframe,
                text="Cancel",
                command=win.destroy,
                bg=self.background_color,
                fg=self.text_color,
            )
            cancel_button.grid(row=0, column=1)

    def options_config_main_window(self):
        win = Toplevel()
        win.configure(bg=self.background_color)
        win.wm_title("Options: Main Display")
        win.geometry("500x250")
        topframe = tkinter.Frame(win, bg=self.background_color)
        topframe.grid(column=0, row=0)
        bottomframe = tkinter.Frame(win, bg=self.background_color)
        bottomframe.grid(column=0, row=1)

        win.columnconfigure(0, weight=1)
        win.rowconfigure(0, weight=1)

        future_label = Label(
            topframe,
            text="Future days to display:",
            bg=self.background_color,
            fg=self.text_color,
        )
        future_label.grid(row=0, column=0)

        past_label = Label(
            topframe,
            text="Past days to display:",
            bg=self.background_color,
            fg=self.text_color,
        )
        past_label.grid(row=1, column=0)

        future_var = tkinter.IntVar()
        future_var.set(self.controller.get_main_display_future_limit())
        future_entry = ttk.Entry(topframe, textvariable=future_var, width=5)
        future_entry.grid(row=0, column=1)

        past_var = tkinter.IntVar()
        past_var.set(self.controller.get_main_display_past_limit())
        past_entry = ttk.Entry(topframe, textvariable=past_var, width=5)
        past_entry.grid(row=1, column=1)

        ########

        date_font_label = Label(
            topframe,
            text="Date Font Size",
            bg=self.background_color,
            fg=self.text_color,
        )
        date_font_label.grid(row=2, column=0)

        date_font_var = tkinter.IntVar()
        date_font_var.set(self.main_display_date_font)
        date_font_combo = ttk.Combobox(
            topframe, state="readonly", textvariable=date_font_var, width=3,
        )

        numbs = []
        for i in range(8, 37):
            if (i % 2) == 0:
                current = str(i)
                print(current)
                numbs.append(current)
        date_font_combo["values"] = numbs
        date_font_combo.grid(row=2, column=1)

        assignment_font_label = Label(
            topframe,
            text="Assignment Font Size",
            bg=self.background_color,
            fg=self.text_color,
        )
        assignment_font_label.grid(row=3, column=0)

        assignment_font_var = tkinter.IntVar()
        assignment_font_var.set(self.main_display_assignment_font)
        assignment_font_combo = ttk.Combobox(
            topframe, state="readonly", textvariable=assignment_font_var, width=3
        )

        assignment_font_combo["values"] = numbs
        assignment_font_combo.grid(row=3, column=1)

        """display_class_label = Label(
            topframe, text="Dis", fg=self.text_color, bg=self.background_color,
        )"""
        # monday_label.grid(row=0, column=0)
        display_class_var = tkinter.BooleanVar()
        display_class_var.set(self.class_display_check)
        Checkbutton(
            topframe,
            text="Display Classes",
            variable=display_class_var,
            fg=self.text_color,
            bg=self.background_color,
            onvalue=True,
            offvalue=False,
            selectcolor=self.background_color,
            activeforeground=self.background_color,
        ).grid(row=4, column=0)

        def save_and_close_window():
            self.controller.change_main_display_options(
                future_var.get(), past_var.get()
            )
            self.main_display_date_font = date_font_var.get()
            self.main_display_assignment_font = assignment_font_var.get()
            self.class_display_check = display_class_var.get()
            win.destroy()
            self.refresh_main()

        ok_button = Button(
            bottomframe,
            text="Ok",
            command=save_and_close_window,
            bg=self.background_color,
            fg=self.text_color,
        )
        ok_button.grid(row=0, column=0)

        cancel_button = Button(
            bottomframe,
            text="Cancel",
            command=win.destroy,
            bg=self.background_color,
            fg=self.text_color,
        )
        cancel_button.grid(row=0, column=1)

    def options_theme_window(self):
        win = Toplevel()
        win.configure(background=self.background_color)
        win.wm_title("Options: Theme")
        win.geometry("500x250")
        topframe = tkinter.Frame(win, bg=self.background_color)
        topframe.grid(column=0, row=0)
        bottomframe = tkinter.Frame(win, bg=self.background_color)
        bottomframe.grid(column=0, row=1)

        win.columnconfigure(0, weight=1)
        win.rowconfigure(0, weight=1)

        theme_label = Label(
            topframe,
            text="Select Theme:",
            bg=self.background_color,
            fg=self.text_color,
        )
        theme_label.grid(row=0, column=0)

        theme_var = tkinter.StringVar()
        theme_var.set(self.theme)
        theme_combo = ttk.Combobox(
            topframe, state="readonly", textvariable=theme_var, width=10,
        )
        theme_combo["values"] = ["light", "dark"]
        theme_combo.grid(row=0, column=1)

        def save_and_close_window():
            print(theme_var.get())
            if theme_var.get() == "dark":
                self.set_dark_theme()
            else:
                self.set_light_theme()
            win.destroy()
            self.refresh_main()

        ok_button = Button(
            bottomframe,
            text="Ok",
            command=save_and_close_window,
            fg=self.text_color,
            bg=self.background_color,
        )
        ok_button.grid(row=0, column=0)

        cancel_button = Button(
            bottomframe,
            text="Cancel",
            command=win.destroy,
            fg=self.text_color,
            bg=self.background_color,
        )
        cancel_button.grid(row=0, column=1)

    def set_dark_theme(self):
        self.theme = "dark"
        self.text_color = "snow"
        self.background_color = "gray4"
        self.class_text_color = "gray12"

    def set_light_theme(self):
        self.theme = "light"
        self.text_color = "gray0"
        self.background_color = "SystemButtonFace"
        self.class_text_color = "gray0"

    def view_all_classes_window(self):
        win = Toplevel()
        win.configure(background=self.background_color)
        win.wm_title("View: All Classes")
        win.geometry("350x195")
        win.resizable(width=True, height=False)
        scroll = Scrollbar(win, orient=tkinter.VERTICAL)
        scroll.pack(side=tkinter.RIGHT, fill=tkinter.Y)

        scrollbar_list = Listbox(
            win,
            yscrollcommand=scroll.set,
            width=20,
            fg=self.text_color,
            bg=self.background_color,
            font="TkDefaultFont 12",
        )
        classes = self.controller.get_classes()
        for i in classes:
            final_string = f"{i.name} - {i.due} @ {i.time}"
            scrollbar_list.insert(tkinter.END, final_string)
            # scrollbar_list.insert(tkinter.END, str(i))
        scrollbar_list.pack(side=tkinter.TOP, fill=tkinter.BOTH)
        scroll.config(command=scrollbar_list.yview)

    def view_all_assignments_window(self):
        win = Toplevel()
        win.configure(background=self.background_color)
        win.wm_title("View: All Assignments")
        win.geometry("350x195")
        win.resizable(width=True, height=False)

        scroll = Scrollbar(win, orient=tkinter.VERTICAL)
        scroll.pack(side=tkinter.RIGHT, fill=tkinter.Y)

        scrollbar_list = Listbox(
            win,
            yscrollcommand=scroll.set,
            width=20,
            fg=self.text_color,
            bg=self.background_color,
            font="TkDefaultFont 12",
        )
        assignments = self.controller.get_all_assignments()
        for i in assignments:
            scrollbar_list.insert(tkinter.END, str(i))
        scrollbar_list.pack(side=tkinter.TOP, fill=tkinter.BOTH)
        scroll.config(command=scrollbar_list.yview)

    # MUST BE FORMATTED LIKE 'DD MM YYYY'
    def find_day(self, date):
        born = datetime.datetime.strptime(date, "%d %m %Y").weekday()
        return calendar.day_name[born]

    def find_month(self, date):
        born = datetime.datetime.strptime(date, "%d %m %Y").weekday()
        return calendar.month_name[born]

    def save(self):
        final_dump = [
            self.theme,
            self.text_color,
            self.background_color,
            self.class_text_color,
            self.main_display_date_font,
            self.main_display_assignment_font,
            self.class_display_check,
        ]
        pickle_file = open("view.txt", "wb")
        pickle_file.truncate(0)
        pickle.dump(final_dump, pickle_file)

    def load(self):
        stuff = pickle.load(open("view.txt", "rb"))
        self.theme = stuff[0]
        self.text_color = stuff[1]
        self.background_color = stuff[2]
        self.class_text_color = stuff[3]
        self.main_display_date_font = stuff[4]
        self.main_display_assignment_font = stuff[5]
        self.class_display_check = stuff[6]

    """def organize_day_by_time(self, assignments=list):
        am_list = []
        pm_list = []
        for assignment in assignments:
            if assignment.time.split(" ")[1] == "am":
                print(f"{assignment} added to am")
                am_list.append(assignment)
            else:
                print(f"{assignment} added to pm")
                pm_list.append(assignment)

        both_lists = [am_list, pm_list]
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
                    timej1 = arr[j].time.split(" ")
                    timej15 = timej1[0]
                    # timej2 = timej15.split[":"]
                    # timej3 = str(timej2[0]) + str(timej2[1])

                    timejj1 = arr[j + 1].time.split(" ")[0]
                    # timejj2 = timejj1.split[":"]
                    # timejj3 = str(timejj2[0]) + str(timejj2[1])

                    if timej15 > timejj1:
                        arr[j], arr[j + 1] = arr[j + 1], arr[j]

            sorted_list += arr
        return sorted_list"""

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

        """for i in after_ten_pm_list:
            if int(i.time.split(":")[0]) == 12:
                after_ten_pm_list.insert(
                    0, after_ten_am_list.pop(after_ten_am_list.index(i))
                )"""

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

    def new_test_window(self):
        win = Toplevel()
        win.wm_title("Create New Assignment")
        win.geometry("500x250")
        frame = ttk.Frame(win, padding="3 3 12 12")
        frame.grid(column=0, row=0)
        win.columnconfigure(0, weight=1)
        win.rowconfigure(0, weight=1)

        def switchButtonState():
            if but["state"] == tkinter.NORMAL:
                but["state"] = tkinter.DISABLED
            else:
                but["state"] = tkinter.NORMAL

        but = Button(frame, text="Button 1", state=tkinter.DISABLED)
        but2 = Button(frame, text="EN/DS", command=switchButtonState)
        but.grid(row=0)
        but2.grid(row=1)

