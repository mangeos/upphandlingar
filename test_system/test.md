# Testning

## Kommandoradsalternativ

### -v eller --verbose
Öka detaljnivån för testutgången. Det här alternativet visar mer detaljer om varje test som körs, vilket kan vara användbart för att se exakt vad som händer.

```bash
python -m unittest -v test_system.test_system_manager
```

--------------------------------------------------------------------------------------------------------------------------------------------------------------------------

### -f eller --failfast
Avbryt vid första felet eller undantaget. Detta är användbart om du vill sluta köra tester så snart något går fel.

```bash
python -m unittest -f test_system.test_system_manager
```

--------------------------------------------------------------------------------------------------------------------------------------------------------------------------

### -c eller --catch
Fångar kontroll-C och visar en trevligare felrapport.

```bash
python -m unittest -c test_system.test_system_manager
```

--------------------------------------------------------------------------------------------------------------------------------------------------------------------------

### -b eller --buffer
Buffra testutgången. Testutgången kommer endast att visas om testet misslyckas eller skrivs ut efter att alla tester har körts. Detta kan göra det lättare att läsa testresultaten, särskilt om du har mycket utdata.

```bash
python -m unittest -b test_system.test_system_manager
```

--------------------------------------------------------------------------------------------------------------------------------------------------------------------------