import PySimpleGUI as sg
# sudo pip3 install pyserial
# /home/bruce/.local/lib/python3.5
# sudo python3.5 keypad3.py
import serial
# oen microcontroller serial port
ser = serial.Serial('/dev/ttyUSB0', 38400)  # open serial port

# run suing python3.5 test_pysimpleGUI.py

#sg.theme('DarkAmber')   # Add a touch of color
# All the stuff inside your window.
font_spec = 'Courier 24 bold'
layout = [  [sg.Text('Keypad', font='Helvetica 9')],
            [sg.RealtimeButton('1', key='key01', font=font_spec),
             sg.RealtimeButton('2', key='key02', font=font_spec),
             sg.RealtimeButton('3', key='key03', font=font_spec)],
            [sg.RealtimeButton('4', key='key04', font=font_spec),
             sg.RealtimeButton('5', key='key05', font=font_spec),
             sg.RealtimeButton('6', key='key06', font=font_spec)],           
            [sg.RealtimeButton('7', key='key07', font=font_spec),
             sg.RealtimeButton('8', key='key08', font=font_spec),
             sg.RealtimeButton('9', key='key09', font=font_spec)],
            [sg.RealtimeButton('*', key='key10', font=font_spec),
             sg.RealtimeButton('0', key='key00', font=font_spec),
             sg.RealtimeButton('#', key='key11', font=font_spec)],       
             [sg.Text('Pushbuttons & toggle switches')],
            [sg.RealtimeButton('P1', key='pushbut1', font='Helvetica 12'),
             sg.RealtimeButton('P2', key='pushbut2', font='Helvetica 12'),
             sg.Checkbox('T1', key='toggle1', font='Helvetica 12',enable_events=True),
             sg.Checkbox('T2', key='toggle2', font='Helvetica 12',enable_events=True)],
            [sg.Text('Potentiometer')],
            [sg.Slider(range=(0,100), default_value=50, size=(22,15), key='slider1',
             orientation='horizontal', font=('Helvetica', 12),enable_events=True)],
            [sg.Text('System Controls')],
            [sg.Button('Exit', font='Helvetica 8')],
            [sg.Button('RESET target', key='rtg', font='Helvetica 8'),
             sg.Checkbox('reset_en', key='r_en',
                        font='Helvetica 8', enable_events=True),
             sg.Button('RESET control', key='rst', font='Helvetica 8')
            ]
         ]

sg.SetOptions(background_color='#9FB8AD',
       text_element_background_color='#9FB8AD',
       element_background_color='#475841',#'#9FB8AD',
       scrollbar_color=None,
       input_elements_background_color='#9FB8AD',#'#F7F3EC',
       progress_meter_color = ('green', 'blue'),
       button_color=('white','#475841'),
       )

# Create the Window
window = sg.Window('ECE47xx Interface', layout, location=(0,0),
                    element_justification='c', finalize=True)

# <ButtonRelease-1>
window['key01'].bind('<ButtonRelease-1>', 'r')
window['key02'].bind('<ButtonRelease-1>', 'r')
window['key00'].bind('<ButtonRelease-1>', 'r')
window['key03'].bind('<ButtonRelease-1>', 'r')
window['key04'].bind('<ButtonRelease-1>', 'r')
window['key05'].bind('<ButtonRelease-1>', 'r')
window['key06'].bind('<ButtonRelease-1>', 'r')
window['key07'].bind('<ButtonRelease-1>', 'r')
window['key08'].bind('<ButtonRelease-1>', 'r')
window['key09'].bind('<ButtonRelease-1>', 'r')
window['key10'].bind('<ButtonRelease-1>', 'r')
window['key11'].bind('<ButtonRelease-1>', 'r')
window['pushbut1'].bind('<ButtonRelease-1>', 'r')
window['pushbut2'].bind('<ButtonRelease-1>', 'r')

# Event Loop to process "events"
event = 0
switch_state = [0, 0, 0]

#
key_on = 0
key_which = '0'
button_on = 0
button_which = '0'
#
while True:
    # time out paramenter makes the system non-blocking
    # If there is no event in 50 mSec the call returns '__TIMEOUT__'
    event, values = window.read() # timeout=50
    #
    #print(event)
    # if user closes window using windows 'x' or clicks 'Exit'   
    if event == sg.WIN_CLOSED or event == 'Exit': #
        break
    # read out the toggle switches
    switch_state[1] = window.Element('toggle1').get()
    switch_state[2] = window.Element('toggle2').get()
    switch_state[0] = window.Element('r_en').get()

    # keypad events
    #if event == 'key01r': is the release event for key01
    if event[0:3]  == 'key' and key_on == 0 :
       #print('k' + event[3:5] + '1' )
       ser.write(('k' + event[3:5] + '1').encode())
       key_on = 1
       key_which = event[3:5]
    elif  (key_on == 1 and event[3:6] == key_which+'r') :
       #print('k' + key_which + '0' )
       ser.write(('k' + key_which + '0').encode())
       key_on = 0
       key_which = ' '
    # pushbutton events
    if event[0:3]  == 'pus' and button_on == 0 :
       #print('b0' + event[7] + '1' )
       ser.write(('b0' + event[7] + '1').encode())
       button_on = 1
       button_which = event[7]
    elif (button_on == 1 and event[7:9] == button_which +'r') :
       #print('b0' + button_which + '0' )
       ser.write(('b0'  + button_which + '0').encode())
       button_on = 0
       button_which = ' '
    # toggle switches
    if event[0:3]  == 'tog'  :
       #print switch number and state
       #print('t0' + event[6] + str(switch_state[int(event[6])]) )
       ser.write(('t0' + event[6] + str(switch_state[int(event[6])])).encode())
    # silder events
    if event[0:3]  == 'sli'  :
       #print slider value
       #print('s' + "{:03d}".format(int(values['slider1'])))
       ser.write(('s' + "{:03d}".format(int(values['slider1']))).encode())
    if event[0:3] == 'rst' and switch_state[0] == 1 :
       ser.write('r00a'.encode())
    if event[0:3] == 'rtg' and switch_state[0] == 1 :
       ser.write('r00b'.encode())

# Bail out
ser.close()             # close port
window.close()
import PySimpleGUI as sg
# sudo pip3 install pyserial
# /home/bruce/.local/lib/python3.5
# sudo python3.5 keypad3.py
import serial
# oen microcontroller serial port
ser = serial.Serial('/dev/ttyUSB0', 38400)  # open serial port

# run suing python3.5 test_pysimpleGUI.py

#sg.theme('DarkAmber')   # Add a touch of color
# All the stuff inside your window.
font_spec = 'Courier 24 bold'
layout = [  [sg.Text('Keypad', font='Helvetica 9')],
            [sg.RealtimeButton('1', key='key01', font=font_spec),
             sg.RealtimeButton('2', key='key02', font=font_spec),
             sg.RealtimeButton('3', key='key03', font=font_spec)],
            [sg.RealtimeButton('4', key='key04', font=font_spec),
             sg.RealtimeButton('5', key='key05', font=font_spec),
             sg.RealtimeButton('6', key='key06', font=font_spec)],           
            [sg.RealtimeButton('7', key='key07', font=font_spec),
             sg.RealtimeButton('8', key='key08', font=font_spec),
             sg.RealtimeButton('9', key='key09', font=font_spec)],
            [sg.RealtimeButton('*', key='key10', font=font_spec),
             sg.RealtimeButton('0', key='key00', font=font_spec),
             sg.RealtimeButton('#', key='key11', font=font_spec)],       
             [sg.Text('Pushbuttons & toggle switches')],
            [sg.RealtimeButton('P1', key='pushbut1', font='Helvetica 12'),
             sg.RealtimeButton('P2', key='pushbut2', font='Helvetica 12'),
             sg.Checkbox('T1', key='toggle1', font='Helvetica 12',enable_events=True),
             sg.Checkbox('T2', key='toggle2', font='Helvetica 12',enable_events=True)],
            [sg.Text('Potentiometer')],
            [sg.Slider(range=(0,100), default_value=50, size=(22,15), key='slider1',
             orientation='horizontal', font=('Helvetica', 12),enable_events=True)],
            [sg.Text('System Controls')],
            [sg.Button('Exit', font='Helvetica 8')],
            [sg.Button('RESET target', key='rtg', font='Helvetica 8'),
             sg.Checkbox('reset_en', key='r_en',
                        font='Helvetica 8', enable_events=True),
             sg.Button('RESET control', key='rst', font='Helvetica 8')
            ]
         ]

sg.SetOptions(background_color='#9FB8AD',
       text_element_background_color='#9FB8AD',
       element_background_color='#475841',#'#9FB8AD',
       scrollbar_color=None,
       input_elements_background_color='#9FB8AD',#'#F7F3EC',
       progress_meter_color = ('green', 'blue'),
       button_color=('white','#475841'),
       )

# Create the Window
window = sg.Window('ECE47xx Interface', layout, location=(0,0),
                    element_justification='c', finalize=True)

# <ButtonRelease-1>
window['key01'].bind('<ButtonRelease-1>', 'r')
window['key02'].bind('<ButtonRelease-1>', 'r')
window['key00'].bind('<ButtonRelease-1>', 'r')
window['key03'].bind('<ButtonRelease-1>', 'r')
window['key04'].bind('<ButtonRelease-1>', 'r')
window['key05'].bind('<ButtonRelease-1>', 'r')
window['key06'].bind('<ButtonRelease-1>', 'r')
window['key07'].bind('<ButtonRelease-1>', 'r')
window['key08'].bind('<ButtonRelease-1>', 'r')
window['key09'].bind('<ButtonRelease-1>', 'r')
window['key10'].bind('<ButtonRelease-1>', 'r')
window['key11'].bind('<ButtonRelease-1>', 'r')
window['pushbut1'].bind('<ButtonRelease-1>', 'r')
window['pushbut2'].bind('<ButtonRelease-1>', 'r')

# Event Loop to process "events"
event = 0
switch_state = [0, 0, 0]

#
key_on = 0
key_which = '0'
button_on = 0
button_which = '0'
#
while True:
    # time out paramenter makes the system non-blocking
    # If there is no event in 50 mSec the call returns '__TIMEOUT__'
    event, values = window.read() # timeout=50
    #
    #print(event)
    # if user closes window using windows 'x' or clicks 'Exit'   
    if event == sg.WIN_CLOSED or event == 'Exit': #
        break
    # read out the toggle switches
    switch_state[1] = window.Element('toggle1').get()
    switch_state[2] = window.Element('toggle2').get()
    switch_state[0] = window.Element('r_en').get()

    # keypad events
    #if event == 'key01r': is the release event for key01
    if event[0:3]  == 'key' and key_on == 0 :
       #print('k' + event[3:5] + '1' )
       ser.write(('k' + event[3:5] + '1').encode())
       key_on = 1
       key_which = event[3:5]
    elif  (key_on == 1 and event[3:6] == key_which+'r') :
       #print('k' + key_which + '0' )
       ser.write(('k' + key_which + '0').encode())
       key_on = 0
       key_which = ' '
    # pushbutton events
    if event[0:3]  == 'pus' and button_on == 0 :
       #print('b0' + event[7] + '1' )
       ser.write(('b0' + event[7] + '1').encode())
       button_on = 1
       button_which = event[7]
    elif (button_on == 1 and event[7:9] == button_which +'r') :
       #print('b0' + button_which + '0' )
       ser.write(('b0'  + button_which + '0').encode())
       button_on = 0
       button_which = ' '
    # toggle switches
    if event[0:3]  == 'tog'  :
       #print switch number and state
       #print('t0' + event[6] + str(switch_state[int(event[6])]) )
       ser.write(('t0' + event[6] + str(switch_state[int(event[6])])).encode())
    # silder events
    if event[0:3]  == 'sli'  :
       #print slider value
       #print('s' + "{:03d}".format(int(values['slider1'])))
       ser.write(('s' + "{:03d}".format(int(values['slider1']))).encode())
    if event[0:3] == 'rst' and switch_state[0] == 1 :
       ser.write('r00a'.encode())
    if event[0:3] == 'rtg' and switch_state[0] == 1 :
       ser.write('r00b'.encode())

# Bail out
ser.close()             # close port
window.close()