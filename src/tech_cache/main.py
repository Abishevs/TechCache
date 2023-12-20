# def on_light_theme_selected():
#     messagebox.showwarning("Warning", "Light theme attracts bugs! Proceed with caution.")

import sys
import os
from PyQt6 import QtWidgets
from tech_cache.views.main_window import MainWindow
from tech_cache.utils.logger_conf import LoggerConfig

def main():
    os.environ['DEBUG_MODE'] = '1' # on
    # os.environ['DEBUG_MODE'] = '0' # off
    LoggerConfig.setup_logging()
    app = QtWidgets.QApplication(sys.argv)
    mainWin = MainWindow()
    mainWin.show()
    sys.exit(app.exec())


if __name__ == "__main__":
    main()

