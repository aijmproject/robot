class TextCommandMapper:
    def __init__(self):
        self.command_code_1 = "surveillance bébé"
        self.command_code_2 = "surveillance maison"
        self.command_code_3 = "mode veille"
        self.command_text_to_code = {self.command_code_1:1, self.command_code_2:2, self.command_code_3: 3}
        self.command_code_to_text = {1:self.command_code_1, 2:self.command_code_2, 3: self.command_code_3}
    
    def get_code_by_text(self, text):
        if text not in self.command_text_to_code:
            return -1
        return self.command_text_to_code[text]
    
    def get_text_by_code(self,code):
        if code not in self.command_code_to_text:
            return "-1"   
        return self.command_code_to_text[code]


