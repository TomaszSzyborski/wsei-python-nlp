'''
Protokół ASYNC_REP jest wykorzystywany gdy zachodzi potrzeba wywołania zapytania do innego agenta,
ale odpowiedź można odebrać i przetworzyć w późniejszym terminie.
W tym celu dwaj agenci muszą posiadać zdefiniowane funkcje reagujące na otrzymane wiadomości.
Początek działania takiej komunikacji jest bardzo podobny do protokołu REP,
gdzie agent przypisany (bob) wysyła wiadomość do agenta powiązanego (alice),
ale zamiast czekać na odpowiedź może zająć się innymi zadaniami,
a w momencie otrzymania odpowiedzi wywoływana jest odpowiednia funkcja odpowiedzialna za jej przetworzenie.
Ponadto możliwe jest również ustalenie czasu oczekiwania na odpowiedź,
po przekroczeniu którego zostanie wykonana inna funkcja, mająca za zadanie odpowiednio zareagować w takiej sytuacji.
'''



from osbrain import run_nameserver
from osbrain import run_agent
import time


def odpowiedz_pozniej(agent, wiadomosc):
    time.sleep(2)
    return 'Cześć, Bob!'


def przetworz_pozniej(agent, wiadomosc):
    agent.log_info('Otrzymano odpowiedź: %s' % wiadomosc)


def brak_odpowiedzi(agent):
    agent.log_warning('Nie otrzymano odpowiedzi!')


if __name__ == '__main__':
    ns = run_nameserver() #uruchomienie serwera
    alice = run_agent('Alice') #uruchomienie agenta z aliasem Alice
    bob = run_agent('Bob')

    addr = alice.bind('ASYNC_REP', handler=odpowiedz_pozniej)
    # przypisanie do adresu agenta alice, używając protokołu ASYNC_REPLY.
    # gdy przez na ten adres zostanie przesłana wiadomość, zostanie obsłużona przez funkcję odpowiedz_pozniej
    bob.connect(addr, alias='kanal', handler=przetworz_pozniej)
    #połączenie agenta bob do adresu alice
    # otrzymana wiadomość zostanie obsłużona przez funkcję przetworz_pozniej

    bob.send('kanal', 'Cześć! Tu Bob!', wait=1, on_error=brak_odpowiedzi)
    #bob wysyła wiadomość przez kanal, ale jeśli nie otrzyma odpowiedzi w ciągu 1s, błąd zostanie dodany do dziennika
    bob.log_info('Wysłano wiadomość do Alice')

    bob.log_info('Oczekuję na odpowiedź')
    time.sleep(0.1)

    ns.shutdown() #zamknięcie serwera i usunięcie utworzonych agentów
