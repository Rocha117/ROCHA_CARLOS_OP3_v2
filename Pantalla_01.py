from kivy.app import App
from kivy.uix.screenmanager import ScreenManager, Screen
import psycopg2
from kivy.uix.screenmanager import SlideTransition
from kivy.properties import NumericProperty, StringProperty, ListProperty, ObjectProperty, BooleanProperty
from kivy.lang import Builder
from kivy.core.window import Window
from kivy.clock import Clock
import random
import Comandos
import CommInversiones
from kivy.uix.label import Label
import sys
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.scrollview import ScrollView
import investpy
import mplfinance as mpf
import pandas as pd
from datepicker import DatePicker
from kivy.core.window import Window
from sqlalchemy import create_engine


def consStock(df):
    Row_list = []
    for index, rows in df.iterrows():
        my_list = rows.symbol
        Row_list.append(my_list)
    return Row_list


valorSP = investpy.get_stock_countries()
stockgen = investpy.get_stocks(country="peru")

stockSP = consStock(stockgen)

spinSP = []
paisV = ""
stockV = ""
HastaV = ""
DesdeV = ""
t = ""

pd.set_option("min_rows", 100)
pd.set_option("max_rows", 200)


class Pantalla1Window(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    def Crear_tabla():
        conn = None
        sql = """CREATE TABLE  jugador (
        nombre_jugador VARCHAR NOT NULL,
        puntaje_jugador INT NOT NULL)"""

        try:
            conn = psycopg2.connect(host="localhost",
                                    database="lab07",
                                    user="postgres",
                                    password="a",
                                    port="5432")
            cur = conn.cursor()
            cur.execute(sql)
            conn.commit()
            conn.commit()
            cur.close()
        except (Exception, psycopg2.DatabaseError) as error:
            print(error)
        finally:
            if conn is not None:
                conn.close()
    Crear_tabla()

    def submit(self, nombre_jugador, puntaje_jugador):
        sql = """ INSERT INTO jugador (nombre_jugador, puntaje_jugador) VALUES (%s, %s);"""
        conn = None
        try:
            conn = psycopg2.connect(
                host="localhost",
                database="lab07",
                user="postgres",
                password="a",
                port="5432")
            cur = conn.cursor()

            # modificar puntuaciones
            cur.execute(sql, (nombre_jugador, puntaje_jugador))

            conn.commit()
            cur.close()
            if conn is not None:
                conn.close()

            print("todo bien")
        except (Exception, psycopg2.DatabaseError) as e:
            print(e, "** ERROR!!!!")
        finally:
            if conn is not None:
                conn.close()

    # def datos_base(self):
    #     nomb = self.ids.NombreI.text
    #     puntaje = str(100)
    #     self.submit(nomb, puntaje)

    def next1(self, *args):

        self.manager.transition = SlideTransition(direction="left")
        self.manager.current = self.manager.next()
        App.get_running_app().root.current = "pantalla02"

    def next3(self, *args):

        self.manager.transition = SlideTransition(direction="left")
        self.manager.current = self.manager.next()
        App.get_running_app().root.current = "pantalla04"


class Pantalla02(Screen):

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    def next1(self):
        self.manager.transition = SlideTransition(direction="left")
        self.manager.current = self.manager.next()
        App.get_running_app().root.current = "pantalla1"

    def next2(self):
        self.manager.transition = SlideTransition(direction="left")
        self.manager.current = self.manager.next()
        App.get_running_app().root.current = "pantalla05"


class ContenedorBotones(BoxLayout):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        Clock.schedule_once(self.generar_botones)

    def generar_botones(self, *args):
        lt = self.letras()

        for ele in lt:
            b = Lab()
            b.id_boton = ele
            self.add_widget(b)

    def letras(self, *args):
        df = CommInversiones.extraer(2, "gra", "peru")
        # Create an empty list
        Row_list = []

        for i in investpy.get_stock_countries():
            Row_list.append(
                "País     " + str(investpy.get_stock_countries().index(i)+1)+"    :     "+str(i))
        return Row_list


class Lab(Label):
    id_boton = StringProperty(None)


class Pantalla04(Screen):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def pasear(self, value, *args):

        # print(App.get_running_app().root.get_screen('botones').ids)
        self.ids.contenedor.clear_widgets()
        self.ids.contenedor.letras(value)
        paisV = value

    def next1(self):
        self.manager.transition = SlideTransition(direction="left")
        self.manager.current = self.manager.next()
        App.get_running_app().root.current = "pantalla1"

    def next2(self):
        self.manager.transition = SlideTransition(direction="left")
        self.manager.current = self.manager.next()
        App.get_running_app().root.current = "pantalla05"


class ContenedorBotones04(BoxLayout):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def generar_botones(self, lt, *args):

        for ele in lt:
            b = Lab04()
            b.id_boton = ele
            self.add_widget(b)

    def letras(self, value, *args):
        df = investpy.get_stocks(country=value)
        # Create an empty list

        Row_list = []
        df.rename(columns={'name': '_name',
                           'isin': '_isin'},
                  inplace=True)
        # Iterate over each row
        for index, rows in df.iterrows():
            # Create list for the current row
            my_list = [rows.country, rows._name, rows.full_name,
                       rows._isin, rows.currency, rows.symbol]

            # append the list to the final list
            Row_list.append(my_list)

        # Print the list

        aux = []

        for i in Row_list:
            for j in i:
                entero = str(j)
                aux.append(entero)

        aux2 = []
        for i in range(len(aux)//6):

            aux2.append(aux[6*i:6*i+6])
        lt = []
        for i in aux2:
            l1 = '               '.join(i)
            lt.append(l1)

        self.generar_botones(lt)


class Lab04(Label):
    id_boton = StringProperty(None)


class Pantalla05(Screen):
    def next1(self, *args):

        self.manager.transition = SlideTransition(direction="left")
        self.manager.current = self.manager.next()
        App.get_running_app().root.current = "pantalla06"

    def next2(self, *args):
        sys.exit()


class Pantalla06(Screen):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def show_calendar1(self):
        datePicker = CustomDatePicker()
        datePicker.show_popup(1, .3)

    def consStock(self, df):
        for index, rows in df.iterrows():
            my_list = [rows.symbol]
            my_list.append(my_list)

    def show_calendar2(self):
        datePicker = CustomDatePicker2()
        datePicker.show_popup(1, .3)

    def pasear(self, value, *args):
        global paisV
        paisV = value

    def cambiar(self, value, *args):
        stockgen = investpy.get_stocks(country=str(value))
        App.get_running_app().root.get_screen(
            "pantalla06").ids.spinner_id2.values = consStock(stockgen)

    def pasear2(self, value, *args):
        global stockV
        stockV = value

    def paisB(self):

        df = CommInversiones.extraer(1, stockV, paisV, DesdeV, HastaV)

        mpf.plot(df, axtitle=f'Gráfica del valor (De {DesdeV} a {HastaV})', style='yahoo',
                 xrotation=15, type='candle')
        mpf.show()

    def next1(self, *args):

        self.manager.transition = SlideTransition(direction="left")
        self.manager.current = self.manager.next()
        App.get_running_app().root.current = "pantalla07"

    def go(self):
        self.paisB()
        self.next1()


class CustomDatePicker(DatePicker):

    def update_value(self,  inst):
        """ Update textinput value on popup close """

        self.text = "%s/%s/%s" % tuple(self.cal.active_date)
        self.focus = False
        App.get_running_app().root.get_screen("pantalla06").ids.ti1.text = self.text
        global DesdeV
        DesdeV = str(self.text)


class CustomDatePicker2(DatePicker):

    def update_value(self, inst):
        """ Update textinput value on popup close """

        self.text = "%s/%s/%s" % tuple(self.cal.active_date)
        self.focus = False
        App.get_running_app().root.get_screen("pantalla06").ids.ti2.text = self.text
        global HastaV
        HastaV = str(self.text)


class Pantalla07(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    def globales(self):
        global stockV
        global paisV
        global DesdeV
        global HastaV
        df = CommInversiones.extraer(1, stockV, paisV, DesdeV, HastaV)
        return df

    def graficoRSI(self):
        global t
        t = "RSI"
        df = self.globales()
        indic1 = CommInversiones.Indicador_tecnico(df)
        indic1.RSI()

        CommInversiones.Grafico(indic1, indic1._RSI, indic1._SMA)
        señ1 = CommInversiones.señal(1, stockV, paisV)
        App.get_running_app().root.get_screen(
            'pantalla08').ids.P8Lab1.text = f"El indicador {t} en el valor búrsatil '{señ1[0]}'\n es de {señ1[1]}, e indica\n que se recomienda {señ1[2]}."

    def graficoSMA(self):
        global t
        t = "SMA"
        df = self.globales()
        indic1 = CommInversiones.Indicador_tecnico(df)
        indic1.SMA()

        CommInversiones.Grafico(indic1, indic1._RSI, indic1._SMA)
        señ1 = CommInversiones.señal(2, stockV, paisV)
        App.get_running_app().root.get_screen(
            'pantalla08').ids.P8Lab1.text = f"El indicador {t} en el valor búrsatil '{señ1[0]}'\n es de {señ1[1]}, e indica\n que se recomienda {señ1[2]}."

    def graficoAMBOS(self):
        global t
        t = "ALL"
        df = self.globales()
        indic1 = CommInversiones.Indicador_tecnico(df)
        indic1.All()

        CommInversiones.Grafico(indic1, indic1._RSI, indic1._SMA)
        señ1 = CommInversiones.señal(3, stockV, paisV)
        App.get_running_app().root.get_screen(
            'pantalla08').ids.P8Lab1.text = f"Con el valor búrsatil '{señ1[0]}', con el indicador RSI,\n el cual es de {señ1[1]}, recomienda {señ1[2]};\n mientras que el indicador SMA, el cual es de {señ1[3]},\n recomienda {señ1[4]}."

    def next(self, *args):
        self.manager.transition = SlideTransition(direction="left")
        self.manager.current = self.manager.next()
        App.get_running_app().root.current = "pantalla08"


class Pantalla08(Screen):
    def globales(self):
        global stockV
        global paisV
        global DesdeV
        global HastaV
        df = CommInversiones.extraer(1, stockV, paisV, DesdeV, HastaV)
        return df

    def conexion(self, *args):
        df = self.globales()
        engine = create_engine(
            'postgresql://postgres:a@localhost:5432/Examen_2')
        df.to_sql('examen_02', engine)

    def next1(self, *args):
        self.manager.transition = SlideTransition(direction="left")
        self.manager.current = self.manager.next()
        App.get_running_app().root.current = "pantalla07"

    def next2(self, *args):
        self.manager.transition = SlideTransition(direction="left")
        self.manager.current = self.manager.next()
        self.conexion()
        App.get_running_app().root.current = "pantalla09"


class Pantalla09(Screen):
    def globales(self):
        global stockV
        global paisV
        global DesdeV
        global HastaV
        df = CommInversiones.extraer(1, stockV, paisV, DesdeV, HastaV)
        return df

    def next1(self, *args):
        self.manager.transition = SlideTransition(direction="left")
        self.manager.current = self.manager.next()
        App.get_running_app().root.current = "pantalla10"

    def next2(self, *args):
        self.manager.transition = SlideTransition(direction="left")
        self.manager.current = self.manager.next()
        App.get_running_app().root.current = "pantalla12"

    def conexion(self, *args):
        df = self.globales()
        engine = create_engine(
            'postgresql://postgres:a@localhost:5432/Examen_2')
        df.to_sql('examen_02', engine)


class Pantalla10(Screen):
    def abrirSimbReg(self):
        pass

    def retrieve(self, *args):
        alchemyEngine = create_engine(
            'postgresql://postgres:a@localhost:5432/Examen_2')

        dbConnection = alchemyEngine.connect()

        dataFrame = pd.read_sql("select * from \"examen_02\"", dbConnection)

        pd.set_option('display.expand_frame_repr', False)

        dbConnection.close()
        return dataFrame

    def pasear(self, value, *args):
        global spinSP
        global stockV
        spinSP = self.retrieve()
        self.ids.spinner_id3.values = [stockV]

    def next1(self, *args):
        self.manager.transition = SlideTransition(direction="left")
        self.manager.current = self.manager.next()
        App.get_running_app().root.current = "pantalla11"

        indic1 = CommInversiones.Indicador_tecnico(df)
        indic1.All()
        CommInversiones.Grafico(indic1, indic1._RSI, indic1._SMA)


class Pantalla11(Screen):
    def next1(self, *args):
        self.manager.transition = SlideTransition(direction="left")
        self.manager.current = self.manager.next()
        App.get_running_app().root.current = "pantalla10"

    def next2(self, *args):
        self.manager.transition = SlideTransition(direction="left")
        self.manager.current = self.manager.next()
        App.get_running_app().root.current = "pantalla12"


class Pantalla12(Screen):
    def next1(self, *args):

        self.manager.transition = SlideTransition(direction="left")
        self.manager.current = self.manager.next()
        App.get_running_app().root.current = "pantalla10"

    def next2(self, *args):
        sys.exit()


class MyScreenManager(ScreenManager):
    pais = StringProperty()
    codigo = StringProperty()
    rangoT = BooleanProperty()
    desdeT = StringProperty()
    hastaT = StringProperty()


kv = Builder.load_file("pantalla_01.kv")


class pantalla_01App(App):
    title = "Screen Manager"
    screen_manager = ObjectProperty()

    def build(self):
        self.screen_manager = MyScreenManager()
        return kv


if __name__ == '__main__':
    pantalla_01App().run()
