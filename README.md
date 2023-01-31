enkelt program for å øve til TIØ4105 Industriell Økonomisk Styring eksamen med MC-spørsmål. Bruk gjerne dataen som ligger under `resources` som dere selv ønsker. Øvinger, forelesningsmateriale for V22 er også med

antar at `python` og `pip` er installert

installer packagene som kreves ved:

1. ```pip install requirements.txt```

bygg appen med 

2. ```pyinstaller App.spec --noconfirm```

så kan appen kjøres. Den bør ligge under `/dist/App`

kun testet på Mac, hvis noen vil lage en PR for å sikre Windows-støtte kan de gjerne gjøre det. 
merk at alle referanser til filer sannsynsligvis må endres for å ikke først bygges med `pyinstaller` dersom appen skal testes uten å bygges
