import random
class ResponseRandomProvider:
    def __init__(self):
        self.not_undestand_commands = ["Désolé, je n'ai pas compris la commande", "Désolé, je n'ai rien compris", "Désolé, je n'ai pas pu comprendre"]
        self.no_access_rights = ["Désolé, vous n'avez pas le droit nécessaire", "je suis navré, mais vous n'avez pas l'autorisation", "Désolé, mais vous n'avez pas le droit d'accès à cette commande"]
        self.bot_ask_to_speaks = ["Oui, quelle est votre demande", "Que puis-je faire pour vous ?", "Oui, je suis à votre écoute"]
        self.fatal_error_texts = ["Il y a eu un problème réseau, veuillez redire svp"]
    
    def not_undestand_command(self):
        return random.choice(self.not_undestand_commands)
    
    def no_access_right(self):
        return random.choice(self.no_access_rights)

    def bot_ask_to_speak(self):
        return random.choice(self.bot_ask_to_speaks)
    
    def fatal_error_text(self):
        retunr random.choice(self.fatal_error_texts)

