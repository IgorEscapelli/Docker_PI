import random

class ErroInjector:
    @staticmethod
    def aplicar(aluno_dict, prob_erro=0.10):
        campos_erro = {
            'nome_aluno': ['#######', '22333123', '', None, 'INVALID', 'AAAAAAAAAAAAAA2', 'IJIJIJII', 0, 10, '101010101'],
            'email_aluno': ['@email', 'user@@site', 'none.com', '?', 'INVALID', 'amazonas', 'NOTEXIST', 'ilegivel'],
            'sexo': ['????', 'XXXXXXXXX', 'INVALID','', 'Masculinas','Femeadoa',902334, 'EXIT01', 'naoreconhecido'],
            'idade': [-5, 130, 999, None, 6676, -13, -393,'', 'numero', 'um', 'vinte','quinzee',-93248, 'NOTEXIST'],
            'renda_familiar': [-1000, 0, 10000000000,00000000,-0,19329320423234,-2349234, -9239, None, 'INVALID'],
            'curso': ['1233E', '', None,'concluido', 'email@gmail.com', 'alguns', '$$$$$$$','veteri', 'WEWEO'],
            'estado_civil': ['Casadoo', '', 'XW0S2#$@43','naoencontrado', None, 'Relacioname', 'Solte', 'XXXOXO0', 'ERROR']
        }

        for campo, valores in campos_erro.items():
            if random.random() < prob_erro:
                aluno_dict[campo] = random.choice(valores)
        return aluno_dict
