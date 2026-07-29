import os
from kivy.app import App

class Database:
    def __init__(self, path=None):
        if path is None:
            # التحقق مما إذا كان التطبيق يعمل على أندرويد لتحديد مسار التخزين الداخلي الآمن
            try:
                app = App.get_running_app()
                if app and app.user_data_dir:
                    data_dir = app.user_data_dir
                else:
                    data_dir = ""
            except:
                data_dir = ""
            
            self.path = os.path.join(data_dir, "inventory.db")
        else:
            self.path = path
            
        self.conn = sqlite3.connect(self.path)
        self.conn.row_factory = sqlite3.Row
        self.create_tables()
        
