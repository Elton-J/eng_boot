# %%
from typing import List
import datetime
from datetime import date

#%%
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


class Curriculo:
    def __init__(self, pessoa: Pessoa, exp: List[str]):
          self.pessoa = pessoa
          self.exp = exp

    @property
    def qtd_exps(self) -> int:
        return len(self.exp)

    @property
    def ultima_exp(self) -> str:
        return self.exp[-1]

    def adiciona_exp(self, nova_exp: str) -> None: # Retorna nada, mas adiciona
        self.exp.append(nova_exp)

    def __str__(self):
       return f'{self.pessoa.nome} tem {self.pessoa.idade} e já teve {self.qtd_exps} exps.' \
              f' Atualmente trabalha para {self.ultima_exp}'    







# %%
elton = Pessoa(nome='Elton', sobrenome='Júnior', data_nascimento=datetime.date(1999, 5, 1))

print(elton)
print(elton.nome)
print(elton.sobrenome)
print(elton.data_nascimento)
print(elton.idade)


# %%
cv_elton = Curriculo(pessoa=elton, exp=['PSD', 'Nielsen', 'Kroton', 'Petz', 'Autopass', 'EBANX', 'BV'])

print(cv_elton.pessoa)
print(cv_elton.pessoa.nome)
print(cv_elton.pessoa.idade)
print(cv_elton)
print(cv_elton.exp)
cv_elton.adiciona_exp(nova_exp='Preditiva.ai')
print(cv_elton.exp)


## Parte 2 - Heranças

# %%

class Vivente:
    def __init__(self, nome: str, data_nascimento: datetime.date) -> None:
        self.nome = nome
        self.data_nascimento = data_nascimento

    
    @property
    def idade(self) -> int:
        return (date.today() - self.data_nascimento).days / 365.25

    def emite_ruido(self, ruido: str):
        print(f'{self.nome} emite o ruído {ruido}')


class PessoaHeranca(Vivente): # Herda a classe Vivente
    def __str__(self) -> str: 
        return f'{self.nome} tem {self.idade} anos'

    def fala(self, frase):
        self.emite_ruido(frase)


class Cachorro(Vivente): # Adiciona arg raca na classe herdeira
    def __init__(self, nome: str, data_nascimento: datetime.date, raca: str) -> None:
        super().__init__(nome, data_nascimento) # super() chama Vivente, classe mãe
        self.raca = raca

    def __str__(self) -> str:
        return f'{self.nome} é da raça {self.raca} e tem {self.idade} anos'

    def late(self):
        self.emite_ruido('Au! Au!')

# %%
elton2 = PessoaHeranca(nome='Elton2',
                       data_nascimento=date(1999, 5, 1)) # Parametros de Vivente
print(elton2)

# %%
spyke = Cachorro(nome='Spyke',
                 data_nascimento=date(2019, 5, 1),
                 raca='Vira-Lata') # Parametros de Vivente

print(spyke)


# %%
spyke.late()
elton2.fala('Porra')
# %%
