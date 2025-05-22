import pandas as pd

class ExportadorCSV:
    @staticmethod
    def exportar(lista_alunos, caminho):
        df = pd.DataFrame([aluno.to_dict() for aluno in lista_alunos])
        df.to_csv(caminho, index=False, encoding='utf-8-sig')
        print(f"Arquivo salvo em: {caminho}")
