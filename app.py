from kivy.app import App, Builder
from kivy.uix.widget import Widget

Builder.load_file("ui/app.kv")


class MainWindow(Widget):
    pass


class SquareGardenApp(App):
    def build(self):
        return MainWindow()


if __name__ == "__main__":
    SquareGardenApp().run()
    # TODO use pipe metaphor in UI? pipes connecting sources and drains?
