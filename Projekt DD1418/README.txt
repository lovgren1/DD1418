Jacob Gustavsson | jacgu@kth.se
Alex Lövgren | alexlov@kth.se
DD1418 - Projektarbete
2022-12-18
------------------------------------------ KLASSERNA: ------------------------------------------

1) ålder
2) avstånd 
3) datum
4) tid 
5) pengar 
6) övrigt 


------------------------------------------ FILERNA: ------------------------------------------


Det finns tre stycken huvudsakliga pythonfiler att köra:

1) ri_model.py
2) evaluate_ri_model.py 
3) rulebased_model.py


Utöver dessa tre filer finns det två komplementära filer;
1) count_classified_words.py 
2) getwiki.py

Det finns 1 textfil som används kontinuerligt:
1) classified_data.txt 

Utöver detta finns det en fil som innehåller de hämtade wikipedia-sidorna som använts till datasetet:
1) data

------------------------------------------ INSTRUKTION TILL FILER: ------------------------------------------


----------------- ri_model.py -----------------
I denna fil kan man testa maskininlärningsmodellen på egna meningar. 
Kör scriptet genom att köra igång filen.
- Vokabuläret för träningsdata byggs upp
- Ordvektorer skapas för samtliga numeriska uttryck och modellen tränas
- Därefter får användaren fritt skriva in sin input. 

Input: Valfri mening med numeriskt uttryck, enheter bör separeras från numeriska uttrycket med ett mellanslag. Exit för att avsluta programmet. 

Output: En lista med längd antalet förekomna numeriska uttryck. Där element 1 är predicerad klass för numeriskt uttryck 1, element 2 är predicerad klass för uttryck 2 osv..


----------------- evaluate_ri_model.py -----------------
I denna fil körs ri_model.py, men istället för att låta användaren skriva in meningar testas modellen på en större mängd data.
Kör scriptet genom att köra igång filen.
Användaren får i koden själv fylla i no_of_testlines, vilket bestämmer hur många rader av testdata som sparas för evaluering av modellen.

Input: -

Output: Index för de linjer i datasetet som används som testdata.
        Confusion matrix och classification report för körningen. 


----------------- rulebased_model.py -----------------
Denna fil kör och testar den regelbaserade modellen.
Kör scriptet genom att köra igång filen.
Användaren får själv bestämma om scriptet ska använda samma testdata som skrivits ut i evaluate_ri_model.py eller om det ska slumpas nya.
Om det ska slumpas nya får användaren själv fylla i no_of_testlines i filen.

Input: -

Output: Confusion matrix och classification report för körningen.


----------------- count_classified_words.py -----------------
Denna fil räknar hur många datapunkter som är klassificerade i vardera klass. 
Kör scriptet genom att köra igång filen.
Denna användes för att se till att fördelningen av klassificerade datapunkter var jämn

Input: -

Output: Mängden klassificerade datapunkter av varje enskild klass samt summan av alla klassificerade datapunkter.


----------------- getwiki.py -----------------
Denna fil användes för att hämta wikipedia-sidor. 
Användaren fyller i URL för den wikipedia-sida som ska hämtas, därefter blir den till en txt-fil i mappen.

Input: -

Output: -




------------------------------------------ FÖR DEN SOM VILL KLASSIFICERA FLER DATAPUNKTER: ------------------------------------------
1. Hämta wikipedia-sida eller annan sida med hjälp utav getwiki.py, fyll i vad txt-filen ska heta, exempelvis "random_indexing.txt".
2. I metoden text_gen i ri_model.py, fyll i manuellt vägen till "random_indexing.txt". (fname = "random_indexing.txt).
3. Kör metoden cn.classify_datapoints().
4. En syntax kommer upp där användaren lätt kan klassificera datapunkter med dess rätta klass.
5. Användaren kan när som helst avsluta klassificeringen och de dittills klassificerade datapunkterna fyller på classified_data.txt. 


