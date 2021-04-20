#A basic PySimpleGUI graph example
import PySimpleGUI as sg
import random
import webbrowser

img = r'R0lGODlhQABAAPIAAAAAABkZGRkdHQAAAAoKChglJQD4/gAAACH5BAUKAAAAIf8LTkVUU0NBUEUyLjADAQAAACwOAA4AIwAjAAIDYwi63GouyrmCCTRni7V33CdW1ziG5oem2spS7ivFMljWE42T3W73PoYuCDEFjshksqFsIgGGqHRKhRCg1WwU4HQyu8pUMci8kXlnoTk93LVx71pcNn/VWfdU3rg+7099Z2MfCQAh+QQFCgAAACweAB4AAwADAAIDBihQMKAlAQAh+QQNCgAAACwdAB0ABQAFAAIDCDiwyvtQNTASACH5BAkKAAAALBwAHAAHAAcAAgMLGLCr2izKKR9wNQEAIfkECQoAAAAsHAAcAAcABwACAxIYEKYOZkkByjIRwAaofdHDOAkAIfkECQoAAAAsHAAcAAcABwACAxEYEKYOZklAl4n0qipVfIyTAAAh+QQJCgAAACwcABwABwAHAAIDERgQpgrAwDUhk9C0SvN0W5AAACH5BAkKAAAALBwAHAAHAAcAAgMOCBAW+ua5t0xUdkpI60wAOw=='
TEXT_COLORS = ['white', 'black']
BOX_COLORS = ['red', 'blue', 'green', 'yellow', 'purple', 'orange', 'pink']
BOX_COLORS_TO_TEXT = {
'red':'white', 'green':'white', 'purple':'white', 'blue':'white',
'orange':'black', 'pink':'black', 'yellow':'black'
                     }
BACKGROUND_COLOR = "gainsboro"
URLS = ["https://docs.python.org/3/library/webbrowser.html", "http://www.python.org", "https://stackoverflow.com/questions/4302027/how-to-open-a-url-in-python", "https://codingbat.com/java"]

def color_palette():
    row = [] 
    for color in BOX_COLORS:
        text_color = 'white'
        if color in ('yellow', 'pink', 'orange'):
            text_color = 'black'
        row.append(sg.B('', key=color, size=(5,1), pad=(0,0), button_color=(text_color, color) ))
    return row

def color_identifier_palette():
    row = [] 
    for color in BOX_COLORS:
        text= ''
        if color == 'red':
            text = '▼'
        row.append(sg.T(text, key=f'-TXT-{color}-', size=(6,1), pad=(0,0), background_color=BACKGROUND_COLOR))
    return row

def main():

    sg.theme("Material2")
    gtop = sg.Graph((5000,5000), (0,0),(1800,1800),background_color="white", enable_events=True) #original: (1350,600)
     
    layout = [ 
    [sg.Checkbox('Connect Mode', enable_events=True, key='Connect Mode', background_color=BACKGROUND_COLOR),\
    sg.Button('Connect'), sg.Text('', size=(50,1), background_color=BACKGROUND_COLOR), sg.Button('http://Take Me There', size=(15,2), button_color = ('blue', 'gainsboro'),font="default 15 italic underline"), \
    sg.Text('Colors:', background_color=BACKGROUND_COLOR)] + [sg.Column([color_identifier_palette(), color_palette()], background_color=BACKGROUND_COLOR)],
    # [sg.Input('', key='-IN-', enable_events=True, text_color='black', background_color='black')], 
    
                [sg.Column([[gtop]], size=(1350,600),scrollable=True)],
                [sg.Input('', key='-IN-', enable_events=True, text_color=BACKGROUND_COLOR, background_color=BACKGROUND_COLOR)]
                ]
    window = sg.Window('MIMI', layout, background_color=BACKGROUND_COLOR)
     
    # Write text and lines
    selected_area = (0,0)
    last_selected = (0,0)
    draw_id = None
    point_id = None
    connect = []
    selected = []
    cur_txt_color = 'white'
    cur_box_color = 'red'
    cur_icon = '-TXT-red-' 

    while True:

        event, values = window.read()
        # print("this is the event",event,values)
        if event==sg.WIN_CLOSED:
            break 
            
        if isinstance(event, int):
            window['-IN-'].update("")
            window['-IN-'].Widget.config(insertbackground=BACKGROUND_COLOR) #for the cursor to not be black 
            window['-IN-'].set_focus()
            selected_area = values[event]
            draw_id = None #so that it doesn't delete already written things on canvas
            rect_id = None
            draw_id_text = None

            if values['Connect Mode']:
                if not selected_area in connect:
                    connect.append(selected_area)
                selected.append(gtop.draw_image(data=img, location=(selected_area[0]-10, selected_area[1]+8))) #will always need to tweak this when changing canvas size
                if len(selected) > 2:
                    unused_cursor = selected.pop(0) # updated the selected
                    gtop.delete_figure(unused_cursor)

            
        if event=='-IN-':
            if draw_id and window['-IN-']:
                gtop.delete_figure(draw_id)
                gtop.delete_figure(draw_id_text)
                gtop.delete_figure(rect_id)
           
            draw_id_text = gtop.draw_text(text = f" {values['-IN-'].upper()}{' '}", location =selected_area, color=cur_txt_color, font='Default 13')
            rect_id = gtop.draw_rectangle( gtop.get_bounding_box(draw_id_text)[0], gtop.get_bounding_box(draw_id_text)[1], fill_color=cur_box_color)
            draw_id = gtop.draw_text(text = f" {values['-IN-'].upper()}{' '} ", location =selected_area, color=cur_txt_color, font='Default 13')
            #prevents text from going off screen -- need to do this but for colliding elements
            coordinates = gtop.get_bounding_box(draw_id)
            for coordinate in coordinates:
                x = coordinate[0]
                if x <= 0:
                    gtop.move_figure(draw_id, -x -1, 0)
                    gtop.move_figure(rect_id, -x -1, 0)
                if x>=1800:
                    gtop.move_figure(draw_id, -(x-1800), 0)
                    gtop.move_figure(rect_id, -(x-1800), 0)


        if event=='Connect':
            if len(connect) >= 2:
                line_id = gtop.draw_line(connect[-1], connect[-2], width=2)
                gtop.SendFigureToBack(line_id)
            for cursor in selected: 
                gtop.delete_figure(cursor)
            selected.clear()

        if event in BOX_COLORS:
            # print('here')
            window[cur_icon].update("")
            cur_icon = f'-TXT-{event}-'
            window[cur_icon].update("▼")
            window[cur_box_color].update(disabled=False)
            cur_txt_color = BOX_COLORS_TO_TEXT[event]
            cur_box_color = event
            window[event].update(disabled=True)

        if event=='http://Take Me There':
        	webbrowser.open(random.choice(URLS))
        	window["http://Take Me There"].update(button_color=("purple", "gainsboro") )

     
    window.close()

if __name__ == '__main__':
    main()