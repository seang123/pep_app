from pywinauto import Desktop, Application, timings
from io import StringIO  # Python3 use: from io import StringIO
import os
import time
import sys

""" Automatically decode Zmax files  --  assume best case """

class CapturePrint:
    # Redirects print() output to a variable
    # then resets the print() output to stdout
    def __ini__(self):
        pass

    def get_text(self):
        return self.output_text.getvalue()

    def __enter__(self):
        self.old_stdout = sys.stdout
        sys.stdout = self.output_text = StringIO()
        return self

    def __exit__(self, ext_type, exc_value, traceback):
        sys.stdout = self.old_stdout


def open_app(start_new = False):
    """ Start or connect to an instance of the HDRecorder app """
    app = "C:\Program Files (x86)\Hypnodyne\ZMax\HDRecorder.exe"
    if start_new:
        Application().start(app)
    app = Application(backend = 'uia').connect(path = app, title = 'HDRecorder')
    return app

def read_from_memory_card(app):
    pass


def process_one(app, i):
    app.HDRecorder.set_focus()
    with CapturePrint() as f:
        app.HDRecorder.print_control_identifiers()
        content = f.get_text()

    window = app.window(best_match = 'Diagog')

    # Open the file-explorer in HDRecorder
    window.child_window(best_match = 'Button4').click_input()

    #window.print_control_identifiers()


    # Navigate to desktop
    #x = window.child_window(best_match = 'Open').child_window(best_match = 'Pane2').child_window(best_match = 'TreeItem1').child_window(best_match = 'Desktop')
    x = window.child_window(best_match = 'Desktop (pinned)')
    x.click_input()

    # Navigate to Zmax_temporary folder
    x = window.child_window(best_match = 'Open').child_window(best_match = 'Zmax_temporary')
    x.double_click_input()

    ## Select the hypno file to decode
    open = window.child_window(best_match = 'Open')

    hypno = open.child_window(best_match = f'hypno{i}.hyp')
    hypno.double_click_input()

    # Click 'OK' in the confirmation box
    ok = window.child_window(best_match = 'OK')
    ok.click()

    folder = window.child_window(best_match = f'{i}')
    folder.click_input()

    # open folder
    window.child_window(best_match = 'Open3').click_input()
    # Save
    #window.print_control_identifiers()
    window.child_window(best_match = 'Button16').click_input()





def main():
    for i in [1, 2, 3, 4, 5, 6, 7]:
        print(f'Decoding hyno: {i}')
        app = open_app(True)
        process_one(app, str(i))
    print('Finished!')



if __name__ == '__main__':
    main()