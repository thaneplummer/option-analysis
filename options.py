"""
options.py

--by tkp

An option analysis program.


"""


from decimal import *
import PySimpleGUI as sg
from datetime import date
from wallstreet import Stock, Call, Put



sg.ChangeLookAndFeel('BlueMono') # 'BluePurple', 'DarkAmber','GreenTan'


size_1 = (10,1)
def makeHeader(headings):
    header = []
    for heading in headings:
        header.append(sg.Text(heading, 
                    text_color='white', 
                    background_color='darkblue', 
                    size=size_1, 
                    justification='center')      
        )
    return header


def textElement(keyval, text='00.0', isInput=True):
    if isInput:
        return sg.Input(text, key=keyval, text_color='black', size=size_1)
        #return sg.Input(text=text, key=keyval, text_color='black', background_color='lightblue', size=size_1)
    return sg.Text(text=text, key=keyval, text_color='black', size=size_1)
    #return sg.Text(text=text, key=keyval, text_color='black', background_color='lightblue', size=size_1)


# Column layout
head = makeHeader(['Strike','Premium','Target 1', 'Gain 1', 'Target 2', 'Gain 2'])
column = [head,
        [textElement('r1c1'), textElement('r1c2'), textElement('r1c3'), textElement('r1c4'), textElement('r1c5'), textElement('r1c6')],
        [textElement('r2c1'), textElement('r2c2'), textElement('r2c3'), textElement('r2c4'), textElement('r2c5'), textElement('r2c6')],
        [textElement('r3c1'), textElement('r3c2'), textElement('r3c3'), textElement('r3c4'), textElement('r3c5'), textElement('r3c6')],
        [textElement('r4c1'), textElement('r4c2'), textElement('r4c3'), textElement('r4c4'), textElement('r4c5'), textElement('r4c6')],
        [textElement('r5c1'), textElement('r5c2'), textElement('r5c3'), textElement('r5c4'), textElement('r5c5'), textElement('r5c6')],
        [textElement('r6c1'), textElement('r6c2'), textElement('r6c3'), textElement('r6c4'), textElement('r6c5'), textElement('r6c6')],
        [sg.Text('_' * 80, background_color='darkblue')]
]

# Window layout
layout = [      
    [sg.Text('Option Analyser', size=(30, 1), font=("Helvetica", 25))],      
    [sg.Text('Symbol\t'), sg.Input('AAPL', size=(10, 1), key='__symbol',tooltip='Enter the underlying stock symbol'),      
        sg.Checkbox('Get option chain', key='__chain', default=True),
        sg.Radio('Calls', "CALL", key='__is_call', default=True, size=(5,1)), sg.Radio('Puts', "CALL")],
    #[sg.Radio(text, 1) for text in ('Call','Put')],
    [sg.Text('Price\t'), sg.Input(key='__price', size=(10, 1)),
        sg.Text('Expires\t'), sg.Input(key='__expdate', size=(10, 1)), sg.CalendarButton('Set date',target=(2,3),format='%Y-%m-%d')],
    [sg.Text('_'  * 80)],      
    [sg.Text('Target 1\t'), sg.Input(key='__target1', size=(10, 1)),
        sg.Text('Target 2\t'), sg.Input(key='__target2', size=(10, 1))],
    [sg.Text('Strike #1\t'), sg.Input(key='__strike_price', size=(10, 1)),
        sg.Text('Strike inc\t'), sg.Input(key='__strike_price_inc', size=(10, 1))],
    #[sg.Text('Put strike\t'), sg.Input(key='__put_strike', size=(10, 1)),
    #    sg.Text('Put decrement\t'), sg.Input(key='__put_strike_dec', size=(10, 1))],
    [sg.Text(' '  * 80)],
    [sg.Column(column, background_color='darkblue')], #'#d3dfda')],      
    [sg.Text(' '  * 80)],
    #[sg.Text('Choose a folder', size=(35, 1))],      
    #[sg.Text('Your folder', size=(15, 1), auto_size_text=False, justification='right'),      
    # sg.Input('Default folder'), sg.FolderBrowse()],      
    [sg.Submit('Lookup'), sg.Cancel('Recalc')]      
]


# TODO: Calculate for Puts
def get_strikes(price, strikes):
    start = 0
    numoptions = 6
    for i, strike in enumerate(strikes):
        eps = Decimal(strike) - price
        if eps > 0:
            start = i
            break
    end = start + numoptions
    return strikes[start:end]


window = sg.Window('AppVizo Options Analysis', default_element_size=(40, 1)).Layout(layout)
# Event loop
while True:
    event, values = window.read() 
    print(event, values)       
    numoptions = 6
    if event in (None, 'Exit'):      
        # Confirm exit here if desired.
        break      
    elif event == 'Lookup':
        #sg.Popup(event, values)        # Debug
        symbol = values['__symbol']
        price = 0 if values['__price'] == '' else Decimal(values['__price'])
        is_call = values['__is_call']
        expdate = None if values['__expdate'] == '' else date.fromisoformat(values['__expdate'])
        target1 = 0 if values['__target1'] == '' else Decimal(values['__target1'])
        target2 = 0 if values['__target2'] == '' else Decimal(values['__target2'])
        strike = 0 if values['__strike_price'] == '' else Decimal(values['__strike_price'])
        strike_inc = 0 if values['__strike_price_inc'] == '' else Decimal(values['__strike_price_inc'])
        if not is_call:
            strike_inc *= -1
        if symbol is not None and len(symbol) > 0:
            s = Stock(symbol)
            window['__price'].update(s.price)
        # Get strikes and populate.
        if expdate is not None:
            o = None # This is our option object.
            if is_call:
                o = Call(symbol, d=expdate.day, m=expdate.month, y=expdate.year)
            else:
                o = Put(symbol, d=expdate.day, m=expdate.month, y=expdate.year)
            if len(o.strikes) > 0:
                strikes = get_strikes(price, o.strikes)
                for i,strik in enumerate(strikes[0:numoptions]):     # WARNING: Hard-coded limiter - 6 options
                    strike = Decimal(strik)
                    o.set_strike(strike)
                    row = f'r{i+1}'
                    window[row+'c1'].update(o.strike)
                    window[row+'c2'].update(o.price)
                    if target1 > 0:
                        window[row+'c3'].update(target1)
                        pctgain = (target1 - strike - Decimal(o.price)) * 100 / Decimal(o.price)
                        window[row+'c4'].update(f'{pctgain:.2f}%')
                    if target2 > 0:
                        window[row+'c5'].update(target2)
                        pctgain = (target2 - strike - Decimal(o.price)) * 100 / Decimal(o.price)
                        window[row+'c6'].update(f'{pctgain:.2f}%')
    else:
        # Recalc values
        for i in range(numoptions):
            row = f'r{i+1}'
            strike = Decimal(values[row+'c1'])
            price = Decimal(values[row+'c2'])
            target1 = Decimal(values[row+'c3'])
            if target1 > 0:
                pctgain = (target1 - strike - price) * 100 / price
                window[row+'c4'].update(f'{pctgain:.2f}%')
            target2 = Decimal(values[row+'c5'])
            if target2 > 0:
                pctgain = (target2 - strike - price) * 100 / price
                window[row+'c6'].update(f'{pctgain:.2f}%')

window.close()

    # for strike in args.strike:
    #     o = Call(symbol, d=24, m=1, y=2020, strike=strike)
    #     print(symbol, o.price, o.strike)

# See: https://pysimplegui.trinket.io/demo-programs#/tables/simulated-tables

# layout =  [[sg.Text('My To Do List', font='Helvetica 15')]]  # a title line t
# layout += [[sg.Text(f'{i}. '), sg.CBox(''), sg.Input()] for i in range(1, 6)]  # the checkboxes and descriptions
# layout += [[sg.Button('Save'), sg.Button('Load'), sg.Button('Exit')]]  # the buttons