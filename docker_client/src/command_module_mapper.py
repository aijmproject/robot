class CommandModuleMapper:
    def __init__(self):
        self.module_1 = "surveillance bébé"
        self.module_2 = "surveillance maison"
        self.module_to_code = {self.module_1:1, self.module_2:2}
        self.code_to_module = {1:self.module_1, 2:self.module_2}