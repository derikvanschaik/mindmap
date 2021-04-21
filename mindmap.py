#A basic PySimpleGUI graph example
import PySimpleGUI as sg
import random
import webbrowser
#This is the new line i added while checking out branch new

img = r'R0lGODlhQABAAPIAAAAAABkZGRkdHQAAAAoKChglJQD4/gAAACH5BAUKAAAAIf8LTkVUU0NBUEUyLjADAQAAACwOAA4AIwAjAAIDYwi63GouyrmCCTRni7V33CdW1ziG5oem2spS7ivFMljWE42T3W73PoYuCDEFjshksqFsIgGGqHRKhRCg1WwU4HQyu8pUMci8kXlnoTk93LVx71pcNn/VWfdU3rg+7099Z2MfCQAh+QQFCgAAACweAB4AAwADAAIDBihQMKAlAQAh+QQNCgAAACwdAB0ABQAFAAIDCDiwyvtQNTASACH5BAkKAAAALBwAHAAHAAcAAgMLGLCr2izKKR9wNQEAIfkECQoAAAAsHAAcAAcABwACAxIYEKYOZkkByjIRwAaofdHDOAkAIfkECQoAAAAsHAAcAAcABwACAxEYEKYOZklAl4n0qipVfIyTAAAh+QQJCgAAACwcABwABwAHAAIDERgQpgrAwDUhk9C0SvN0W5AAACH5BAkKAAAALBwAHAAHAAcAAgMOCBAW+ua5t0xUdkpI60wAOw=='
TEXT_COLORS = ['white', 'black']
BOX_COLORS = ['red', 'blue', 'green', 'yellow', 'purple', 'orange', 'pink']
BOX_COLORS_TO_TEXT = {
'red':'white', 'green':'white', 'purple':'white', 'blue':'white',
'orange':'black', 'pink':'black', 'yellow':'black'
                     }
MAX_X, MAX_Y = 1800, 1800 
BACKGROUND_COLOR = "gainsboro"
URLS = ["https://docs.python.org/3/library/webbrowser.html", "http://www.python.org", "https://stackoverflow.com/questions/4302027/how-to-open-a-url-in-python", "https://codingbat.com/java"]

def colored_button(color, text_color):
    return sg.B('', key=color, size=(5,1), pad=(0,0), button_color=(text_color, color) )

def color_palette():
    black = ('yellow', 'pink', 'orange')
    return [ colored_button(color, 'black') if color in black else colored_button(color, 'white') for color in BOX_COLORS]

def color_identifier_palette():
    row = [] 
    for color in BOX_COLORS:
        text= ''
        if color == 'red':
            text = '▼'
        row.append(sg.T(text, key=f'-TXT-{color}-', size=(6,1), pad=(0,0), background_color=BACKGROUND_COLOR))
    return row

def clear_text(d1,d2,d3, canvas):
    for figure in [d1,d2,d3]:
        canvas.delete_figure(figure)

def draw_text(text, loc, txt_color, canvas):
    return canvas.draw_text( text = text, location = loc, color = txt_color, font = "default 13")

def keep_text_on_canvas(figure_ids, max_col, canvas):
    coordinate = canvas.get_bounding_box(figure_ids[0])[0]
    x = coordinate[0]
    x_delta = None

    if x <= 0:
        x_delta = -x

    elif x>=max_col:
        x_delta = -(x-max_col)
    
    if x_delta:
        for figure in figure_ids:
            canvas.move_figure(figure, x_delta, 0)

def write_text_to_canvas(already_is_text, draw_id_text, rect_id, draw_id, text, selected_area, cur_txt_color,cur_box_color, canvas):
    if already_is_text: # if user is currently writing text -deletes and updates text
        clear_text(draw_id, draw_id_text, rect_id, canvas = canvas) 
        # print("clearing text")

    draw_id_text = canvas.draw_text(text = text , location =selected_area, color=cur_txt_color, font='Default 13')
    rect_id = canvas.draw_rectangle( canvas.get_bounding_box(draw_id_text)[0] , canvas.get_bounding_box(draw_id_text)[1], fill_color=cur_box_color)
    draw_id = canvas.draw_text(text = text , location =selected_area, color=cur_txt_color, font='Default 13')
    keep_text_on_canvas([draw_id, rect_id], MAX_X, canvas)
    return draw_id_text, rect_id, draw_id

def connect_selected_text_boxes(selected_boxes, selection_cursors, canvas):
    if len(selected_boxes) >= 2:
        line_id = canvas.draw_line(selected_boxes[-1], selected_boxes[-2], width=2)
        canvas.SendFigureToBack(line_id)
    for cursor in selection_cursors: 
        canvas.delete_figure(cursor)
    selection_cursors.clear()

def update_color(chosen_color, text_color_dict):
    return chosen_color, text_color_dict[chosen_color]

def create_canvas(key):
    return sg.Graph((5000,5000), (0,0),(MAX_X,MAX_Y),background_color="white", enable_events=True, key=key)

def main():

    sg.theme("Material2")

     
    layout = [ 

    [sg.Checkbox('Connect Mode', enable_events=True, key='Connect Mode', background_color=BACKGROUND_COLOR),\
    sg.Button('Connect'), sg.Text('', size=(50,1), background_color=BACKGROUND_COLOR),\
    sg.Button('Go To Images'),  \
    sg.Text('Colors:', background_color=BACKGROUND_COLOR)] + [sg.Column([color_identifier_palette(), color_palette()], background_color=BACKGROUND_COLOR)],

    [sg.TabGroup([[sg.Tab(f"Tab {i} ", [[sg.Column([[ create_canvas(i) ]], size=(1350,575),scrollable=True) ]], key = f"-TAB-{i}-", visible=(i==1)) for i in range(1,30) ]] + [[sg.Button('➕', key='-NEW-TAB-')]], enable_events=True) ] ,
                [sg.Input('', key='-IN-', enable_events=True, text_color=BACKGROUND_COLOR, background_color=BACKGROUND_COLOR)]
                ]


    # [sg.Column([[cur_canvas]], size=(1350,600),scrollable=True)],
    #             [sg.Input('', key='-IN-', enable_events=True, text_color=BACKGROUND_COLOR, background_color=BACKGROUND_COLOR)]

    #     ]

    window = sg.Window('MIMI', layout, background_color=BACKGROUND_COLOR)
     
    # Write text and lines
    selected_area = (0,0)
    last_selected = (0,0)
    draw_id = None
    point_id = None
    connect = [] #will contain locations of boxes that are to be connected
    selected = [] #will contain loc of temporary selection cursors when in connect mode
    cur_txt_color = 'white'
    cur_box_color = 'red'
    cur_icon = '-TXT-red-'
    cur_canvas = 1 

    while True:

        event, values = window.read()
        print(event)

        if event==sg.WIN_CLOSED:
            break

            
        if isinstance(event, int):
            window['-IN-'].update("")
            window['-IN-'].Widget.config(insertbackground=BACKGROUND_COLOR) #for the cursor to not be black 
            window['-IN-'].set_focus()
            selected_area = values[event]
            draw_id = None 
            rect_id = None
            draw_id_text = None

            if values['Connect Mode']:
                if not selected_area in connect:
                    connect.append(selected_area)
                selected.append(window[cur_canvas].draw_image(data=img, location=(selected_area[0]-10, selected_area[1]+8))) #will always need to tweak this when changing canvas size

                if len(selected) > 2:
                    unused_cursor = selected.pop(0) # updated the selected
                    window[cur_canvas].delete_figure(unused_cursor)
            
        if event=='-IN-':
            draw_id_text, rect_id, draw_id = write_text_to_canvas( all([draw_id, window['-IN-']]), draw_id, draw_id_text, rect_id, values['-IN-'].upper(), selected_area, cur_txt_color,cur_box_color, window[cur_canvas])

        elif event=='Connect':
            connect_selected_text_boxes(connect, selected, window[cur_canvas])

        elif event in BOX_COLORS: #updating textbox colors 
            cur_box_color, cur_txt_color = update_color(event, BOX_COLORS_TO_TEXT)
            window[cur_icon].update("")
            cur_icon = f'-TXT-{event}-'
            window[cur_icon].update("▼")


        elif event=='Go To Images':
        	webbrowser.open(random.choice(URLS))

        elif event == '-NEW-TAB-':
            cur_canvas += 1
            window[f'-TAB-{cur_canvas}-'].update(visible=True)
            window[f'-TAB-{cur_canvas}-'].select()
            

     
    window.close()

if __name__ == '__main__':
    main()