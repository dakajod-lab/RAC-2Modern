# Så testar du RAC-2Modern

Den här guiden är för dig som testar. Du behöver inte koda någonting. Knapparna i OpenRACs launcher
heter samma sak här som i appen, alltså på engelska.

## Det här behöver du

- En dator med Windows, macOS eller Linux och ett grafikkort som klarar **Vulkan**. Det behövs för
  OpenRACs moderna grafik.
- Din egen skiva av *Ratchet & Clank 2: Locked and Loaded* (PAL) som en avbild, `.iso` eller
  `.chd`. Har du ingen avbild gör du en från skivan med en DVD-läsare, till exempel med ImgBurn
  på Windows ("Create image file from disc"). Ladda aldrig ner en avbild från nätet.

## 1. Installera OpenRAC och spela en gång

1. Ladda ner launchern från
   [OpenRACs releaser](https://github.com/OpenRAC/OpenRAC/releases/latest) och installera den.
2. Öppna den och välj mappen där skivavbilden ligger. Launchern känner igen skivan
   (Going Commando, Europe, `SCES_516.07`) och gör i ordning banorna.
3. Tryck **Play** och spela en stund. Kolla att allt fungerar innan du lägger till mods.

## 2. Slå på Enhanced graphics

Enhanced graphics är OpenRACs moderna renderer, med studsljus, mjuka skuggor och ambient occlusion.
RAC-2Modern bygger på den.

1. Gå till **Mods** → **My mods** och slå på raden **Enhanced graphics**.
2. Första gången räknar datorn fram ljuset för varje bana. **Lighting** på samma sida visar hur
   långt den har kommit. Vänta tills bana 0 (Aranos) och bana 1 (Oozla) är klara.
3. Syns inte raden? Slå på **developer tools** under **Settings** → **Launcher** och titta igen.

## 3. Lägg till RAC-2Modern

1. Gå till **Mods** → **Add from a link** och klistra in
   `https://github.com/dakajod-lab/RAC-2Modern`.
2. Välj **RAC-2Modern** och installera.
3. Kolla att RAC-2Modern är på och att reglaget **Mods** under **Play** är på. Tryck **Play**.

Launchern letar efter uppdateringar en gång om dagen. Du kan också trycka **Check for updates** på
Mods-fliken när jag säger att något nytt finns.

## 4. Det här vill jag ha tillbaka

Version 0.1.0 ändrar ingenting på skärmen ännu. Testet går ut på att se att kedjan fungerar och få
en jämförelse att utgå från.

1. **Laddades modden?** Står det något på RAC-2Moderns rad i launchern, till exempel ett fel?
2. **Loggen:** öppna spelets logg (**Logs**, under spelets saves) och kopiera raden där det står
   `rac2-modern`.
3. **Fyra skärmdumpar:** starten av Aranos och starten av Oozla, båda med Enhanced graphics av och
   på. Ta dem från samma ställe och samma vinkel, så att de går att jämföra.
4. **Din dator:** operativsystem och grafikkort, och om spelet flyter med Enhanced graphics på.

## 5. Inför nästa steg: exportera banorna

För att göra om banorna behöver jag se vad de består av.

1. Gå till **Mods** → **Models and textures** → **Export**, välj bana 0 och **everything**.
   Gör samma sak för bana 1.
2. Mapparna hamnar under `exports/` i spelets mapp (`level_00-…`, `level_01-…`). På Windows ligger
   OpenRAC i `%USERPROFILE%\OpenRAC` om du inte har valt något annat.

Filerna kommer från din skiva, så **lägg dem aldrig på GitHub**. Dela dem med mig privat, på något
av de här sätten:

- Zippa mapparna och ladda upp dem i chatten.
- Öppna chatten i Claude-appen på datorn och lägg till exportmappen med **+** → **Add folder**.
  Då läser jag filerna direkt.

## Om något går fel

- **Modden vägras:** skicka orsaken som står på dess rad.
- **Spelet kraschar eller ser trasigt ut:** skicka loggen och en skärmdump. Säg också om det
  händer utan RAC-2Modern. Är det fel även utan modden ligger felet i OpenRAC, och då rapporterar
  vi det till dem.
