import json
from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.screenmanager import Screen, ScreenManager
from kivy.uix.label import Label
from kivy.lang import Builder
from kivy.uix.button import Button
from kivy.core.window import Window
from kivy.uix.gridlayout import GridLayout
from kivy.graphics import Rectangle
from kivy.uix.scrollview import ScrollView

Builder.load_file('main.kv')
def draw_rectangle_on_canvas(self, source_path='bg_for_menu.jpg'):
    with self.canvas.before:  # Используем canvas.before для заднего фона
        Rectangle(source=source_path, size=self.size, pos=self.pos)


class Menu_app(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        draw_rectangle_on_canvas(self)
        button_menu = GridLayout(cols=1, padding=[.2, .3], spacing=3, size_hint=(.7, .5), pos_hint={'center_x':.5, 'center_y':.5})
        #для доп функций можно переделать создание кнопок не в ручную, а считывание
        but_first_object = Button(background_normal='', background_color=(.3, .3, .4, .85), text='Торговый центр', font_size=45)
        but_second_object = Button(background_normal='', background_color=(.3, .3, .4, .85), text='Парк', font_size=45)
        but_third_object = Button(background_normal='', background_color=(.3, .3, .4, .85), text='Котлован', font_size=45)

        but_first_object.bind(on_press=self.go_to_first_object)
        but_second_object.bind(on_press=self.go_to_second_object)
        but_third_object.bind(on_press=self.go_to_third_object)
        button_menu.add_widget(but_first_object)
        button_menu.add_widget(but_second_object)
        button_menu.add_widget(but_third_object)
        self.add_widget(button_menu)


    def go_to_first_object(self, *args):
        self.manager.transition.direction = 'left'
        self.manager.current = 'first'

    def go_to_second_object(self, *args):
        self.manager.transition.direction = 'left'
        self.manager.current = 'second'

    def go_to_third_object(self, *args):
        self.manager.transition.direction = 'left'
        self.manager.current = 'third'


class Object(Screen):
    def __init__(self, file_json, name_o, addres, **kwargs):
        super().__init__(**kwargs)
        draw_rectangle_on_canvas(self)
        name_object = Label(text=('Объект - '  + name_o), font_name='Roboto-Regular.ttf', font_size=35, size_hint=(0.2, 0.05), pos_hint={'x': 0.43, 'y': 0.85})
        addres_object = Label(text=('Адрес - ' + addres), font_name='Roboto-Regular.ttf', font_size=35, size_hint=(0.2, 0.05), pos_hint={'x': 0.43, 'y': 0.8})
        return_menu = Button(text='Назад', background_normal='', background_color=(.3, .3, .4, .85), size_hint=(0.2, 0.05),
                             pos_hint={'x': 0.02, 'y': 0.93}, font_name='Roboto-Regular.ttf', font_size=35)
        return_menu.bind(on_press=self.go_to_menu)
        sv = ScrollView(do_scroll_x = True, pos_hint={'center_x':.53, 'center_y':.4}, size_hint = (1, .65))
        grid = GridLayout(cols=6, spacing=5, size_hint = (.95, .8))
        with open(file_json, "r", encoding='utf-8') as f:
            self.estimate = json.load(f)
        #self.name_object = name_o
        #self.address = addres

        for item in self.estimate['warehouse']:
            text1 = Label(text=item['material_name'], halign='left', size_hint_x=0.3)
            grid.add_widget(text1)
            text2 = Label(text=item['unit_of_measure'], halign='left', size_hint_x=0.15)
            grid.add_widget(text2)
            text3 = Label(text=str(item['quantity']), halign='left', size_hint_x=0.05)
            grid.add_widget(text3)
            text4 = Label(text=str(item['price']), halign='left', size_hint_x=0.15)
            grid.add_widget(text4)
            but_provider = Button(text=item['supplier'], halign='left', size_hint_x=0.25, background_normal='', background_color=(.3, .3, .4, .85))
            but_provider.bind(on_press=self.switch_screen_callback(item['id_screen']))
            grid.add_widget(but_provider)
            text6 = Label(text=item['date_received'], halign='left', size_hint_x=0.15)
            grid.add_widget(text6)
        sv.add_widget(grid)
        self.add_widget(sv)
        self.add_widget(return_menu)
        self.add_widget(name_object)
        self.add_widget(addres_object)

    def go_to_menu(self, *args):
        self.manager.transition.direction = 'right'
        self.manager.current = 'menu'

    def switch_screen_callback(self, screen_name):
        def callback(instance):
            if screen_name in self.manager.screen_names:
                self.manager.current = screen_name
            else:
                print(f"Error: Screen '{screen_name}' not found in ScreenManager.")

        return callback


class Supplier(Screen):
    def __init__(self, name_s, information, **kwargs):
        super().__init__(**kwargs)
        draw_rectangle_on_canvas(self)
        bxlt = BoxLayout(pos_hint={'center_x':.53, 'center_y':.6}, size_hint = (.8, .65))
        bxlt.add_widget(Label(text=information['information']))
        name_object = Label(text=(name_s), font_name='Roboto-Regular.ttf', font_size=35,
                            size_hint=(0.2, 0.05), pos_hint={'x': 0.43, 'y': 0.85})
        return_menu = Button(text='Назад', background_normal='', background_color=(.3, .3, .4, .85),
                             size_hint=(0.2, 0.05),
                             pos_hint={'x': 0.02, 'y': 0.93}, font_name='Roboto-Regular.ttf', font_size=35)
        return_menu.bind(on_press=self.go_to_menu)
        self.add_widget(name_object)
        self.add_widget(return_menu)
        self.add_widget(bxlt)


    def go_to_menu(self, *args):
        self.manager.transition.direction = 'right'
        self.manager.current = 'menu'



class MyApp(App):
    def build(self):
        Window.size = (800, 800)
        first_obj = Object(file_json='object_first.json', name_o='Торговый центр', addres='Улица Гоголя, 13, Новосибирск', name='first')
        second_obj = Object(file_json='object_first.json', name_o='Парк', addres='Улица Мичурина, 8, Новосибирск', name='second')
        third_obj = Object(file_json='object_first.json', name_o='Котлован', addres='Улица Горский, 64, Новосибирск', name='third')

        with open('information_supplier.json', "r", encoding='utf-8') as f:
            sup_information = json.load(f)

        stroy_market_sup = Supplier(name_s='СтройМаркет', information=sup_information['sup'][0], name='stroy_market')

        sm = ScreenManager()
        screen_menu = Menu_app(name='menu')
        sm.add_widget(screen_menu)
        sm.add_widget(first_obj)
        sm.add_widget(second_obj)
        sm.add_widget(third_obj)
        sm.add_widget(stroy_market_sup)

        return sm

if __name__ == '__main__':
    MyApp().run()