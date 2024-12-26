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
from kivy.properties import NumericProperty
from kivy.graphics import Color, Rectangle
from kivy.core.text import LabelBase
from kivy.uix.image import Image
from kivy.uix.relativelayout import RelativeLayout
from kivy.uix.textinput import TextInput
from kivy.storage.jsonstore import JsonStore

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

        bid = Button(text='Заявка', background_normal='', background_color=(.3, .3, .4, .85), size_hint=(0.2, 0.05),
                             pos_hint={'x': 0.78, 'y': 0.93}, font_name='Roboto-Regular.ttf', font_size=35)
        bid.bind(on_press=self.switch_screen_callback('add_' + str(self.name)))

        but_warehouse = Button(text='Склад', background_normal='', background_color=(.3, .3, .4, .85), size_hint=(0.2, 0.05),
                             pos_hint={'x': 0.55, 'y': 0.93}, font_name='Roboto-Regular.ttf', font_size=35)
        but_warehouse.bind(on_press=self.switch_screen_callback('warehouse_' + str(self.name)))

        sv = ScrollView(do_scroll_x = True, pos_hint={'center_x':.53, 'center_y':.45}, size_hint = (1, .55))
        grid = GridLayout(cols=6, spacing=4, size_hint = (.95, .8))
        grid_for_name = GridLayout(cols=6, spacing=5, size_hint=(.95, .2), pos_hint={'center_x':.5, 'center_y':.75})
        with open(file_json, "r", encoding='utf-8') as f:
            self.estimate = json.load(f)
            sum_estimate = 0
        # здесь создание таблицы с данные для сметы
            for item in self.estimate['warehouse']:
                sum_estimate += item['price'] * item['quantity']
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
        grid_for_name.add_widget(Label(text='Материалы', halign='left', size_hint_x=0.35))
        grid_for_name.add_widget(Label(text='Ед. изм.', halign='left', size_hint_x=0.15))
        grid_for_name.add_widget(Label(text='Кол-во', halign='left', size_hint_x=0.08))
        grid_for_name.add_widget(Label(text='Цена', halign='left', size_hint_x=0.15))
        grid_for_name.add_widget(Label(text='Поставщик', halign='left', size_hint_x=0.25))
        grid_for_name.add_widget(Label(text='Дата', halign='left', size_hint_x=0.17))
        sv.add_widget(grid)
        self.add_widget(but_warehouse)
        self.add_widget(Label(text=('Итог - ' + str(sum_estimate) + ' руб.'), font_name='Roboto-Regular.ttf', font_size=35, size_hint=(0.2, 0.05), pos_hint={'x': 0.1, 'y': 0.1}))
        self.add_widget(sv)
        self.add_widget(return_menu)
        self.add_widget(bid)
        self.add_widget(name_object)
        self.add_widget(addres_object)
        self.add_widget(grid_for_name)


    def go_to_menu(self, *args):
        self.manager.transition.direction = 'right'
        self.manager.current = 'menu'

    # для переключения на экран именно поставщика
    def switch_screen_callback(self, screen_name):
        def callback(instance):
            if screen_name in self.manager.screen_names:
                self.manager.transition.direction = 'left'
                self.manager.current = screen_name
            else:
                print(f"Error: Screen '{screen_name}' not found in ScreenManager.")

        return callback


# для адаптации текста нормального чтобы автоматом перенос строки был
class FitTextLabel(Label):
    font_size = NumericProperty(20)

    def on_size(self, *args):
        self.adjust_font_size()

    def on_text(self, *args):
        self.adjust_font_size()

    def adjust_font_size(self):
        font_size = self.font_size
        if not self.size or self.text is None:
            return
        while True:
             self.font_size = font_size
             text_width, text_height = self.texture_size
             if text_width > self.width or text_height > self.height:
                 font_size -= 1
             else:
                 break
        self.font_size = font_size

class Supplier(Screen):
    def __init__(self, name_s, information, previos_sc,  **kwargs):
        super().__init__(**kwargs)
        background_image = Image(source='bg_for_menu.jpg', allow_stretch=True, keep_ratio=False)
        self.add_widget(background_image)

        # Главный макет
        main_layout = RelativeLayout()

        #  название поставщика вверху
        name_object = Label(text=(name_s), font_name='Roboto-Regular.ttf', font_size=75,
                           size_hint=(0.2, 0.05), pos_hint={'x': 0.43, 'y': 0.85},
                           halign='center', valign='middle')
        main_layout.add_widget(name_object)


        # Кнопка "Назад"
        return_menu = Button(text='Назад', background_normal='', background_color=(.3, .3, .4, .85),
                             size_hint=(None, None), size=(100,40),
                             pos_hint={'x': 0.02, 'top': 0.98}, font_name='Roboto-Regular.ttf', font_size=20)
        return_menu.bind(on_press=self.switch_screen_callback(previos_sc))
        main_layout.add_widget(return_menu)

        # Текст описания поставщика
        text_box = FitTextLabel(text=information['information'], font_name='Roboto-Regular.ttf',
                                     halign='left', valign='top', font_size=35,
                                     text_size=(700, None), size_hint = (.7, .7), size=(.7, .7),
                                     pos_hint={'center_x': .5, 'center_y': .6})
        main_layout.add_widget(text_box)

        # Добавление layout на экран
        self.add_widget(main_layout)

    def go_to_menu(self, instance):
        self.manager.current = 'menu'


    # для дальнейших работ, переход не в меню, а просто назад
    def switch_screen_callback(self, screen_name):
        def callback(instance):
            if screen_name in self.manager.screen_names:
                self.manager.transition.direction = 'right'
                self.manager.current = screen_name
            else:
                print(f"Error: Screen '{screen_name}' not found in ScreenManager.")

        return callback


class RequestAddition(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        background_image = Image(source='bg_for_menu.jpg', allow_stretch=True, keep_ratio=False)
        self.add_widget(background_image)
        return_obj = Button(text='Назад', background_normal='', background_color=(.3, .3, .4, .85),
                             size_hint=(0.2, 0.05),
                             pos_hint={'x': 0.02, 'y': 0.93}, font_name='Roboto-Regular.ttf', font_size=35)
        return_obj.bind(on_press=self.switch_screen_callback(self.name[4:]))

        add_materials = GridLayout(cols=1, padding=[.2, .3], spacing=3, size_hint=(.7, .7),
                                 pos_hint={'center_x': .5, 'center_y': .5})
        add_materials.add_widget(Label(text='Поставщик', font_name='Roboto-Regular.ttf', font_size=35))
        self.sup_add = TextInput(font_size=35)
        add_materials.add_widget(self.sup_add)
        add_materials.add_widget(Label(text='Дата поставки', font_name='Roboto-Regular.ttf', font_size=35))
        self.data_add = TextInput(font_size=35)
        add_materials.add_widget(self.data_add)
        add_materials.add_widget(Label(text='Материал', font_name='Roboto-Regular.ttf', font_size=35))
        self.mater_add = TextInput(font_size=35)
        add_materials.add_widget(self.mater_add)
        add_materials.add_widget(Label(text='Кол-во', font_name='Roboto-Regular.ttf', font_size=35))
        self.count_add = TextInput(font_size=35)
        add_materials.add_widget(self.count_add)
        add_materials.add_widget(Label(text='Ед. изм.', font_name='Roboto-Regular.ttf', font_size=35))
        self.uni_add = TextInput(font_size=35)
        add_materials.add_widget(self.uni_add)
        add_materials.add_widget(Label(text='Цена', font_name='Roboto-Regular.ttf', font_size=35))
        self.price_add = TextInput(font_size=35)
        add_materials.add_widget(self.price_add)

        but_add = Button(text='Добавить', background_normal='', background_color=(.3, .3, .4, .85),
                             size_hint=(0.2, 0.05), pos_hint={'center_x': .5, 'center_y': .1}, font_name='Roboto-Regular.ttf', font_size=35)
        but_add.bind(on_press=self.add_in_file)

        self.add_widget(but_add)
        self.add_widget(add_materials)
        self.add_widget(return_obj)

    def switch_screen_callback(self, screen_name):
        def callback(instance):
            if screen_name in self.manager.screen_names:
                self.manager.transition.direction = 'right'
                self.manager.current = screen_name
            else:
                print(f"Error: Screen '{screen_name}' not found in ScreenManager.")

        return callback

    def add_in_file(self, instance):
        info_id = self.find_value_by_key("name_s", self.sup_add.text, "id_screen")
        file_j = 'object_' + self.name[4:] + '.json'
        print(file_j)

        new_info_mat = {"material_name": self.mater_add.text,
                        "unit_of_measure": self.uni_add.text,
                        "quantity": int(self.count_add.text),
                        "price": int(self.price_add.text),
                        "supplier": self.sup_add.text,
                        "date_received": self.data_add.text,
                        "id_screen": info_id
                        }

        store = JsonStore('stock.json')
        with open(file_j, 'r+', encoding='utf-8') as file:
            data = json.load(file)
            data["warehouse"].append(new_info_mat)
            file.seek(0)
            json.dump(data, file, indent=2)
            file.truncate()
        print(new_info_mat)

    def find_value_by_key(self, search_key, search_value, target_key):
        with open('information_supplier.json', 'r', encoding='utf-8') as f:
            data = json.load(f)
            for obj in data["sup"]:
                if isinstance(obj, dict) and search_key in obj and obj[search_key] == search_value:
                    if target_key in obj:
                        return obj[target_key]



class WarehouseObject(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        return_menu = Button(text='Назад', background_normal='', background_color=(.3, .3, .4, .85),
                             size_hint=(0.2, 0.05),
                             pos_hint={'x': 0.02, 'y': 0.93}, font_name='Roboto-Regular.ttf', font_size=35)
        return_menu.bind(on_press=self.switch_screen_callback(self.name[10:]))
        self.add_widget(return_menu)
        sv = ScrollView(do_scroll_x=True, pos_hint={'center_x': .53, 'center_y': .45}, size_hint=(1, .7))
        grid = GridLayout(cols=6, spacing=4, size_hint=(.95, .8))
        grid_for_name = GridLayout(cols=6, spacing=5, size_hint=(.95, .2), pos_hint={'center_x': .5, 'center_y': .87})
        with open('warehouse_for_' + str(self.name)[10:] + '_object.json', "r", encoding='utf-8') as f:
            self.estimate = json.load(f)
            sum_estimate = 0
            # здесь создание таблицы с данные для сметы
            for item in self.estimate['warehouse']:
                text1 = Label(text=item['material_name'], halign='left', size_hint_x=0.3)
                grid.add_widget(text1)
                text2 = Label(text=item['unit_of_measure'], halign='left', size_hint_x=0.15)
                grid.add_widget(text2)
                text3 = Label(text=str(item['quantity']), halign='left', size_hint_x=0.05)
                grid.add_widget(text3)
                text4 = Label(text=str(item['price']), halign='left', size_hint_x=0.15)
                grid.add_widget(text4)
                but_provider = Label(text=item['supplier'], halign='left', size_hint_x=0.25)
                grid.add_widget(but_provider)
                text6 = Label(text=item['date_received'], halign='left', size_hint_x=0.15)
                grid.add_widget(text6)
        grid_for_name.add_widget(Label(text='Материалы', halign='left', size_hint_x=0.3, font_size=30))
        grid_for_name.add_widget(Label(text='Ед. изм.', halign='left', size_hint_x=0.18, font_size=30))
        grid_for_name.add_widget(Label(text='Кол-во', halign='left', size_hint_x=0.1, font_size=30))
        grid_for_name.add_widget(Label(text='Цена', halign='left', size_hint_x=0.15, font_size=30))
        grid_for_name.add_widget(Label(text='Поставщик', halign='left', size_hint_x=0.25, font_size=30))
        grid_for_name.add_widget(Label(text='Дата', halign='left', size_hint_x=0.17, font_size=30))
        sv.add_widget(grid)
        self.add_widget(sv)
        self.add_widget(grid_for_name)

    def switch_screen_callback(self, screen_name):
        def callback(instance):
            if screen_name in self.manager.screen_names:
                self.manager.transition.direction = 'right'
                self.manager.current = screen_name
            else:
                print(f"Error: Screen '{screen_name}' not found in ScreenManager.")

        return callback


class MyApp(App):
    def build(self):
        Window.size = (800, 800)
        # создание классов объектов стройки
        first_obj = Object(file_json='object_first.json', name_o='Торговый центр', addres='Улица Гоголя, 13, Новосибирск', name='first')
        second_obj = Object(file_json='object_second.json', name_o='Парк', addres='Улица Мичурина, 8, Новосибирск', name='second')
        third_obj = Object(file_json='object_third.json', name_o='Котлован', addres='Улица Горский, 64, Новосибирск', name='third')
        bid_first = RequestAddition(name='add_first')
        bid_second = RequestAddition(name='add_second')
        bid_third = RequestAddition(name='add_third')

        warehouse_first = WarehouseObject(name='warehouse_first')
        warehouse_second = WarehouseObject(name='warehouse_second')
        warehouse_third = WarehouseObject(name='warehouse_third')

        with open('information_supplier.json', "r", encoding='utf-8') as f:
            sup_information = json.load(f)

        # создание классов для поставщиков, в будущем можно из файла информацию брать наверное
        stroy_market_sup = Supplier(name_s=sup_information['sup'][0]['name_s'], information=sup_information['sup'][0], previos_sc='menu', name=sup_information['sup'][0]['id_screen'])
        stroy_mir_sup = Supplier(name_s=sup_information['sup'][1]['name_s'], information=sup_information['sup'][1], previos_sc='menu', name=sup_information['sup'][1]['id_screen'])
        pesok_service_sup = Supplier(name_s=sup_information['sup'][2]['name_s'], information=sup_information['sup'][2], previos_sc='menu', name=sup_information['sup'][2]['id_screen'])
        scheben_trans_sup = Supplier(name_s=sup_information['sup'][3]['name_s'], information=sup_information['sup'][3], previos_sc='menu', name=sup_information['sup'][3]['id_screen'])
        kirpichny_zavod_sup = Supplier(name_s=sup_information['sup'][4]['name_s'], information=sup_information['sup'][4], previos_sc='menu', name=sup_information['sup'][4]['id_screen'])
        les_hoz_sup = Supplier(name_s=sup_information['sup'][5]['name_s'], information=sup_information['sup'][5], previos_sc='menu', name=sup_information['sup'][5]['id_screen'])
        metizy_sup = Supplier(name_s=sup_information['sup'][6]['name_s'], information=sup_information['sup'][6], previos_sc='menu', name=sup_information['sup'][6]['id_screen'])
        kraski_pro_sup = Supplier(name_s=sup_information['sup'][7]['name_s'], information=sup_information['sup'][7], previos_sc='menu', name=sup_information['sup'][7]['id_screen'])
        stroy_mix_sup = Supplier(name_s=sup_information['sup'][8]['name_s'], information=sup_information['sup'][8], previos_sc='menu', name=sup_information['sup'][8]['id_screen'])
        oboi_dom_sup = Supplier(name_s=sup_information['sup'][9]['name_s'], information=sup_information['sup'][9], previos_sc='menu', name=sup_information['sup'][9]['id_screen'])

        sm = ScreenManager()
        screen_menu = Menu_app(name='menu')
        sm.add_widget(screen_menu)
        sm.add_widget(bid_first)
        sm.add_widget(bid_second)
        sm.add_widget(bid_third)
        sm.add_widget(warehouse_first)
        sm.add_widget(warehouse_second)
        sm.add_widget(warehouse_third)
        sm.add_widget(first_obj)
        sm.add_widget(second_obj)
        sm.add_widget(third_obj)
        sm.add_widget(stroy_market_sup)
        sm.add_widget(stroy_mir_sup)
        sm.add_widget(pesok_service_sup)
        sm.add_widget(scheben_trans_sup)
        sm.add_widget(kirpichny_zavod_sup)
        sm.add_widget(les_hoz_sup)
        sm.add_widget(metizy_sup)
        sm.add_widget(kraski_pro_sup)
        sm.add_widget(stroy_mix_sup)
        sm.add_widget(oboi_dom_sup)

        return sm

if __name__ == '__main__':
    MyApp().run()