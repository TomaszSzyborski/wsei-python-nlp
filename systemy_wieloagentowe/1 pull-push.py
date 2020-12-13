'''
Pierwsza rzecz jaką należy zrobić korzystając z biblioteki OSBrain,
to uruchomienie serwera na którym następnie zostaną utworzeni agenci,
mogący niezależnie od siebie wykonywać zadane polecenia.
Podstawą takiego systemu jest komunikacja między agentami w celu synchronizacji pracy i przekazywania informacji.
W omawianym przykładzie wykorzystywany jest protokół PUSH,
dzięki któremu wiadomość wysyłana w utworzonym kanele przez agenta powiązanego (alice) wywołuje odpowiednią funkcję
w agencie który dołączył do kanału (bob).
'''

from osbrain import run_nameserver
from osbrain import run_agent
import time


def zapisz_wiadomosc(agent, wiadomosc):
    agent.log_info('Otrzymano: %s' % wiadomosc)


if __name__ == '__main__':
    ns = run_nameserver() #uruchomienie serwera
    alice = run_agent('Alice') #uruchomienie agenta z aliasem Alice i przypisanie jego proxy do zmiennej
    bob = run_agent('Bob')

    #ten typ połączenia polega na wywołaniu przez agenta Alice akcji obsługiwanej przez agenta Bob
    addr = alice.bind('PUSH', alias='main')
    # bind zwraca adres do którego został powiązany agent alice.
    # W parametrach przekazywane są: protokół komunikacji oraz alias kanału
    bob.connect(addr, handler=zapisz_wiadomosc)
    #connect pozwala na połączenie innego agenta do istniejącego kanału przekazując jego adres,
    # oraz za pomocą jakiej funkcji obsłużyć otrzymaną wiadomość

    for _ in range(3): #wykonaj 3 razy
        time.sleep(1) #czekaj 1 sekundę
        alice.send('main', 'Cześć, Bob!')
        #Alice wysyła w kanale main wiadomość "Cześć Bob!"

    ns.shutdown() #zamknięcie serwera i usunięcie utworzonych agentów