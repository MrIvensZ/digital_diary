from database import Database, engine, EntryORM
from gui_class import Gui

if __name__ == '__main__':
    db = Database(engine, EntryORM)
    gui = Gui(db)
    gui.run()
