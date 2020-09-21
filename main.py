from kivy.app import App
from kivy.lang import Builder
from kivy.uix.screenmanager import Screen, ScreenManager
from hoverable import HoverBehavior
from kivy.uix.behaviors import ButtonBehavior
from kivy.uix.image import Image
import json, glob
from datetime import datetime
from pathlib import Path
import random

# window is provided by kivy.sdl2 package ---installed using project interpreter

Builder.load_file('design.kv')


# <<.........................LOGIN SCREEN............................>
class LoginScreen(Screen):
    def login(self, uname, pword):
        with open('users.json') as file:
            users = json.load(file)
            if uname in users.keys() and users[uname]['password'] == pword:
                self.ids.username.text = ''
                self.ids.password.text = ''
                self.ids.login_wrong.text = ''
                self.manager.current = 'login_screensuccess'
            else:
                self.ids.login_wrong.text = "Wrong username or password"

    def signup(self):
        self.manager.current = 'signup_screen'


# <<........................SIGN UP SCREEN........................>>
class SignUpScreen(Screen):
    def add_user(self, uname, pword):
        with open('users.json', 'r') as file:
            users = json.load(file)
            users[uname] = {'username': uname, 'password': pword,
                            'created': datetime.now().strftime("%Y-%m-%d %H-%M-%S")}
        print(users)
        with open('users.json', 'w') as file:
            json.dump(users, file, indent=2)
        self.manager.current = 'signup_screensuccess'


# <<........................SUCCESS SIGN UP........................>>
class SignUpScreenSuccess(Screen):
    def login_page(self):
        self.manager.current = 'login_screen'


# <<........................SUCCESS LOGIN...........................>>
class LoginScreenSuccess(Screen):
    def log_out(self):
        self.manager.current = 'login_screen'

    def get_quote(self, feel):
        feel = feel.lower()
        avail_feel = glob.glob('quotes/*.txt')
        avail_feel = [Path(filename).stem for filename in avail_feel]
        if feel in avail_feel:
            with open(f"quotes/{feel}.txt", encoding="utf8") as file:
                quotes = file.readlines()
                print(quotes)
            self.ids.quote.text = random.choice(quotes)
        else:
            self.ids.quote.text = 'Try another feeling'


# <<........................LOGOUT BUTTON............................>>
class ImageButton(ButtonBehavior, HoverBehavior, Image):
    pass


# <<........................ROOT WIDGET............................>>
class RootWidget(ScreenManager):
    pass


# <<........................MAIN APP...............................>>
class MainApp(App):
    def build(self):
        return RootWidget()


if __name__ == "__main__":
    MainApp().run()
