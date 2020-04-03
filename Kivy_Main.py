import kivy
from kivy.app import App
from kivy.uix.label import Label
from kivy.uix.gridlayout import GridLayout
from kivy.uix.textinput import TextInput
from kivy.uix.button import Button
from kivy.uix.widget import Widget
from kivy.properties import ObjectProperty
from kivy.lang import Builder
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.uix.progressbar import ProgressBar
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.floatlayout import FloatLayout



class MainWindow(Screen):
    pass

class StatWindow(Screen):
    pass

class WindowManager(ScreenManager):
    pass

class ProgBar(BoxLayout):
    pass

kv = Builder.load_file("Kivy_Home.kv")


class PlantGrid(Widget):
    moisture = ObjectProperty(None)
    light = ObjectProperty(None)

    def btn(self):
        print("Moisture:", self.moisture.text, "Light:", self.light.text)
        self.moisture.text = ''
        self.light.text = ''


class PlantE(App):
    #no need for init cos App has an in  it itself

    def build(self):
        return kv

if __name__ == '__main__':
    PlantE().run()                    #.run is from App from kivy.app