from dotenv import load_dotenv
from ui.main_window import MainWindow

if __name__ == "__main__":

    load_dotenv()

    app = MainWindow()

    app.mainloop()