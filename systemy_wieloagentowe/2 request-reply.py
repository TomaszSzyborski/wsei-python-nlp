'''
W przypadku protokołu REP działanie jest odwrotnie niż w przypadku PUSH,
czyli agent dołączony (bob) wysyła wiadomość do agenta powiązanego (alice),
który następnie wysyła odpowiedź na wiadomość tym samym kanałem.
Należy pamiętać, że dopóki odpowiedź nie zostanie odebrana, nie będzie można tym samym kanałem wysłać kolejnej wiadomości.
 W tej sytuacji pojawia się też nowa forma zwracania odpowiedzi.
 Zazwyczaj do tego celu jest wykorzystywane polecenie return, które zwraca wartość i kończy działanie funkcji.
'''

from osbrain import run_nameserver
from osbrain import run_agent


def reply_for_request(agent, wiadomosc):
    #zwracana jest wiadomość jaka zostanie wysłana w odpowiedzi
    return 'Potwierdzam otrzymanie: "' + str(wiadomosc) + '"'


def reply_for_request_using_yield(agent, wiadomosc):
    #return zwraca dane i natychmiast kończy działanie funkcji
    #yield zwraca dane ale pozwala na wykonywanie kolejnych działań
    yield 'Potwierdzam otrzymanie: ' + str(wiadomosc) + '"!'
    agent.log_info('Już wysłano odpowiedź, ale jeszcze mogę zapisać to w dzienniku!')


if __name__ == '__main__':
    ns = run_nameserver() #uruchomienie serwera
    alice = run_agent('Alice') #uruchomienie agenta z aliasem Alice i przypisanie jego proxy do zmiennej
    bob = run_agent('Bob')

    addr = alice.bind('REP', alias='main', handler=reply_for_request)
    #addr zawiera adres do którego został przypisany agent alice, za pomocą protokołu REP,
    # dodatkowo została podana nazwa funkcji do obsługi otrzymanych wiadomości
    #   dla przetestowania YIELD zmień "handler=wygeneruj_odpowiedz" na "handler=wykrzycz_odpowiedz"
    bob.connect(addr, alias='main')
    # bob został przypisany do tego kanału, tym razem nie musi obsługiwać otrzymanej wiadomości

    for i in range(10): # wykonaj 10 razy licząc od 0 dla i
        bob.send('main', 'Wiadomość nr ' + str(i)) #wysyła w kanale main wiadomość z kolejnymi numerami
        odpowiedz = bob.recv('main') #przypisanie do zmiennej odpowiedzi otrzymanej kanałem main
        # oczekiwanie na odpowiedź nie musi być wywołane natychmiast po wysłaniu wiadomości.
        # w tym czasie mogą być wykonywane inne zadania, a odpowiedź przetworzona dopiero gdy będzie potrzebna.
        # Trzeba pamiętać, że dopóki odpowiedź nie zostanie odebrana, nie można wysłać kolejnej wiadomości tym kanałem.
        print(odpowiedz) #wyświetlene odpowiedzi

    ns.shutdown() #zamknięcie serwera i usunięcie utworzonych agentów
