#   training_gui.py
from kivy.uix.screenmanager import Screen
from kivy.uix.button import Button
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.gridlayout import GridLayout
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.slider import Slider
import random

class TrainingScreen(Screen):
    def __init__(self, parent_app, **kwargs):
        super(TrainingScreen, self).__init__(**kwargs)
        self.parent_app = parent_app
        self.name = 'screen_training'

        #   Local Variables
        self.configuring = True
        self.in_training = False

        #   Layout setup
        self.base_layout = BoxLayout()
        self.add_widget(self.base_layout)

        #   Sublists
        self.slider_list = BoxLayout(orientation='vertical', padding = 10, spacing = 10, size_hint=(.7, 1))
        self.base_layout.add_widget(self.slider_list)
        self.button_list = BoxLayout(orientation='vertical', padding = 10, spacing = 10, size_hint=(.3, 1))
        self.base_layout.add_widget(self.button_list)

        #   Buttons
        buttons = []
        buttons.append(Button(id = 'btn_start', text = "Start"))
        buttons.append(Button(id = 'btn_back', text = "Back"))
        for b in buttons:
            b.bind(on_press = self.callback)
            self.button_list.add_widget(b)

        #   Sliders
        self.sliders = []
        t = Label(text = "Population Size")
        s = Slider(min=10, max=1000, value=500, step = 5, value_track=True, value_track_color=[0, 0.8, 0.8, 1])
        self.sliders.append((t, s))
        t = Label(text = "Batches")
        s = Slider(min=1, max=20, value=1, step = 1, value_track=True, value_track_color=[0, 0.8, 0.8, 1])
        self.sliders.append((t, s))
        t = Label(text = "Top Percentage to Keep")
        s = Slider(min=0, max=20, value=5, step = 1, value_track=True, value_track_color=[0, 0.8, 0.8, 1])
        self.sliders.append((t, s))
        t = Label(text = "Percentage of Mixed Contestants to Keep")
        s = Slider(min=0, max=50, value=40, step = 1, value_track=True, value_track_color=[0, 0.8, 0.8, 1])
        self.sliders.append((t, s))
        t = Label(text = "Percentage of New Contestants")
        s = Slider(min=0, max=30, value=10, step = 1, value_track=True, value_track_color=[0, 0.8, 0.8, 1])
        self.sliders.append((t, s))
        t = Label(text = "Games to Play")
        s = Slider(min=1, max=30, value=5, step = 1, value_track=True, value_track_color=[0, 0.8, 0.8, 1])
        self.sliders.append((t, s))

        for t, s in self.sliders:
            t.base_text = t.text
            s.label = t
            t.text = t.base_text + ": " + str(int(s.value))
            if 'Percentage' in t.base_text:
                t.text += "%"
            s.bind(value = self.slider_move)

            self.slider_list.add_widget(t)
            self.slider_list.add_widget(s)

    #   Slider
    def slider_move(self, instance, value):
        instance.label.text = instance.label.base_text + ": " + str(int(value))
        if 'Percentage' in instance.label.base_text:
            instance.label.text += "%"


    #   Used when the 
    def callback(self, instance):
        print('The button <%s> is being pressed' % instance.text)
        if (instance.id == 'btn_back'):
            self.parent_app.screenmanager.current = 'screen_main'
            