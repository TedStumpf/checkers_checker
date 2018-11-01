#   main.py
#   Theodore Stumpf
#   The class responsible for starting the Kivy interface and main menu
#import kivy
from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.gridlayout import GridLayout
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.image import Image
from sys import exit

class MenuScreen(Screen):
    def __init__(self, **kwargs):
        super(MenuScreen, self).__init__(**kwargs)
        self.name = 'screen_main'

        self.base_layout = BoxLayout()
        self.add_widget(self.base_layout)

        self.base_layout.add_widget(Image(source = "img/menu_img.png", size_hint=(.6, 1)))

        self.button_list = BoxLayout(orientation='vertical', padding = 10, spacing = 10, size_hint=(.4, 1))
        self.base_layout.add_widget(self.button_list)

        buttons = []
        buttons.append(Button(id = 'btn_test', text = "Test Players"))
        buttons.append(Button(id = 'btn_train', text = "Train Players"))
        buttons.append(Button(id = 'btn_review', text = "Review Players"))
        buttons.append(Button(id = 'btn_exit', text = "Exit"))
        for b in buttons:
            b.bind(on_press = self.callback)
            self.button_list.add_widget(b)

    def callback(self, instance):
        print('The button <%s> is being pressed' % instance.text)
        if (instance.id == 'btn_exit'):
            exit()


class Main(App):

    def build(self):
        menu = MenuScreen()
        self.screenmanager = ScreenManager()
        self.screenmanager.add_widget(menu)
        self.screenmanager.current = menu.name
        return self.screenmanager



if (__name__ == '__main__'):
    Main().run()