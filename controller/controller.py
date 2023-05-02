from model.model import Model


class Controller:
    def __init__(self, view) -> None:
        self.model = Model(view)
    
    def process_sentence(self, text: str):
        processed_sentence = self.model.process_sentence(text)
        print("sentence: ", processed_sentence)
        self.model.fill_table(processed_sentence)

    def process_filter(self, filter_text: str):
        self.model.filter_table(filter_text)
        
    def process_reset(self):
        self.model.reset_table()
        
    def get_result(self):
        self.model.refresh_current_result()
        return self.model.current_result
    
    def fill_load_data(self, data: dict):
        self.model.fill_table(data)