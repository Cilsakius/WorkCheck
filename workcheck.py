import calendar
import datetime
import os
import platform
import ast


class structure(): #denne klasse styrer struktur
    def menu(self):#denne metode styrer valg af menu
        self.system = platform.system()# henter navnet på computerens system i en string
        if self.system == "Windows": #hvis den string er windows
             self.clear = lambda: os.system('cls')#så kører brugeren windows og derfor rydder vi på denne måde                self.clear() #rydder pythons console
        elif self.system == "Linux":#hvis styresystemet er linux
            self.clear = lambda: os.system('clear')#ryddes der på denne måde
        while True: #infinite loop
            self.menuPick = input("Choose a menu by typing the corresponding number \n1 - Check pay \n2 - Set settings \n3 - Show settings \n")# henter et menuinput
            if self.menuPick == "1": #hvis input er 1
                if filing.fileRead(10) == "True\n": # hvis  fileread(6) retunerer som stringen true
                    self.clear() #ryd compiler
                    start.workMenu() # kør workMenu
                else: #ellers
                    print("\nERROR - You have not set your settings yet\n") # print en fejlbesked
            elif self.menuPick == "2": # hvis input er 2
                self.clear() #ryd
                start.settingMenu() #kør settingMenu
            elif self.menuPick == "3": #hvis input er 3
                if filing.fileRead(10) == "True\n": #hvis fileread(6) er sand betyder det at brugeren har sat sine settings
                    self.clear()
                    output.settingsset() #kør settingsset
                else: # ellers print en fejlbesked
                    print("\nERROR - You have not set your settings yet\n")
            else: # hvis der ikke er blevet skrevet et tal der passer til en menu
                self.clear() # ryd compiler
                print("\nERROR - Only type 1, 2 or 3 \n") # print fejlbesked

    def settingMenu(self): # denne metode styrer hvilke metoder der kaldes for at sætte settings
        inputs.settingsPay()
        inputs.settingsHoleday()
        if inputs.settings1Hourday() == True: # hvis denne metode retunere true
            inputs.settings2Hourday() #kør denne metode

    def workMenu(self): # denne metode styrer hvilke metoder der kaldes for at udregne løn
        #et eksempel på formatet der regnes løn ud fra kunne være 05-10,07:20-13:50,00:30,0
        self.outputLists = [[],[],[]] #laver nested lists til penge,pause,timer
        self.workDayList = inputs.workInputs() #denne variabel fyldes med det der retunerer fra workInputs som her er en liste over arbejdsdage
        if self.workDayList:
            self.listNumber = len(self.workDayList)-1 #skaber en variabel som er det samme som det antal af elemeter i ovenstående liste
            for item in self.workDayList: #for hvert element i listen
                self.splittedlist = split.main(str(self.workDayList[self.listNumber]), ",")# kør funktionen split.main med elementet med nummeret listnumber fra worklist konverteret til en string
                #nu er formatet en liste og ser sådan ud 05-10 07:20-13:50 00:30 0
                self.splittedHours = split.main(self.splittedlist[1], '-') #splitter et element fra en liste fra HH:MM-HH:MM til 'HH:MM','HH:MM'
                self.addPay = calculate.addPayCheck(self.splittedlist[0],self.splittedlist[1], calculate.holidayCheck(self.splittedlist[3]), datetime.datetime.now().year) #denne variabel indholder en float værdi som udregnes af addPayCheck
                self.decimalDeltaTime = calculate.timeDecimal(calculate.timeDif(self.splittedHours[0],self.splittedHours[1]))#denne variabel indeholder tidsdifferencen(som der modtages som parameter) konverteret til decimaler
                self.pauseDecimal = calculate.timeDecimal(self.splittedlist[2]+":00")#denne variabel indeholder pausen omregnet til decimaler
                self.dayTuple = calculate.oneDay(self.decimalDeltaTime, self.pauseDecimal, self.addPay)#denne tuple indeholder 3 elementer som nedenfor appendes til den korrekte liste
                self.outputLists[0].append(self.dayTuple[0])#append timer
                self.outputLists[1].append(self.dayTuple[1])#append pause
                self.outputLists[2].append(self.dayTuple[2])#append timer
                self.listNumber -= 1 # gør listnumber en mindre
            start.clear()#ryd compiler
            self.totalTuple = calculate.total(self.outputLists[0], self.outputLists[1], self.outputLists[2])#udregn totalet
            output.outputs(self.totalTuple[0], self.totalTuple[2], self.totalTuple[1])
        else:
            start.clear()

class splitting():  #denne klasse splitter linjer
    def main(self, string, seperator):#denne metode modtager en string og en seperator og splitter derefter stringen ud til en liste
        self.list = list(string.split(seperator))#splitter den indkomne string ved hvert komma (den string der kommer ind bør gerne have formatet dd-mm,TT:MM-TT:MM,TT:MM,S)
        return self.list

class calculating(): #denne klasse udregner
    def WeekdayCheck(self, listDate, currentYear): #Denne metode tjekker ugedagen som den indtastede dato er og retunerer den
        self.dateSplit = split.main(listDate, '-') #splitter listdate til dato og måned
        self.weekDay = calendar.weekday(int(currentYear), int(self.dateSplit[1]), int(self.dateSplit[0])) #finder ud af hvilken ugedag det er ud fra datoen givet
        return self.weekDay

    def addPayCheck(self, date, shiftHours, holidayBool, currentYear): #denne metode udregner ekstra tillæg og retunerer det
        self.totalAddPay = 0
        self.weekDay = calculate.WeekdayCheck(date, currentYear) #denne variabel indeholder et tal der repræsenterer en ugedag, 0=mandag og 6=søndag
        self.dayHour1 = split.main(filing.fileRead(6), '-')#indeholder tidspunkter for specialtid som brugeren har sat i settings
        self.dayHour2 = split.main(filing.fileRead(9), '-') #indeholder et andet tidspunkter for specialtid
        self.shift = split.main(shiftHours, '-') #denne variavel indeholder en liste over hvornår der mødes [0] og hvornår der er fyraften [1]
        if holidayBool == True or filing.fileRead(2) != "null" and self.weekDay == int(filing.fileRead(2)): #hvis parammeteret holidayBool er sand eller ugedagen er det samme som fileread(2)
            self.delta = calculate.timeDecimal(calculate.timeDif(self.shift[0],self.shift[1]))#udregn tidsdifferencen mellem hvornår der mødtes på arbejde og hvornår der er fyraften, dette kunne egentligt bare modtages i parameteren da det allerede er udregnet
            self.totalAddPay = self.delta * filing.fileRead(3)#udregner det totale tillæg ud fra tidsdecimalerne og lønningen
        elif filing.fileRead(4) != "null" and self.weekDay in filing.fileRead(5): # hvis den givne dag er i listen af dage og dermed er omfattet af specielløn
            if self.dayHour1[0] < self.shift[0] < self.dayHour1[1] and self.dayHour1[0] < self.shift[0] < self.dayHour1[1]: #hvis både mødetiden og fyraften ligger inden for de specielle løntimer
                self.delta = calculate.timeDecimal(calculate.timeDif(self.shift[0], self.shift[1])) #udregn tiden mellem fremmøde og fyraften
            elif self.dayHour1[0] < self.shift[0] < self.dayHour1[1] and self.shift[0] > self.dayHour1[1]: #hvis fyraften er større end specieltid og mødetid er imellem
                self.delta = calculate.timeDecimal(calculate.timeDif(self.shift[0], self.dayHour1[1])) #udregn tiden mellem fremmøde og tiden specieltid slutter
            elif self.shift[0] < self.dayHour1[0] and self.dayHour1[0] < self.shift[0] < self.dayHour1[1]: #hvis mødetid er før specieltid og fyraften er imellem
                self.delta = calculate.timeDecimal(calculate.timeDif(self.dayHour1[0],self.shift[1])) #udregn tiden mellem specieltids start og fyraften
            elif self.shift[0] < self.dayHour1[0] and self.shift[1] > self.dayHour1[1]:# hvis mødetid er før specieltid og fyraften er efter
                self.delta = calculate.timeDecimal(calculate.timeDif(self.dayHour1[0], self.dayHour1[1]))# udregn tiden mellem specieltids start og slut
            self.totalAddPay = self.delta * filing.fileRead(4)#udregn det totale tillæg ud fra tidsdecimalet * lønningen
            #ellers rammer hverken mødetid eller fyraften tidsrummet omkring specialtid og så skal der ikke tilføjes ekstra timeløn
        elif filing.fileRead(7) != "null" and self.weekDay in filing.fileRead(8): # hvis den givne dag er i listen af dage og dermed er omfattet af specielløn
            if self.dayHour2[0] < self.shift[0] < self.dayHour2[1] and self.dayHour2[0] < self.shift[0] < self.dayHour2[1]: #hvis både mødetiden og fyraften ligger inden for de specielle løntimer
                self.delta = calculate.timeDecimal(calculate.timeDif(self.shift[0], self.shift[1]))#udregn tiden mellem fremmøde og fyraften
            elif self.dayHour2[0] < self.shift[0] < self.dayHour2[1] and self.shift[0] > self.dayHour2[1]: #hvis fyraften er større end specieltid og mødetid er imellem
                self.delta = calculate.timeDecimal(calculate.timeDif(self.shift[0], self.dayHour2[1]))#udregn tiden mellem fremmøde og tiden specieltid slutter
            elif self.shift[0] < self.dayHour2[0] and self.dayHour2[0] < self.shift[0] < self.dayHour2[1]: #hvis mødetid er før specieltid og fyraften er imellem
                self.delta = calculate.timeDecimal(calculate.timeDif(self.dayHour2[0],self.shift[1]))#udregn tiden mellem specieltids start og fyraften
            elif self.time[0] < self.dayHour2[0] and self.shift[1] > self.dayHour2[1]:# hvis mødetid er før specieltid og fyraften er efter
                self.delta = calculate.timeDecimal(calculate.timeDif(self.dayHour2[0], self.dayHour2[1]))# udregn tiden mellem specieltids start og slut
            self.totalAddPay = self.delta * filing.fileRead(7)#udregn det totale tillæg ud fra tidsdecimalet * lønningen
        return self.totalAddPay#retuner tillægget

    def holidayCheck(self, boolInt): #denne metode tjekker om brugeren har angivet datoen som en helligdag
        if int(boolInt) == 1:#hvis boolInt er 1 returner sand ellers retuner falsk
            return True
        else:
            return False

    def timeDif(self, listTime1, listTime2):#denne metode udregner tidsdifferencen mellem hvornår der er mødt på arbejde og hvornår man har fri
        self.deltaTime = datetime.datetime.strptime(str(listTime2), '%H:%M') - datetime.datetime.strptime(str(listTime1), '%H:%M') #her udregner vi tidsdifferencen mellem de to tidspunkter
        #self.deltaTime er en variabel der indeholder tidsdifferencen mellem de to tidspunkter følger formattet: HH:MM:SS
        return self.deltaTime

    def timeDecimal(self, timedif): #denne metode her omregner tidsdifferencen til tidsdecimaler eks. går en time og 30 minutter fra 01:30 til 1,5
        (h, m, s) = str(timedif).split(':') #den modtagede parameter konverteres til string og splittes ud til en liste med (HH, MM, SS)
        self.decimalResult = int(h) + int(m) / 60 + int(s) / 3600 #her omregnes det hele til timedecimaler dvs 30 minutter = 0,5 timer
        return self.decimalResult

    def oneDay(self, hourDecimal, pauseDecimal, addPay): #denne metode udregner hvor mange penge der er tjent på vagten
        self.totalDayPay = filing.fileRead(1) * (hourDecimal - pauseDecimal) + addPay # ganger timeløn med arbejdsdecimalet og lægger parameteren der indeholder tillægsløn til
        return self.totalDayPay, pauseDecimal, hourDecimal # retunerer en tuple med hhv. dagens løn, pause holdt i decimaler og timer arbejdet i decimaler

    def total(self, payList, breakList, hoursList): #Denne metode udregner totaler
        self.totalPay = float(0)#sætter værdier til 0
        self.totalHours = float(0)
        self.totalBreak = float(0)
        self.x = len(payList)-1#denne variabel er lig med længden af paylist i realiteten kunne det også være en af de andre parameter, det betyder nemlig ikke noget idet de alle har samme længde
        for items in payList: #for hvert element i payList
            self.totalPay += float(payList[self.x]) #læg listens element på plads x til det totale og gør det samme nedenfor
            self.totalBreak += float(breakList[self.x])
            self.totalHours += float(hoursList[self.x])
            self.x -= 1#gør x mindre
        return self.totalPay, self.totalBreak, self.totalHours

class inputs(): #denne klasse samler inputs

    def workInputs(self):# denne metode samler input om hvor mange dage der er arbejdet og hvilke dage, den retunerer så elementerne i en liste
        self.antalDage = input('Input the amount of workdays\n') #få input om hvor mange antal arbejdsdage der er tale om
        while self.antalDage.isnumeric() != True: #imens ovenstående input ikke er et tal
            start.clear()
            print('\nERROR - Input only numbers!\n') #print fejlbesked
            self.antalDage = input('Input the amount of workdays\n') #få nyt input
        self.workList = [] #laver en tom liste
        if int(self.antalDage) > 0:
            print('Input according to the code dd-mm,HH:MM-HH:MM,HH:MM,B') #printer besked
            for x in range(int(self.antalDage)): #kører nedenstående den antal gange som tallet skrevet i antalDage
                self.check = input('') # få input
                while len(self.check) != 25: #er input ikke på 25 tegn
                    print('ERROR - Input according to the code') #print fejlbesked
                    self.check = input('')# Få nyt input
                self.workList.append(self.check) #tilføj til enden af listen workList
            return self.workList

    def settingsPay(self): #Denne metode samler input om hvad timelønnen er
        while True:#infinite loop
            self.pay = input("Input your hourly pay\n") #få input
            try:
                self.pay = float(self.pay)#prøv at gøre det til en float
            except ValueError: #medmindre der er en valueerror så print en fejlbesked
                print("\nERROR - Input only numbers and use dot as seperator!\n")
            else:#ellers
                start.clear() #ryd compiler
                filing.fileWrite(self.pay, "w")#skriv det ind i dokumenter, her med "w" som parameter da vi skal rydde dokumentet
                break#bryd loop

    def settingsHoleday(self): # denne metode samler input om en hel arbejdsdag med ekstra løn
        while True:#infinite loop
            self.specialPayDay = input("Do you have a regular weekday where you recieve additional hourly pay for the entire day? \nType the corresponding letter to choose answer \n0 - Monday\n1 - Tuesday\n2 - Wednesday\n3 - Thursday\n4 - Friday\n5 - Saturdat\n6 - Sunday\n7 - I do not\n")
            try: #prøv
                self.specialPayDay = int(self.specialPayDay)# at gøre input til en int
            except ValueError:#hvis det ikke kan
                print("\nERROR - Input only one number that corresponds to an answer!\n")#print fejlbesked
            else:
                while -1 < self.specialPayDay < 7: #hvis inputtet matcher en af de muligheder beskrevet før / hvis det er en int som er større end -1 og mindre end 7
                    self.specialPay = input("Input your additional hourly pay on this regular weekday\n")#få nyt input
                    try:#prøv
                        self.specialPay = float(self.specialPay)#at gøre det til en float
                    except ValueError:#medmindre at der er ValueError
                        print("\nERROR - Input only numbers and use dot as seperator!\n")#så print fejlbesked
                    else:#ellers
                        start.clear()#ryd compiler
                        filing.fileWrite(self.specialPayDay, "a")#skriv ind i dokumentet her med "a" som et parameter sådan så det bare tilføjes til sidst i dokumentet
                        filing.fileWrite(self.specialPay, "a")
                        break
                else:#ellers
                    start.clear()#ryd
                    filing.fileWrite("null", "a")#skriv null ind sådan så vores dokument altid overholder det samme antal linjer
                    filing.fileWrite("null", "a")
                    break
                break

    def settings1Hourday(self): # denne metode samler input omkring en dag hvor der modtages ekstra løn i nogle timer af dagen
        while True:#infinite loop
            self.amountOfDays1 = input("Do you have one or multiple days where you recieve additional pay based on the hour? \nIf so write the amount of days, else write 0\n")
            try: #prøv
                self.amountOfDays1 = int(self.amountOfDays1)# at gøre input til en int
            except ValueError:#hvis det ikke kan
                print("\nERROR - Input only one number that corresponds to an answer!\n")#print fejlbesked
            else:
                while 8 > self.amountOfDays1 > 0: # imens input er mellem 0 og 8
                    self.additionalPay1 = input("How much additional pay do you recieve on such a day\n")
                    try:#prøv at gøre variabel til en float
                        self.additionalPay1 = float(self.additionalPay1)
                    except ValueError:#medmindre der er ValueError
                        print("\nERROR - Input only numbers and use dot as seperator!\n")#så print en fejlbesked
                    else:#ellers
                        self.whatDaysList1 = []#lav en tom liste
                        print("input the number correlating to the days on which you recieve this pay - 0 is Monday and 6 is Sunday")
                        for x in range(int(self.amountOfDays1)): # kør det antal gange som der blev skrevet i amountOfDays1
                            self.whatDays1 = input("") # få input
                            while self.whatDays1.isnumeric() == False or 6 < int(self.whatDays1) or int(self.whatDays1)< 0: # imens det ikke er et tal eller input er større end 6 eller mindre end 0
                                print("\nERROR - Try again\n")#print errrorcode
                                self.whatDays1 = input("input the number correlating to the days on which you recieve this pay - 0 is Monday and 6 is Sunday\n")#få input igen
                            else: #ellers
                                self.whatDaysList1.append(self.whatDays1) #tilføj talllet til listen
                        self.whatHour1 = input("Input which hours you recive the pay on these days - formatted HH:MM-HH:MM\n")#få input
                        while len(self.whatHour1) != 11:#imens input ikke er 11 tegn
                            print("\nERROR - Input according to format HH:MM-HH:MM\n")#print fejlbesked
                            self.whatHour1 = input("Input which hours you recive the pay on these days - formatted HH:MM-HH:MM\n")#få nyt input
                        start.clear()#ryd compiler
                        filing.fileWrite(self.additionalPay1, "a")#skriv data ind i dokumentet
                        filing.fileWrite(self.whatDaysList1, "a")
                        filing.fileWrite(self.whatHour1, "a")
                        return True #og retuner True
                else:#ellers
                    start.clear()#ryd
                    filing.fileWrite("null","a")#tilføj en masse linjer af "null" til dokumentet
                    filing.fileWrite("null","a")
                    filing.fileWrite("null","a")
                    filing.fileWrite("null","a")
                    filing.fileWrite("null","a")
                    filing.fileWrite("null","a")
                    filing.fileWrite("True","a")#denne linje er true for at indikere at settings er blevet sat
                    return False#retuner False

    #nedenstående metode er næsten identisk med ovenstående metode hvilket er derfor at den nedenstående metode kun kaldes hvis brugeren overhovedet gør brug af den ovenstående
    def settings2Hourday(self):# denne metode samler input omkring en anden dag hvor der modtages ekstra løn i nogle timer af dagen
        while True:#infinite loop
            self.amountOfDays2 = input("Do you have yet another day or multiple days where you recieve additional pay based on the hour \nIf so write the amount of days, else write 0\n") #har du aftenløn
            try: #prøv
                self.amountOfDays2 = int(self.amountOfDays2)# at gøre input til en int
            except ValueError:#hvis det ikke kan
                print("\nERROR - Input only one number that corresponds to an answer!\n")#print fejlbesked
            else:
                while 8 > int(self.amountOfDays2) > 0: # hvis input er mellem 0 og 8
                    self.additionalPay2 = input("How much additional pay do you recieve on such a day\n")
                    try:
                        self.additionalPay2 = float(self.additionalPay2)
                    except ValueError:
                        print("\nERROR - Input only numbers and use dot as seperator!\n")
                    else:
                        self.whatDaysList2 = []
                        print("input the number correlating to the days on which you recieve this pay - 0 is Monday and 6 is Sunday")
                        for x in range(int(self.amountOfDays2)):
                            self.whatDays2 = input("")
                            while self.whatDays2.isnumeric() == False or 6 < int(self.whatDays2) or int(self.whatDays2)< 0: # imens det ikke er et tal eller input er større end 6 eller mindre end 0
                                print("\nERROR - Try again\n")
                                self.whatDays2 = input("input the number correlating to the days on which you recieve this pay - 0 is Monday and 6 is Sunday\n")
                            else:#ellers
                                self.whatDaysList2.append(self.whatDays2) #tilføj tallet bagerst til listen
                        self.whatHour2 = input("Input which hours you recive the pay on these days - formatted HH:MM-HH:MM\n")
                        while len(self.whatHour2) != 11:
                            print("\nERROR - Input according to format HH:MM-HH:MM\n")
                            self.whatHour2 = input("Input which hours you recive the pay on these days - formatted HH:MM-HH:MM\n")
                        start.clear()
                        filing.fileWrite(self.additionalPay2,"a")
                        filing.fileWrite(self.whatDaysList2,"a")
                        filing.fileWrite(self.whatHour2,"a")
                        filing.fileWrite("True","a")
                        break
                else:
                    start.clear()
                    filing.fileWrite("null","a")
                    filing.fileWrite("null","a")
                    filing.fileWrite("null","a")
                    filing.fileWrite("True","a")
                break


class filing():#denne klasse håndterer filer

    def fileWrite(self,input,openType):# denne metode kaldes med 2 parameter, en string som der skal gemmes og en opentype som f.eks. kan være "w" hvor den så overskriver dokumentet eller "a" hvor den så appender til dokumentet
        self.Sfile = open("settings.txt", openType) #åbner filen settings.txt for at gøre hvad end der står i opentype typisk vil det her være "w" for write eller "a" for append
        self.Sfile.write(str(input))#skriv stringen ind
        self.Sfile.write("\n")#gå ned på en ny linje
        self.Sfile.close()#luk dokumentet

    def fileRead(self,line):#denne metode læser dokumentet og retunerer en bestemt linje som den har modtaget som parameter
        try:
            self.Sfile = open("settings.txt", "r") # åbner dokumentet med "r" som står for read
        except FileNotFoundError:
            start.clear()
            return None
        else:
            self.Sfile1 = self.Sfile.readline() #her læser vi den første linje
            self.Sfile2 = self.Sfile.readline() #så den anden
            self.Sfile3 = self.Sfile.readline() #tredje
            self.Sfile4 = self.Sfile.readline() #osv.
            self.Sfile5 = self.Sfile.readline() #desværre har jeg ikke kunnet finde en måde at få python til at læse specifikke linjer, det ville ellers have været mere praktisk
            self.Sfile6 = self.Sfile.readline()
            self.Sfile7 = self.Sfile.readline()
            self.Sfile8 = self.Sfile.readline()
            self.Sfile9 = self.Sfile.readline()
            self.Sfile10 = self.Sfile.readline()
            #herunder er der en masse if statements der alle sammen gør mere eller mindre det samme
            if line == 1: # hvis parameteret modtaget er 1
                if self.Sfile1 == "null\n": #hvis self.sfilex er  == "null\n"
                    self.RSfile = "null"#gør rsfile til "null"
                else:#ellers
                    self.RSfile = float(self.Sfile1)# gør rsfile til indholdet af sfilex men konverteret til den rigtige type. I dette tilfælde er det en float
            elif line == 2:
                if self.Sfile2 == "null\n":
                    self.RSfile = "null"
                else:
                    self.RSfile = int(self.Sfile2) #her er det en int
            elif line == 3:
                if self.Sfile3 == "null\n":
                    self.RSfile = "null"
                else:
                    self.RSfile = float(self.Sfile3)#float
            elif line == 4:
                if self.Sfile4 == "null\n":
                    self.RSfile = "null"
                else:
                    self.RSfile = float(self.Sfile4)
            elif line == 5:
                if self.Sfile5 == "null\n":
                    self.RSfile = "null"
                else:
                    self.RSfile = ast.literal_eval(self.Sfile5) #konverterer listen gemt som string tilbage til en liste uden de overskydende tegn der ville være hvis man brugte strip() og scrape()
            elif line == 6:
                if self.Sfile6 == "null\n":
                    self.RSfile = "null"
                else:
                    self.RSfile = self.Sfile6#bevares som string
            elif line == 7:
                if self.Sfile7 == "null\n":
                    self.RSfile = "null"
                else:
                    self.RSfile = float(self.Sfile7)#float
            elif line == 8:
                if self.Sfile8 == "null\n":
                    self.RSfile = "null"
                else:
                    self.RSfile = ast.literal_eval(self.Sfile8)#konverterer listen gemt som string tilbage til en liste uden de overskydende tegn der ville være hvis man brugte strip() og scrape()
            elif line == 9:
                if self.Sfile9 == "null\n":
                    self.RSfile = "null"
                else:
                    self.RSfile = self.Sfile9#bevares som string
            elif line == 10: #denne linje behøver vi ikke tjekke om er null fordi hvis den ikke er true findes den ikke
                self.RSfile = self.Sfile10
            self.Sfile.close()#så lukker vi dokumentet
            return self.RSfile# og retunerer RSfile

class output():#denne klasse håndterer outputs

    def settingsset(self):#denne metode printer et output som er baseret ud fra settings
        print("Your regular hourly pay is", filing.fileRead(1),"\n")
        self.specialDay = filing.fileRead(2) #her lægges fileread(2) ned i en variabel hvilket gøres for at fileread(2) ikke skal kaldes flere gange
        if self.specialDay != "null":#hvis variablen ikke er "null"
            print("You recieve special pay on the whole weekday numbered",int(self.specialDay)+1,"\n-On this day you recieve an additional pay of", filing.fileRead(3),"\n")  #print settings
        else: #ellers print at brugeren ikke gør brug af disse settings
            print("you dont recieve special pay on any hole regular weekday")
        self.specialHour1Day = filing.fileRead(5)#her ligges fileread(5) også ned i en variabel af samme grund som før
        if self.specialHour1Day != "null": #hvis variablen ikke er "null"
            print("You recieve special pay on the weekday(s) numbered", self.specialHour1Day, "\n-On these days you recieve an additional pay of", filing.fileRead(4), "in the timespand", filing.fileRead(6))#print flere settings
            self.specialHour2Day = filing.fileRead(8)
            if self.specialHour2Day != "null":
                print("You recieve special pay on the weekday(s) numbered", self.specialHour2Day, "\n-On these days you recieve an additional pay of", filing.fileRead(7), "in the timespand", filing.fileRead(9))
        else:#ellers print at brugeren ikke gør brug af disse settings
            print("You dont recieve special pay based on the time of your work on any weekday\n")

    def outputs(self, totalPay, totalHours, totalBreak): # denne metode printer 3 modtagede parameter, pænt opsat
        print('In total you have worked', totalHours, 'hours\n')
        print('You have held', totalBreak, 'hours break\n')
        print('You have earned', totalPay,"\n")

start = structure()
split = splitting()
calculate = calculating()
inputs = inputs()
filing = filing()
output = output()
if __name__ == '__main__':
    start.menu()
