#   main.py
#   Theodore Stumpf
#   The class responsible for starting the Kivy interface and main menu
import kivy

from kivy.app import App
from kivy.uix.label import Label

class Main(App):

	def build(self):
		return Label(text="Hello Checkers")

if (__name__ == '__main__'):
	Main().run()