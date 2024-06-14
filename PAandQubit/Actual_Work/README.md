## Useful links
>- IQ-Mixer (IQ0318): https://www.mwstore.com/static/download/catalog/0/IQ-0318.pdf
>- Cable (SUCOFLEX 104): https://www.limpulsion.fr/upload/docs/SUCOFLEX104.PDF
>- QuickSyn FSL001: http://ni-microwavecomponents.com/datasheets/QuickSyn_Brochure_Datasheet.pdf
>- https://arxiv.org/pdf/2310.05238
>- https://arxiv.org/pdf/1904.06560

1. Attraverso il VNA cerco la frequenza del risonatore. Potrei usarlo anche per fare la resonator spectroscopy. Connessione sulla linea di readout.
2. Attraverso il signal generator faccio la resonator spectroscopy e la punchout. Connessione sulla linea di readout. Il segnale nel GHz viene mandato al qubit+risonatore, ma siccome ci mettiamo ad alta potenza, il qubit si sovraeccita (si satura) e la frequenza del risonatore sarà la bare frequency, ossia la frequenza che avrebbe il risonatore preso singolarmente in assenza del qubit. Alla frequenza di risonanza, il risonatore assorbirà il segnale restituendo un'ampiezza più bassa. Questo segnale viene downconvertito per poter essere acquisito dalla scheda.
3. Per la qubit spectroscopy mando un segnale utilizzando il signal generator collegato alla line di drive con la frequenza di risonanza settata e facendo variare la potenza. Il signal generator è un ottimo strumento per l'impulso di drive perché è in grado di mandare impulsi con larghezza molto piccola (min 5ns). Per il readout usiamo l'awg per creare un'onda quadra che stabilica la larghezza del segnale che voglio mandare attraverso il quicksyn VALON (che lavora nel GHz). L'onda quadra e il quicksyn verranno combinati con iq-mixer in modalità di up conversion (Q col tappo, VALON in LO, awg in I e output in RF). C'è la possibilità di fare anche il contrario, ossia usare SG come read e VALON come drive. VEDREMO. NB: il segnale di drive non lo acquisiamo, quindi non è necessario downconvertirlo.


- cilindro di rame: utile perché...
- cilindro di schermo magnetico: per evitare che i campi magnetici interferiscano col sistema




---

offset: mi regola il leakedge della     LO
ampiezza:

guardare l'on off ratio


AWG:
- QSyn_freq = 8 GHz
- BEST OFFSET: 500 mV
- BEST AMPLITUDE: 990 mVpp
- IQMixer: 0318L