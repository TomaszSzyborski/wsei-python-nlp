'''
Protokół SYNC_PUB, tak jak PUB, pozwala na wysyłanie wiadomości do wielu subskrybentów jednocześnie,
również umożliwiając filtrowanie ich po tematach.
Jednak najważniejszą różnicą jest możliwość przesłania tym samym masowym kanałem wiadomości od subskrybenta do agenta publikującego,
a następnie przesłanie odpowiedzi na tą wiadomość w taki sposób, że tylko nadawca pierwotniej wiadomości ją otrzyma,
pomimo użycia masowego kanału. Dodatkowo można stosować tu filtrowanie wiadomości po tematach tak jak w protokole PUB.
'''



from osbrain import run_nameserver
from osbrain import run_agent
import time


def publikuj(agent):
    agent.send('wydawca', 'Publikujemy nowy numer...')


def wygeneruj_odpowiedz(agent, wiadomosc):
    return 'Otrzymano wiadomość: "%s"' % wiadomosc


def przeczytaj_publikacje(agent, publikacja):
    agent.log_info('Przeczytano: "%s"' % publikacja)


def przetworz_pozniej(agent, wiadomosc):
    agent.log_info('Odpowiedź od wydawcy: "%s"' % wiadomosc)


if __name__ == '__main__':
    ns = run_nameserver()  # uruchomienie serwera
    alice = run_agent('Alice')  # uruchomienie agenta z aliasem Alice i przypisanie jego proxy do zmiennej
    bob = run_agent('Bob')
    eve = run_agent('Eve')

    addr = alice.bind('SYNC_PUB', alias='wydawca', handler=wygeneruj_odpowiedz)
    #połączenie za pomocą SYNC_PUB wymaga od publikującego agenta zadeklarowania funkcji
    # obsługującej wiadomości otrzymywane od subskrybentów w przeciwieństwie do publikowanych wiadomości,
    # odpowiedź na wiadomość otrzymaną od sybskrybenta jest przekazywana tylko do niego, mimo użycia tego samego kanału
    bob.connect(addr, alias='wydawca', handler=przeczytaj_publikacje)
    eve.connect(addr, alias='wydawca', handler=przeczytaj_publikacje)

    alice.each(0.4, publikuj) #co 0.4s jest wykonywana funkcja publikuj przez agenta alice
    time.sleep(1)
    bob.send('wydawca', 'Bob ma pytanie!', handler=przetworz_pozniej)
    #bob przesyła wiadomość do wydawcy. Otrzymana odpowiedź zostanie obsłużona przez funkcję przetworz_pozniej
    time.sleep(1)

    ns.shutdown()  # zamknięcie serwera i usunięcie utworzonych agentów
