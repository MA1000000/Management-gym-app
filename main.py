import csv
import pandas as pd
from csv import DictReader
from kivy.lang import Builder
from kivy.metrics import dp
from kivy.uix.screenmanager import ScreenManager
from kivy.uix.textinput import TextInput
from kivymd.uix.button import MDFlatButton, MDRaisedButton
from kivymd.uix.dialog import MDDialog
from kivymd.app import MDApp
from kivy.core.window import Window
from kivymd.uix.boxlayout import MDBoxLayout
import datetime
import calendar
from kivymd.uix.expansionpanel import MDExpansionPanel, MDExpansionPanelThreeLine
from kivymd.uix.list import ThreeLineListItem
from kivymd.uix.snackbar import Snackbar

Window.size = 340, 610

weekdays = {1: "Monday",
            2: "Tuesday",
            3: "Wednesday",
            4: "Thursday",
            5: "Friday",
            6: "Saturday",
            7: "Sunday"}
now_present_day = datetime.date.today()

global now1
now1 = now_present_day


def send_date_time():
    now = datetime.datetime.now()
    date = now.strftime("%d/%m/%Y, %H:%M:%S")
    return date


class Content(MDBoxLayout):
    first_1st_text = ''  # class name
    second_1st_text = ''  # date
    second_1st_text_2 = ''  # time range
    tertiary_1st_text = ''  # coach name

    first_2nd_text = ''  # class name
    second_2nd_text = ''  # date
    second_2nd_text_2 = ''  # time range
    tertiary_2nd_text = ''  # coach name

    first_3rd_text = ''  # class name
    second_3rd_text = ''  # date
    second_3rd_text_2 = ''  # time range
    tertiary_3rd_text = ''  # coach name

    FirstName = ''
    LastName = ''
    Email = ''
    Password = ''

    def book_lesson(self, meeting_date_and_range):
        self.find_meeting(meeting_date_and_range)

    def find_meeting(self, date_and_range):
        date = date_and_range[0:10]
        time_range1 = date_and_range[16:28]
        line_num = 0
        with open(f'meeting.csv', 'r') as f:
            reader = csv.DictReader(f)
            for row in reader:
                line_num += 1

                if row['date'] == date and row['time_range'] == time_range1:
                    """print(line_num)"""
                    self.find_next_spot(line_num, date, time_range1)

                elif date_and_range == 'no      practice':
                    Snackbar(text="No Practice!!!", snackbar_x="10dp", snackbar_y="10dp",
                             size_hint_y=.08, hovering=0.1,
                             size_hint_x=(Window.width - (dp(10) * 2)) / Window.width,
                             bg_color=(104 / 255, 104 / 255, 104 / 255, 1),
                             font_size="13sp").open()

    def csvr_reader(self):
        with open(f'meeting.csv', 'r') as g:
            reader = csv.DictReader(g)
            csvr = csv.reader(g)
            csvr = list(csvr)
            return csvr

    def ucsvr_reader(self):
        df = pd.read_csv(f'u_{self.Email}.csv')
        df.sort_values(by='date', inplace=True)
        df.to_csv(f'u_{self.Email}.csv', index=False)

    def find_next_spot(self, line_number, date, time_range2):
        csvr = self.csvr_reader()
        num_of_registered = int(csvr[line_number][5])
        if num_of_registered < int(csvr[line_number][4]):
            details = f"{self.Email}"
            line_len = len(csvr[line_number])
            valid = True
            for colum in range(5, line_len):
                if str(details) == str(csvr[line_number][colum]):
                    valid = False
                    Snackbar(text="Already signed for this class!", snackbar_x="10dp", snackbar_y="10dp",
                             size_hint_y=.08, hovering=0.1,
                             size_hint_x=(Window.width - (dp(10) * 2)) / Window.width,
                             bg_color=(104 / 255, 104 / 255, 104 / 255, 1),
                             font_size="13sp").open()

            if valid:
                self.add_user_to_class_data(line_number)
                Snackbar(text="Thank you for signing up! You will get answer shortly", snackbar_x="10dp",
                         snackbar_y="10dp",
                         size_hint_y=.08, hovering=0.1,
                         size_hint_x=(Window.width - (dp(10) * 2)) / Window.width,
                         bg_color=(104 / 255, 104 / 255, 104 / 255, 1),
                         font_size="13sp").open()


        else:
            Snackbar(text="Meeting Full!", snackbar_x="10dp", snackbar_y="10dp",
                     size_hint_y=.08, hovering=0.1,
                     size_hint_x=(Window.width - (dp(10) * 2)) / Window.width,
                     bg_color=(104 / 255, 104 / 255, 104 / 255, 1),
                     font_size="13sp").open()

    def add_user_to_class_data(self, line_number):
        details = f"{self.Email}"
        csvr = self.csvr_reader()
        csvr[line_number].append(details)
        x = csvr[line_number][5]
        y = int(x)
        y += 1
        csvr[line_number][5] = y
        user_meeting_line = []
        for value in range(0, 4):
            user_meeting_line.append(csvr[line_number][value])

        with open(f'meeting.csv', 'w', newline='') as f:
            writer = csv.writer(f)
            writer.writerows(csvr)

        with open(f'u_{self.Email}.csv', 'a', newline='') as g:
            writer = csv.writer(g)
            writer.writerow(user_meeting_line)

        self.ucsvr_reader()


class MyApp(MDApp):
    """uor app"""

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.email = ''
        self.password = ''
        self.first_name = ''
        self.last_name = ''
        self.login_password = ''
        self.login_email = ''

    def build(self):
        """ func for screens and pick screen manager to switch between screens """
        self.theme_cls.theme_style = "Light"
        global screen_manager
        screen_manager = ScreenManager()
        screen_manager.add_widget(Builder.load_file("ScreenLogin.kv"))
        screen_manager.add_widget(Builder.load_file("ScreenMain.kv"))
        screen_manager.add_widget(Builder.load_file("ScreenAddMeetings.kv"))
        screen_manager.add_widget(Builder.load_file("ScreenMyAccount.kv"))
        screen_manager.add_widget(Builder.load_file("ScreenMyMeeting.kv"))
        screen_manager.add_widget(Builder.load_file("ScreenSignUp.kv"))
        screen_manager.add_widget(Builder.load_file("ScreenContact.kv"))
        return screen_manager

    def selected_meeting_rows(self):
        # Convert date column to Timestamp object
        df['date'] = pd.to_datetime(df['date'])

        # Sort df  'date' column
        sorted_df = df.sort_values(by='date')

        # Calculate the date range from today until two weeks from today
        today = pd.Timestamp.now().floor('D')
        two_weeks = today + pd.Timedelta(days=14)

        # Select rows where the date is within the specified range
        selected_rows = sorted_df[(sorted_df['date'] >= today) & (sorted_df['date'] <= two_weeks)]

        return selected_rows

    def book_a_lesson(self):

        selected_rows = self.selected_meeting_rows()
        status = 'open'

        for i in range(0, len(selected_rows)):
            day = now1.isoweekday()

            with open(f'meeting.csv', 'r') as f:
                reader = csv.DictReader(f)
                counter = 1
                for row in reader:
                    if row['date'] == str(now1) and counter == 1:
                        Content.first_1st_text = row['class_name']
                        Content.second_1st_text_2 = row['time_range']
                        Content.second_1st_text = row['date']
                        Content.tertiary_1st_text = row['coach_name']
                        counter += 1

                    elif row['date'] == str(now1) and counter == 2:
                        Content.first_2nd_text = row['class_name']
                        Content.second_2nd_text_2 = row['time_range']
                        Content.second_2nd_text = row['date']
                        Content.tertiary_2nd_text = row['coach_name']
                        counter += 1
                    elif row['date'] == str(now1) and counter == 3:
                        Content.first_3rd_text = row['class_name']
                        Content.second_3rd_text_2 = row['time_range']
                        Content.second_3rd_text = row['date']
                        Content.tertiary_3rd_text = row['coach_name']
                        counter += 1
                    elif row['date'] != str(now1) and counter == 1:
                        Content.first_1st_text = 'no practice'
                        Content.second_1st_text = 'no '
                        Content.second_1st_text_2 = 'practice'
                        Content.tertiary_1st_text = 'no practice'
                        Content.first_2nd_text = 'no practice'
                        Content.second_2nd_text = 'no '
                        Content.second_2nd_text_2 = 'practice'
                        Content.tertiary_2nd_text = 'no practice'
                        Content.first_3rd_text = 'no practice'
                        Content.second_3rd_text = 'no '
                        Content.second_3rd_text_2 = 'practice'
                        Content.tertiary_3rd_text = 'no practice'

            self.root.get_screen("screen_add_meeting").ids.box.add_widget(
                MDExpansionPanel(
                    icon="clock-plus-outline",
                    content=Content(),
                    panel_cls=MDExpansionPanelThreeLine(
                        text=(str(now1) + '    ' + str(weekdays[day])),
                        secondary_text=status,
                    )
                )
            )
            now1 += datetime.timedelta(days=1)

    def valid_new_user_names(self, first, last):
        """בודקת שהשם לא מכיל מספרים ורווחים גם על השם משפחה"""
        if len(first) < 21 and len(last) < 21 and len(first) > 1 and len(last) > 1:
            return True
        elif len(first) > 21 or len(last) > 21:
            Snackbar(text="First Name or Last Name are too long!", snackbar_x="10dp", snackbar_y="10dp",
                     size_hint_y=.08, hovering=0.1,
                     size_hint_x=(Window.width - (dp(10) * 2)) / Window.width,
                     bg_color=(104 / 255, 104 / 255, 104 / 255, 1),
                     font_size="13sp").open()
            return False
        elif len(first) < 2 or len(last) < 2:
            Snackbar(text="First Name or Last Name are too short!", snackbar_x="10dp", snackbar_y="10dp",
                     size_hint_y=.08, hovering=0.1,
                     size_hint_x=(Window.width - (dp(10) * 2)) / Window.width,
                     bg_color=(104 / 255, 104 / 255, 104 / 255, 1),
                     font_size="13sp").open()
            return False

    def valid_new_user_email(self, email):
        """check user input email and give a response"""
        if len(email) < 4:
            Snackbar(text="Email too short!", snackbar_x="10dp", snackbar_y="10dp",
                     size_hint_y=.08, hovering=0.1,
                     size_hint_x=(Window.width - (dp(10) * 2)) / Window.width,
                     bg_color=(104 / 255, 104 / 255, 104 / 255, 1),
                     font_size="13sp").open()
            return False

        at_counter = 0
        for i in range(0, len(email)):
            if email[i] == '@':
                at_counter += 1
        if email[-1] == 'm' and email[-2] == 'o' and email[-3] == 'c' and email[-4] == '.' and at_counter == 1:
            with open(f'users.csv', 'r') as f:
                reader = csv.DictReader(f)
                for row in reader:
                    if row['Email'] == email:
                        Snackbar(text="This email has an account!", snackbar_x="10dp", snackbar_y="10dp",
                                 size_hint_y=.08, hovering=0.1,
                                 size_hint_x=(Window.width - (dp(10) * 2)) / Window.width,
                                 bg_color=(104 / 255, 104 / 255, 104 / 255, 1),
                                 font_size="13sp").open()
                        return False
                return True
        else:
            Snackbar(text="Check your Email!", snackbar_x="10dp", snackbar_y="10dp",
                     size_hint_y=.08, hovering=0.1,
                     size_hint_x=(Window.width - (dp(10) * 2)) / Window.width,
                     bg_color=(104 / 255, 104 / 255, 104 / 255, 1),
                     font_size="13sp").open()
            return False

    def valid_new_user_password(self, password):
        """check user input password and response"""
        if len(password) < 11 and len(password) > 3:
            return True
        else:
            Snackbar(text="Password should be between 4-10 letters !", snackbar_x="10dp", snackbar_y="10dp",
                     size_hint_y=.08, hovering=0.1,
                     size_hint_x=(Window.width - (dp(10) * 2)) / Window.width,
                     bg_color=(104 / 255, 104 / 255, 104 / 255, 1),
                     font_size="13sp").open()
            return False

    def open_new_user_csv(self):
        """create for new users there file"""

        head = ['date', 'time_range', 'class_name', 'coach_name']
        with open(f'u_{self.email}.csv', 'a') as f:
            writer = csv.writer(f)
            writer.writerow(head)

    def get_sign_up_data(self, first, last, email, password):
        """get user input and send for verification """

        if (self.valid_new_user_names(first, last) and
                self.valid_new_user_password(password) and
                self.valid_new_user_email(email)):
            self.email = email
            self.password = password
            self.first_name = first
            self.last_name = last
            self.open_new_user_csv()
            Snackbar(text="Signed Up successfully, Log In to continue!", snackbar_x="10dp", snackbar_y="10dp",
                     size_hint_y=.08, hovering=0.1,
                     size_hint_x=(Window.width - (dp(10) * 2)) / Window.width,
                     bg_color=(104 / 255, 104 / 255, 104 / 255, 1),
                     font_size="13sp").open()
            self.add_new_user_to_bank_users_file()

    def get_log_in_data(self, email, password):
        """get login data, check it, and response """

        with open(f'users.csv', 'r') as f:
            reader = csv.DictReader(f)
            found = False
            for row in reader:
                if row['Email'] == email and row['Password'] == password:
                    screen_manager.current = "main_screen"
                    screen_manager.transition.direction = "right"
                    self.email = email
                    self.password = password
                    self.first_name = row['First_name']
                    self.last_name = row['Last_name']
                    Content.FirstName = row['First_name']
                    Content.LastName = row['Last_name']
                    Content.Email = email
                    Content.Password = password
                    self.user_info_to_my_account()
                    self.user_future_meetings()

                    found = True
            if not found:
                Snackbar(text="Email or Password are incorrect ", snackbar_x="10dp", snackbar_y="10dp",
                         size_hint_y=.08, hovering=0.1,
                         size_hint_x=(Window.width - (dp(10) * 2)) / Window.width,
                         bg_color=(104 / 255, 104 / 255, 104 / 255, 1),
                         font_size="13sp").open()

    def add_new_user_to_bank_users_file(self):
        """add ned user to uor file"""

        new_user = [f'{self.email}', f'{self.password}',
                    f'{self.first_name}',
                    f'{self.last_name}',
                    f'{send_date_time()}']

        with open(f'users.csv', 'a', newline='') as f:
            writer = csv.writer(f)
            writer.writerow(new_user)

    def user_info_to_my_account(self):
        """ func to post the user deletes on is account page"""

        screen_manager.get_screen(
            "my_account_screen").first_n_last_name.text = f"Name:   {self.first_name} {self.last_name}"
        screen_manager.get_screen("my_account_screen").user_email.text = f"Email:   {self.email}"

    def location_message(self):
        """ dialog for our address, needs to be connect to waze or other maps
        ones user press on the locating icon he will see dialog"""

        self.dialog = MDDialog(
            elevation=0,
            radius=[20, 7, 20, 7],
            title="Our Location ",
            type="simple",
            buttons=[
                MDRaisedButton(
                    text=" Yeda Am St 8, Ramat Gan",
                    icon="car-side",
                    elevation=1.2,
                    md_bg_color=(237 / 255, 239 / 255, 241 / 255, 255),
                    theme_text_color="Custom",
                    text_color=(0, 0, 0, 1),
                    pos_hint={"center_y": .7},
                ),
            ],
        )
        self.dialog.open()

    def phone_message(self):
        """ dialog to call us, needs to sand to he's phone,
         ones user press on the locating icon he will see dialog"""

        self.dialog = MDDialog(
            elevation=1.2,
            radius=[20, 7, 20, 7],
            title="Call The Office ?",
            type="simple",
            buttons=[
                MDRaisedButton(
                    text="     Call      ",
                    elevation=1.2,
                    md_bg_color=(237 / 255, 239 / 255, 241 / 255, 255),
                    theme_text_color="Custom",
                    text_color=(0, 0, 0, 1),
                    pos_hint={"center_y": .7},
                ),
                MDFlatButton(
                    text="Cancel",
                    theme_text_color="Custom",
                    text_color=(0, 0, 0, 1),
                    on_release=self.close_dialog,
                    pos_hint={"center_y": .7},
                ),

            ],
        )
        self.dialog.open()

    def user_future_meetings(self):
        """get user meeting from he's file and post it on is meeting page"""

        with open(f'u_{self.email}.csv', 'r') as fl:
            data = DictReader(fl)
            for row in data:
                screen_manager.get_screen('screen_my_meeting').ids.future_meetings.add_widget(
                    ThreeLineListItem(
                        text=f"Date: {row['date']}",
                        secondary_text=f"Time: {row['time_range']}",
                        tertiary_text=f"Class: {row['class_name']},    Coach Name: {row['coach_name']} ",
                    )
                )

    def close_dialog(self, obj):
        """ close dialog, foe all dialog"""

        self.dialog.dismiss()


global df
df = pd.read_csv('meeting.csv')

MyApp().run()
