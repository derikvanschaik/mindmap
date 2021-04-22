#A basic PySimpleGUI graph example
import PySimpleGUI as sg
import random
import webbrowser
#This is the new line i added while checking out branch new

# -------------CONSTANTS BELOW---------------------#
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

T_OFF = b'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'
T_ON = b'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'
# -------------CONSTANTS ABOVE---------------------#

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

def get_user_text(text_input_element):
    text_input_element.update("")
    text_input_element.Widget.config(insertbackground=BACKGROUND_COLOR) #for the cursor to not be black 
    text_input_element.set_focus()

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

def create_text_element(canvas, text, selected_area, cur_txt_color, additional_font):
    font_add = ""
    if additional_font:
        font_add += additional_font

    canvas.draw_text(text = text , location =selected_area, color=cur_txt_color, font='Default 13'+ ' ' +font_add)

def is_approx_in(search_tup, dict):
    y_threshold = 7
    x_threshold = 25
    for loc_tup in dict.keys():
        if search_tup[0] == loc_tup[0] and abs(search_tup[1] - loc_tup[1]) <= x_threshold and abs(search_tup[2] - loc_tup[2]) <= y_threshold:
            return loc_tup

    return None #could not find a match


def main():

    sg.theme("Material2")

    layout = [ 

   # [sg.Checkbox('Connect Mode', enable_events=True, key='Connect Mode', background_color=BACKGROUND_COLOR),\
    [sg.Column(
        [
        [sg.T('Connect Mode', font='default 9 italic', background_color=BACKGROUND_COLOR), sg.T('OFF', key='-CON-STAT-', text_color = 'dark grey', size=(3,1),background_color=BACKGROUND_COLOR,justification='right'), sg.T('', size=(12,1),  background_color=BACKGROUND_COLOR), sg.T('Links are:', font=('default 9 italic'),  background_color=BACKGROUND_COLOR), sg.T('HOT', text_color='red', k='-LINK-STAT-', size= (6,1),background_color=BACKGROUND_COLOR)],
        [sg.B(image_data=T_OFF, k='-TOGGLE1-', metadata=False, button_color=(BACKGROUND_COLOR, BACKGROUND_COLOR), border_width=0, image_subsample=2), sg.Button('Connect', size=(8,1)), sg.T('', size=(10,1), background_color=BACKGROUND_COLOR),sg.B('Link', size=(8,1)), sg.B(' ', button_color = ('red', 'red'), k='-HOT-LINK-',metadata=True, size=(5,1) ,pad=(0,0)), sg.B(' ', button_color = ('grey', 'grey'), k='-COLD-LINK-', metadata = False, size=(1,1), pad=(0,0))]], background_color = BACKGROUND_COLOR), \
    sg.Button('Go To Images'),  \
    sg.Text('Colors:', background_color=BACKGROUND_COLOR)] + [sg.Column([color_identifier_palette(), color_palette()], background_color=BACKGROUND_COLOR)], #canvas change here

    [sg.TabGroup([[sg.Tab(f"Tab {i} ", [[sg.Column([[ create_canvas(i) ]], size=(1350,575),scrollable=True) ]], key = f"-TAB-{i}-", visible=(i==1)) for i in range(1,30) ]] + [[sg.Button('➕', key='-NEW-TAB-')]]) ] ,
                [sg.Input('', key='-IN-', enable_events=True, text_color=BACKGROUND_COLOR, background_color=BACKGROUND_COLOR)]
    ]

    window = sg.Window('MIMI', layout, background_color=BACKGROUND_COLOR)
     
    selected_area = (0,0)
    last_selected = (0,0)
    draw_id = None
    point_id = None
    connect = [] #will contain locations of boxes that are to be connected
    selected = [] #will contain loc of temporary selection cursors when in connect mode
    linked = {} #(tab num, x, y) --> link (tab number)
    linked_to_text = {} #(tab num, x, y) --> text 
    cur_txt_color = 'white'
    cur_box_color = 'red'
    cur_icon = '-TXT-red-'
    cur_canvas = 1
    most_recently_visible_canvas = 1
    linked_was_generated = False
    last_tab = 1
    connect_mode = False
    hot_links = True

    while True:
        event, values = window.read()

        if event==sg.WIN_CLOSED:
            break


        elif isinstance(event, int): #canvas was clicked
            cur_canvas = event
            get_user_text(window['-IN-'])
            selected_area = values[event]
            draw_id = None 
            rect_id = None
            draw_id_text = None
            is_hot_link = is_approx_in( (event, selected_area[0], selected_area[1] ) ,linked)

            if connect_mode:
                if not selected_area in connect:
                    connect.append(selected_area)
                selected.append(window[cur_canvas].draw_image(data=img, location=(selected_area[0]-10, selected_area[1]+8))) #draws snipping cursor

                if len(selected) > 2: # cannot connect more than 2 text boxes at a time -- delete least recent snipping cursor
                    unused_cursor = selected.pop(0) 
                    window[cur_canvas].delete_figure(unused_cursor)

            if is_hot_link and hot_links:
                window[f'-TAB-{linked[is_hot_link]}-'].select() #go to the hot link

            if is_hot_link and not hot_links and not connect_mode: #they are trying to go back to a link but forgot to enable hot links again 
                sg.popup("Hot links are disabled!")
            
        elif event=='-IN-':
            linked_to_text[(cur_canvas, selected_area[0], selected_area[1])] = values['-IN-'] 
            draw_id_text, rect_id, draw_id = write_text_to_canvas( all([draw_id, window['-IN-']]), draw_id, draw_id_text, rect_id, values['-IN-'].upper(), selected_area, cur_txt_color,cur_box_color, window[cur_canvas])
            #get the text associated with this tab number and location 
            # print(values['-IN-'])
            # print("selected area:", selected_area)

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
            print("most_recently_visible_canvas in new tab event", most_recently_visible_canvas)
            most_recently_visible_canvas += 1
            window[f'-TAB-{most_recently_visible_canvas}-'].update(visible=True)
            window[f'-TAB-{most_recently_visible_canvas}-'].select()

            if linked_was_generated:
                linked_was_generated = False
                create_text_element(window[most_recently_visible_canvas], linked_to_text[ (cur_canvas, selected_area[0], selected_area[1]) ], (50, 1780), 'blue', 'italic underline' )
                linked[ (most_recently_visible_canvas, 50, 1780 ) ] = cur_canvas # back link is created 

     
        elif event == 'Link':

            tab_and_location_tup = (cur_canvas, selected_area[0], selected_area[1]) 
            linked[tab_and_location_tup] = most_recently_visible_canvas + 1 #forward link is created 
            window['-NEW-TAB-'].click() #activate new tab event
            linked_was_generated = True #identifier to draw a link

        elif event.startswith('-TOGGLE'): #Thanks for this one @ Mike! Taken from: https://github.com/PySimpleGUI/PySimpleGUI/blob/master/DemoPrograms/Demo_Simple_Material_Feel.py
            state = window[event].metadata = not window[event].metadata
            window[event].update(image_data=T_ON if state else T_OFF, image_subsample=2)
            window[event].set_size(size=(40,30))
            connect_mode = not connect_mode
            if connect_mode:
                window['-CON-STAT-'].update('ON', text_color='dark blue')
            else:
                window['-CON-STAT-'].update('OFF', text_color='dark grey')

        elif event in ('-HOT-LINK-', '-COLD-LINK-'):

            if hot_links:
                window['-HOT-LINK-'].update( button_color=('grey', 'grey'))
                window['-HOT-LINK-'].set_size(size=(1,1))
                window['-COLD-LINK-'].update(button_color=('blue', 'blue'))
                window['-COLD-LINK-'].set_size(size=(5,1))
                window['-LINK-STAT-'].update("COLD", text_color='blue')
            else:
                window['-HOT-LINK-'].update(button_color=('red', 'red'))
                window['-HOT-LINK-'].set_size(size=(5,1))
                window['-COLD-LINK-'].update(button_color=('grey', 'grey'))
                window['-COLD-LINK-'].set_size(size=(1,1))
                window['-LINK-STAT-'].update("HOT", text_color='red')

            hot_links = not hot_links




        # print(linked)
    window.close()

if __name__ == '__main__':
    main()