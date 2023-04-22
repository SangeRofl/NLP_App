from model.model import Model


class Controller:
    def __init__(self, view) -> None:
        self.model = Model(view)
    
    def process_text(self, text: str):
        processed_text = self.model.process_text(text)
        print("processed_text: ", processed_text)

    def process_filter(self, filter_text: str):
        self.model.filter_table(filter_text)
        
    def process_reset(self):
        self.model.reset_table()