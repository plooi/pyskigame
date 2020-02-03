import PySimpleGUI as sg
from time import sleep
progress = 0
in_use = False
window = None
from threading import Thread

def progress_bar(text="Loading...", window_title = ""):
    global progress,in_use,window
    if in_use:
        layout = [[sg.Text('Progress bar already in use!')]]
    
        window = sg.Window('', layout, size=(500,300), non_blocking=True)
        event, values = window.Read()
        window.close()
        return
    
    progress = 0
    in_use = True
    
    layout = [[sg.Text(text)],
              [sg.ProgressBar(100, orientation='h', size=(20, 20), key='progressbar')]]
    
    
    window = sg.Window(window_title, layout)

def update(progress):
    
    global window,in_use
    
    if window == None:
        return
    window.read(timeout=0)
    if progress >= 99:
        in_use = False
        window.close()
        window = None
        return
    progress_bar = window['progressbar']
    progress_bar.UpdateBar(progress)
    
def main():
    progress_bar()
    for i in range(0,10000,1):
        update(i/100)

if __name__ == "__main__": main()
    
