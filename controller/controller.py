from model.model import Model


class Controller:
    def __init__(self, view) -> None:
        self.model = Model(view)
    
    def send_message(self, text):
        response = self.model.make_response(text)
        return response
    
    def process_text(self, text: str):
        processed_text = self.model.process_text(text)
        print("processed_text: ", processed_text)

    def process_filter(self, filter_text: str):
        self.model.filter_table(filter_text)
        
    def process_reset(self):
        self.model.reset_table()
        
    def get_result(self):
        self.model.refresh_current_result()
        return self.model.current_result
    
    def fill_load_data(self, data: dict):
        self.model.fill_table(data)