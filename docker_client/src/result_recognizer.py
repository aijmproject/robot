import operator
from operator import itemgetter
class ResultUsersRecognizer:
    
    def _get_users_recognized(self, recognition_data):
        result = []
        for key, value in recognition_data.items():
            max_value = max(value.items(), key=operator.itemgetter(1))
            result.append(max_value)
        return result
    
    def get_recognized_result(self,input_data):
        print("input_data :", input_data)
        result = self._get_users_recognized(input_data)
        _inconnu_l = "inconnu"
        if len(result) == 0:
            return 1, [_inconnu_l]
        elif len(result) == 1:
            name,acc = result[0]
            if acc > 0.90:
                return 2, [name]
            elif acc > 80:
                return 3, [name]
            else:
                return 4, [_inconnu_l]
        else:
            result_value = [value >= 0.80 for name,value in result]
            if all(result_value):
                return 5, [name for name,value in result]
            elif any(result_value):
                reconnus = []
                inconnus = []
                for name,value in result:
                    if value >= 0.80:
                        reconnus.append(name)
                    else:
                        inconnus.append("{0}_{1}".format(_inconnu_l,len(inconnus)))
                return 6,reconnus + inconnus
            else:
                return 7, ["{0}_{1}".format(_inconnu_l, index) for index, item in enumerate(result)]

if __name__ == "__main__":
    app  = ResultUsersRecognizer()
    dict_ = {0: {'Ibrahim': 0.186, 'Junior': 0.015, 'Matthew': 0.807}, 1: {'Ibrahim': 0.874, 'Junior': 0.054, 'Matthew': 0.097}}
    dict_1 = {0: {'Ibrahim': 0.874, 'Junior': 0.054, 'Matthew': 0.097}}
    print(app.get_recognized_result(dict_1))
            