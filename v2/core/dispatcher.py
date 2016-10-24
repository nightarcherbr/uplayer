import weakref;
import threading;

_any = "BROADCAST";

class DispatcherError(Exception):
    pass

class Dispatcher():
    def __init__(self):
        self.signals = {};

    def subscribe(self, listener, signal = _any, weak = True ):
        """
        Register signal listener
        """
        if signal is None :
            signal = _any;
        signal = signal.upper();

        # Cria uma referencia fraca
        if( weak ): 
            def dead_signal_remover(ref):
                for target in self.signals[signal]:
                    if id(target) == id(ref) :
                        self.signals[signal].remove(target);
            listener = weakref.ref(listener, dead_signal_remover);

        # Ja existe signals registrados com esse nome
        if( signal not in self.signals ):
            self.signals[signal] = [];

        # Adiciona o signal na lista
        self.signals[ signal ].append( listener );

    def unsubscribe(self, listener, signal = _any ):
        """
        Unregister a signal listener
        """
        if signal is None :
            signal = _any;
        signal = signal.upper();

        # Ja existe signals registrados com esse nome
        if( signal in self.signals ):
            try:
                for target in self.signals[signal]:
                    ref = target;
                    if( type(ref) is weakref.ref ):
                        ref = ref();

                    if id(listener) == id(ref) :
                        self.signals[signal].remove(target);
                    del ref;
                    del target;
            except ValueError: pass


    def dispatch(self, signal, *args, **kargs):
        """
        Dispatches a signal to all listeners, including broadcasters
        """
        if( signal is None or signal == _any ):
            raise DispatcherException("Invalid signal");
        signal = signal.upper();
        listeners = [];

        # Processa os ouvintes do sinal direto
        try:
            for target in self.signals[signal] :
                listeners.append(target);
        except KeyError as e: pass


        # Processa os ouvintes do sinal direto
        try:
            for target in self.signals[_any] :
                listeners.append(target);
        except KeyError as e: pass

        # Dispara os signals 
        for ref in set(listeners):
            # Convert the weak to real-reference
            if( type(ref) is weakref.ref ):
                ref = ref();

            try:
                ref(*args, **kargs);
            except Exception as e:
                print("ERROR", e);
            finally:
                del ref;
                del listener;
        del listeners;