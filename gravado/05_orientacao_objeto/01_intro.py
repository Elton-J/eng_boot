# %%
import datetime
from datetime import date
class Pessoa:
    def __init__(self, nome: str, sobrenome: str, data_nascimento: datetime.date):
        self.nome = nome
        self.sobrenome = sobrenome
        self.data_nascimento = data_nascimento

    @property # Sem isso é método, com esse decorator vira um atributo como nome (sem () na chamada)
    def idade(self) -> int:
        return (date.today() - self.data_nascimento).days / 365.25

    def __str__(self) -> str: # Muda o texto quando a classe "elton" que era (bound method Pessoa.__str__ of <__main__.Pessoa object at 0x7f7c785433d0>) 
        return f'{self.nome} tem {self.idade} anos'

# %%
elton = Pessoa(nome='Elton', sobrenome='Júnior', data_nascimento=datetime.date(1999, 5, 1))

print(elton)
print(elton.nome)
print(elton.sobrenome)
print(elton.data_nascimento)
print(elton.idade)
