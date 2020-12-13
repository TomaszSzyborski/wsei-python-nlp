'''
Agenci, poza przekazywaniem wiadomości i wykonywaniem przypisanych funkcji,
mogą również przechowywać własne zmienne i funkcje, do których można się później odwoływać w wygodniejszy sposób.
Ważną operacją jest również kończenie pracy agentów po zakończeniu wykonywania zadań.
Domyślnie, w momencie zakończenia pracy serwera wszyscy agenci którzy byli do niego przypisani również są zamykani.
Natomiast gdyby zaszła potrzeba wcześniej zakończyć pracę któregoś z agentów wystarczy wywołać na nim komendę shutdown.
'''



from osbrain import run_agent
from osbrain import run_nameserver


def sum_of_numbers(self):
    return self.liczba1 + self.liczba2


if __name__ == '__main__':
    ns = run_nameserver() #uruchomienie serwera
    alice = run_agent('Alice') #uruchomienie agenta alice

    alice.set_attr(liczba1=3, liczba2=5) #ustawienie jako domyślne atrybuty 2 liczby
    alice.set_method(suma=sum_of_numbers) #przypisanie funcji jak metody agenta

    print(alice.suma()) #wywołanie metody bez konieczności podawania atrybutów

    ns.shutdown()
