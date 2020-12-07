# from fbs_runtime.application_context.PyQt5  import ApplicationContext
from PyQt5.QtWidgets import QApplication
from GUI import GUI
# import sys

if __name__ == "__main__":
    # appctxt = ApplicationContext()
    app = QApplication([])
    gui = GUI()
    app.exec_()
    # exit_code = appctxt.app.exec_()      # 2. Invoke appctxt.app.exec_()
    # sys.exit(exit_code)