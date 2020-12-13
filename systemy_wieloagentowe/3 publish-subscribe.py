'''
Protokół PUB pozwala na wysyłanie wiadomości jednocześnie do wielu odbiorców,
tak jak to ma miejsce w przypadku tradycyjnego publikowania informacji i przesyłania ich do subskrybentów.
Dzięki takiemu podejściu, jednocześnie wielu agentów może wykonywać różne operacje na tych samych danych.
Jeśli na pewnych danych nie ma potrzeby wykonywania niektórych operacji można do wiadomości dodawać tematy,
dzięki którym tylko agenci którzy subskrybują dany temat będą mogli obsłużyć przesłaną wiadomość.
'''

from osbrain import run_nameserver
from osbrain import run_agent
import time
import random


def save_to_log_subject_A(agent, wiadomosc):
    agent.log_info('Otrzymano temat A: "%s"' % wiadomosc)


def save_to_log_subject_B(agent, wiadomosc):
    agent.log_info('Otrzymano temat B: "%s"' % wiadomosc)


if __name__ == '__main__':
    ns = run_nameserver() #uruchomienie serwera
    alice = run_agent('Alice') #uruchomienie agenta z aliasem Alice i przypisanie jego proxy do zmiennej
    bob = run_agent('Bob')
    eve = run_agent('Eve') #uruchamiamy kolejnych agentów
    dave = run_agent('Dave')

    addr = alice.bind('PUB', alias='main')
    #protokół PUB pozwala na wysłanie wiadomości do wszystkich agentów w danym kanale
    bob.connect(addr, handler={'A': save_to_log_subject_A, 'B': save_to_log_subject_B})
    # nawiasy wąsate pozwalają wybrać funckję obsługującą w zależności od tematu
    eve.connect(addr, handler={'A': save_to_log_subject_A})
    dave.connect(addr, handler={'B': save_to_log_subject_B})

    for _ in range(6):
        time.sleep(2)
        temat = random.choice(['A', 'B'])
        wiadomosc = 'Cześć wszystkim! Temat %s!' % temat
        alice.send('main', wiadomosc, topic=temat)
        # alice wysyła wiadomość w kanale main, o losowo wybranym temacie,
        # która następnie zostanie odebrana przez wszystkich subskrybentów,
        # ale obsłużona tylko przez subskrybujących wylosowany temat

    ns.shutdown() #zamknięcie serwera i usunięcie utworzonych agentów
