"""
options.py

--by tkp

An option analysis program.
PySimpleGUI reference: https://pysimplegui.readthedocs.io/en/latest/


"""

from bisect import bisect_left
from decimal import *
import PySimpleGUI as sg
import requests
from datetime import date
from wallstreet import Stock, Call, Put



# Start of support code
# From: https://stackoverflow.com/questions/12141150/from-list-of-integers-get-number-closest-to-a-given-value
def take_closest(myList, myNumber):
    """
    Assumes myList is sorted. Returns closest value to myNumber.

    If two numbers are equally close, return the smallest number.
    WARNING: bisect_left requires the list to be sorted from LOW to HIGH.
    """
    pos = bisect_left(myList, myNumber)
    if pos == 0 or pos == len(myList):
        return pos
    before = myList[pos - 1]
    after = myList[pos]
    if after - myNumber < myNumber - before:
       return pos - 1
    else:
       return pos


# Start of GUI code
sg.ChangeLookAndFeel('BlueMono') # 'BluePurple', 'DarkAmber','GreenTan'

size_1 = (10,1)
font_h14 = "Helvetica 14"
font_h14b = "Helvetica 14 bold"
def makeHeader(headings):
    header = []
    for heading in headings:
        header.append(sg.Input(heading, 
                    disabled=True,
                    font=font_h14b,
                    #text_color='white', 
                    #background_color='darkblue', 
                    size=size_1, 
                    justification='center')      
        )
    return header


def textElement(keyval, text='00.0', isInput=True):
    if isInput:
        return sg.Input(text, key=keyval, text_color='black', font=font_h14, size=size_1)
        #return sg.Input(text=text, key=keyval, text_color='black', background_color='lightblue', size=size_1)
    return sg.Input(text=text, key=keyval, text_color='black', font=font_h14, size=size_1, disabled=True)
    #return sg.Text(text=text, key=keyval, text_color='black', background_color='lightblue', size=size_1)

def emptyElement(keyval, isInput=False):
    #return sg.Input(key=keyval, font=font_h14, size=size_1, text_color='darkblue', background_color='darkblue', visible=True, disabled=True)
    return sg.Text(key=keyval, font=font_h14, size=size_1, text_color='darkblue', background_color='darkblue', visible=True)
    

# Column layout
head = makeHeader(['Strike','Premium','Target 1', 'Gain 1', 'Target 2', 'Gain 2'])
targets = [emptyElement('r0c1'), emptyElement('r0c2'), textElement('__target1', True), emptyElement('r0c4'), textElement('__target2', True), emptyElement('r0c6')]
column = [targets,
        head,
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
    [sg.Text('Symbol\t', font=font_h14), sg.Input('AAPL', size=(10, 1), key='__symbol',tooltip='Enter the underlying stock symbol', font=font_h14),      
        #sg.Checkbox('Get option chain', key='__chain', default=True, font=font_h14),
        sg.Radio('Calls', "CALL", key='__is_call', default=True, size=(5,1), font=font_h14), sg.Radio('Puts', "CALL", font=font_h14)],
    [sg.Text('Price\t', font=font_h14), sg.Input(key='__price', size=(10, 1), font=font_h14),
        sg.Text('Expires\t', font=font_h14), sg.Input(key='__expdate', size=(10, 1), font=font_h14), sg.CalendarButton('Set date',target=(2,3),format='%Y-%m-%d', font=font_h14)],
    [sg.Text('_'  * 80, font=font_h14)],      
    #[sg.Text('Target 1\t', font=font_h14), sg.Input(key='__target1', size=(10, 1), font=font_h14),
        #sg.Text('Target 2\t', font=font_h14), sg.Input(key='__target2', size=(10, 1), font=font_h14)],
    #[sg.Text('Strike #1\t', font=font_h14), sg.Input(key='__strike_price', size=(10, 1), font=font_h14),
        #sg.Text('Strike inc\t', font=font_h14), sg.Input(key='__strike_price_inc', size=(10, 1), font=font_h14)],
    [sg.Text(' '  * 80, font=font_h14)],
    [sg.Column(column, background_color='darkblue')], #'#d3dfda')],      
    [sg.Text(' '  * 80, font=font_h14)],
    #[sg.Text('Choose a folder', size=(35, 1))],      
    #[sg.Text('Your folder', size=(15, 1), auto_size_text=False, justification='right'),      
    # sg.Input('Default folder'), sg.FolderBrowse()],      
    [sg.Submit('Lookup', font=font_h14), sg.Cancel('Recalc', font=font_h14)]      
]


def get_strikes(price, striks, is_call=True, num_options=6):
    strikes = list(striks) 
    print('get_strikes')
    print(price, is_call, strikes)
    idx = take_closest(strikes, float(price))
    print(idx) #, strikes[idx])
    if not is_call:
        # PUTS
        strikes.reverse()
        idx = len(strikes) - idx
    return strikes[idx:idx+num_options]


window = sg.Window('AppVizo Options Analysis', default_element_size=(40, 1)).Layout(layout)
# Event loop
while True:
    event, values = window.read() 
    print(event, values)       
    num_options = 6  # WARNING: Hard-coded limiter - 6 options
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
        #strike1 = 0 if values['__strike_price'] == '' else Decimal(values['__strike_price'])
        #strike_inc = 0 if values['__strike_price_inc'] == '' else Decimal(values['__strike_price_inc'])
        #if not is_call:
         #   strike_inc *= -1
        errors = False
        if symbol is not None and len(symbol) > 0:
            try:
                s = Stock(symbol)
                window['__price'].update(s.price)
            except requests.exceptions.ConnectionError as ConnectionError:
                window['__price'].update("ERROR")
                errors = True
        # Get strikes and populate.
        # TODO: Wait for the price to update
        if expdate is not None and not errors:
            o = None # This is our option object.
            if is_call:
                o = Call(symbol, d=expdate.day, m=expdate.month, y=expdate.year)
                print("CALLS")
            else:
                o = Put(symbol, d=expdate.day, m=expdate.month, y=expdate.year)
                print("PUTS")
            if len(o.strikes) > 0:
                print("Strikes", o.strikes)
                strikes = get_strikes(price, o.strikes, is_call, num_options)
                for i,strik in enumerate(strikes):
                    strike = Decimal(strik)
                    o.set_strike(strike)
                    row = f'r{i+1}'
                    price = Decimal(o.price)
                    window[row+'c1'].update(o.strike)
                    window[row+'c2'].update(o.price)
                    if target1 > 0:
                        gain = strike - target1 - price
                        if is_call:
                            gain = target1 - strike - price
                        window[row+'c3'].update(f'{gain:.2f}')
                        pctgain = gain * 100 / price
                        window[row+'c4'].update(f'{pctgain:.2f}%')
                    if target2 > 0:
                        gain = strike - target2 - price
                        if is_call:
                            gain = target2 - strike - price
                        window[row+'c5'].update(f'{gain:.2f}')
                        pctgain = gain * 100 / price
                        window[row+'c6'].update(f'{pctgain:.2f}%')
    else:
        # Recalc values
        target1 = 0 if values['__target1'] == '' else Decimal(values['__target1'])
        target2 = 0 if values['__target2'] == '' else Decimal(values['__target2'])
        for i in range(num_options):
            row = f'r{i+1}'
            strike = Decimal(values[row+'c1'])
            price = Decimal(values[row+'c2'])
            if target1 > 0:
                gain = strike - target1 - price
                if is_call:
                    gain = target1 - strike - price
                window[row+'c3'].update(f'{gain:.2f}')
                pctgain = gain * 100 / price
                window[row+'c4'].update(f'{pctgain:.2f}%')
            if target2 > 0:
                gain = strike - target2 - price
                if is_call:
                    gain = target2 - strike - price
                window[row+'c5'].update(f'{gain:.2f}')
                pctgain = gain * 100 / price
                window[row+'c6'].update(f'{pctgain:.2f}%')

window.close()

    # for strike in args.strike:
    #     o = Call(symbol, d=24, m=1, y=2020, strike=strike)
    #     print(symbol, o.price, o.strike)

# See: https://pysimplegui.trinket.io/demo-programs#/tables/simulated-tables

# layout =  [[sg.Text('My To Do List', font='Helvetica 15')]]  # a title line t
# layout += [[sg.Text(f'{i}. '), sg.CBox(''), sg.Input()] for i in range(1, 6)]  # the checkboxes and descriptions
# layout += [[sg.Button('Save'), sg.Button('Load'), sg.Button('Exit')]]  # the buttons