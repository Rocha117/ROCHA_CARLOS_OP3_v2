
import investpy
import pandas as pd
import numpy as np
import talib
import mplfinance as mpf


pd.set_option("min_rows", None)
pd.set_option("max_rows", 100)


def extraer(cond, stock_valor, pais, pi="", pf=""):
    """
    Se extraen los datos del precio final diaro del valor 
    """
    if cond == 1:
        # Se extraen los datos del precio final diario del valor en el rango de días dado
        df = investpy.get_stock_historical_data(
            stock_valor, pais, pi, pf)
    else:
        # Se extraen los datos del precio final diario del valor en el último mes del valor
        df = investpy.get_stock_recent_data(
            stock_valor, pais, as_json=False, order='ascending')

    return df


class Indicador_tecnico:
    """
    Permite especificar el indicador tecnico para analizar el activo
    """
    # Aca se usara el paquete talib

    def __init__(self, DataStock, RSI=0, SMA=0):
        self.DataStock = DataStock
        self._RSI = RSI
        self._SMA = SMA

    def RSI(self):
        # Obtener Relative Strength Index (RSI)
        self.DataStock["RSI"] = talib.RSI(
            self.DataStock["Close"], timeperiod=8)
        self._RSI = 1

    def SMA(self):
        # Obtener Simple Moving Average (SMA)
        self.DataStock["SMA"] = talib.SMA(
            self.DataStock["Close"], timeperiod=8)
        self._SMA = 1

    def All(self):
        # Obtener ambos indicadores
        self.DataStock["SMA"] = talib.RSI(
            self.DataStock["Close"], timeperiod=8)
        self.DataStock["RSI"] = talib.SMA(
            self.DataStock["Close"], timeperiod=8)
        self._RSI = 1
        self._SMA = 1


def Grafico(indicadorTec, numSubplots1, numSubplots2, vr=None, pi=None, pf=None):
    """
    Permite hacer la gráfica del activo en un periodo de tiempo
    """

    fig = mpf.figure(figsize=(12, 9))
    s = mpf.make_mpf_style(base_mpf_style='yahoo', y_on_right=False)

    if numSubplots1 == 1 and numSubplots2 == 0:

        ax1 = fig.add_subplot(2, 2, 2, style=s)
        ax11 = ax1.twinx()
        ap = mpf.make_addplot(
            indicadorTec.DataStock['RSI'], ax=ax11, ylabel='RSI')
        vol = fig.add_subplot(2, 2, 4, sharex=ax1, style=s)
        mpf.plot(indicadorTec.DataStock,  volume=vol, ax=ax1,
                 addplot=ap, xrotation=10, ylabel='Precio', type='candle', axtitle='Gráfica de valor con indicador RSI')

    elif numSubplots1 == 0 and numSubplots2 == 1:

        ax2 = fig.add_subplot(2, 2, 2, style=s)
        ax22 = ax2.twinx()
        ap = mpf.make_addplot(
            indicadorTec.DataStock['SMA'], ax=ax22, ylabel='SMA')
        vol = fig.add_subplot(2, 2, 4, sharex=ax2, style=s)
        mpf.plot(indicadorTec.DataStock,  volume=vol, ax=ax2,
                 addplot=ap, xrotation=10, ylabel='Precio', type='candle', axtitle='Gráfica de valor con indicador SMA')

    elif numSubplots1 == 1 and numSubplots2 == 1:

        ax1 = fig.add_subplot(2, 2, 2, style=s)
        ax11 = ax1.twinx()
        ap = mpf.make_addplot(
            indicadorTec.DataStock['RSI'], ax=ax11, ylabel='RSI')

        mpf.plot(indicadorTec.DataStock,   ax=ax1,
                 addplot=ap, xrotation=10, ylabel='Precio', type='candle', axtitle='Gráfica de valor con indicador RSI')

        ax2 = fig.add_subplot(2, 2, 4, style=s)
        ax22 = ax2.twinx()
        ap = mpf.make_addplot(
            indicadorTec.DataStock['SMA'], ax=ax22, ylabel='SMA')

        mpf.plot(indicadorTec.DataStock, ax=ax2,
                 addplot=ap, xrotation=10, ylabel='Precio', type='candle', axtitle='Gráfica de valor con indicador SMA')

    if pi == None and pf == None:
        axp = fig.add_subplot(2, 2, 1, style=s)
        volp = fig.add_subplot(2, 2, 3, sharex=axp, style=s)
        mpf.plot(indicadorTec.DataStock, ax=axp, volume=volp,
                 xrotation=10, ylabel='Precio', type='candle', axtitle='Gráfica del valor (últimos 30 días) ')
        mpf.show()

    else:
        axp = fig.add_subplot(2, 2, 1, style=s)
        volp = fig.add_subplot(2, 2, 3, sharex=axp, style=s)
        mpf.plot(indicadorTec.DataStock, ax=axp, volume=volp,
                 xrotation=10, ylabel='Precio', type='candle', axtitle=f'Gráfica del valor (De {pi} a {pf}) ')
        mpf.show()


class Valor:
    """
    Es la base de datos de los valores guardados 
    """
    # Guarda diferentes valores en un diccionario y muestra los diferentes graficos con los diferentes indicadores tecnicos consultados
    valor = {}

    def __init__(self, valor={}):
        self.valor = valor

    def agregar_valor(self, valo, dfIndicador):
        existe = 0
        for key in self.valor.keys():
            if valo == key:
                existe = 1
                break
            else:
                existe = 0

        if existe == 1:
            global num_exis
            num_exis = 1
            return num_exis
        elif existe == 0:
            self.valor.update({valo: dfIndicador})

    def mostrar_valor(self, v1):
        existe = 0

        for key in self.valor.keys():
            if v1 == key:
                existe = 1
                break
            else:
                existe = 0
        if existe == 1:
            print(f"\n{v1}:\n {self.valor[v1].DataStock}\n")
            return self.valor[v1], self.valor[v1]._RSI, self.valor[v1]._SMA
        elif existe == 0:

            print("\nNo está registrado ese valor en el historial de búsquedas\n")


def señal(indicador, nombre, pais):
    rec = ''
    if indicador == 1:
        data = investpy.technical_indicators(
            name=nombre, country=pais, product_type='stock', interval='daily')
        if data.loc[0, 'signal'] == 'sell':
            rec = 'vender'
        else:
            rec = 'comprar'
        return nombre, data.loc[0, 'value'], rec

    elif indicador == 2:
        data = investpy.moving_averages(
            name=nombre, country=pais, product_type='stock', interval='daily')
        if data.loc[0, 'sma_signal'] == 'sell':
            rec = 'vender'
        else:
            rec = 'comprar'
        return nombre, data.loc[0, 'sma_value'], rec

    elif indicador == 3:
        data = investpy.technical_indicators(
            name=nombre, country=pais, product_type='stock', interval='daily')
        data2 = investpy.moving_averages(
            name=nombre, country=pais, product_type='stock', interval='daily')
        if data.loc[0, 'signal'] == 'sell':
            rec = 'vender'
        else:
            rec = 'comprar'

        if data2.loc[0, 'sma_signal'] == 'sell':
            rec2 = 'vender'
        else:
            rec2 = 'comprar'

        return nombre, data.loc[0, 'value'], rec, data2.loc[0, 'sma_value'], rec2
