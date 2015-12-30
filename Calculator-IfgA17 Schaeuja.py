#Author Jan Schäuble, Bearbeitung vom 23-30.12.15 Geschrieben mit Python 3.4.3
#Anleitung: Jedes Zeichen des Taschenrechners hat einen eigenen Knopf. Die Zahlen und Rechenoperatoren geben ihren Wert wieder. C löscht ein Zeichen, CE löscht die gesamte Zeile und = Berechnet das Ergebnis der Rechnung.
#!!!!!!!Achtung: Geben sie auf keine Fall Zeichen in die obere Anzeigeleiste des Rechners ein, es wird zu einem Absturz führen!!!!!!

from tkinter import *
import tkinter

    
class Calculator_App(tkinter.Frame):
        
	def __init__(self, master, **options):
		tkinter.Frame.__init__(self, master, options)
                #Der Grid Befehl ordnet das Fenster wie eine Tabelle an, sodass die Knöpfe mit Columns und Rows platziert werden können
		self.grid()
		self.add_Components()

	def add_Components(self):
                #Hier wird das aussehen der Leiste festgelegt, die oben die Zahlen anzeigen soll 
		self.display = tkinter.Entry(self,justify= 'right',bd=34,bg="white",textvariable=txtDisplay)	
		self.display.grid(column=0, row=0, columnspan=5, sticky="we")
                
                #eine Liste mit allen Zeichen, die sich auf Knöpfen befinden sollen
		buttons = ['1', '2', '3', '(', ')','4', '5', '6', ' * ', ' / ','7', '8', '9', ' +', ' -','.', '0','CE' ,'C','=']
                #Hier sind die Variablen für die Reihen und Säulen, in denen sich die Knöpfe später befinden sollen
		varColumn = -1
		varRow = 1
                #Für alle Knöpfe soll folgendes gelten:
		for button in buttons:
			varColumn += 1      
                        #Die Knöpfe haben folgende Eigenschaften:
			self.btnClick = ClickButtons(self,value=button,width=4,height=3,padx=16, pady=16, bd=8,
                                activebackground="#333333",activeforeground="#ffffff",                 
				text=button.replace(' ', ''),relief="raised", )
                        #Falls C oder CE gedrückt wird, dann soll die Methode Equals_Input verwendet werden
			if button == 'C':
				self.btnClick.configure(command=self.btnClick.Equals_Input)

			elif button == 'CE':
				self.btnClick.configure(command=self.btnClick.Equals_Input)
			#Falls = gedrückt wird, dann soll die Methode Answer_Output verwendet werden	
			elif button == '=':
				self.btnClick.configure(command=self.btnClick.Answer_Output)
				self.btnClick.grid(column=varColumn, row=varRow)
			#Falls irgendeine andere Taste gedrückt wird, dann soll die Addition_Input Methode verwendet werden.
			else:
				self.btnClick.configure(command=self.btnClick.Addition_Input)
                        
			self.btnClick.grid(column=varColumn, row=varRow)
                        #Falls sich ein Knopf an der 5. Stelle einer Reihe beinden sollte, dann wird er eine Reihe nach unten verschoben. 
			if varColumn == 4:
				varColumn = -1
				varRow += 1

class ClickButtons(tkinter.Button):
	def __init__(self, master, value=None, **options):
		tkinter.Button.__init__(self, master, options)
                #Der Wert eines Knopfes ist sein Zeichen, Außnahmen sind hierbei die C, CE und =.
		self.value = value
	#Wird ein Knopf gedrückt, soll dieser Standardmäßig oben in die Leiste hinzugefügt werden, undzwar als das Zeichen, was es darstellt
	def Addition_Input(self):
		global operator

		App_Function.display.config(fg="black")
		operator += self.value

		txtDisplay.set(operator.replace(' ', ''))

	def Equals_Input(self):
		global operator
                #Wenn die Textleiste nicht leer ist, so soll sie geleert werden.(Mit einem Tutorial aus dem Internet angefertigt)
		if not operator == "":

			selector = operator.split()[-1][-1]

			if selector == '*' or selector == '/':
				operator = operator[0:-3]
			elif selector == '+' or selector == '-':
				operator = operator[0:-2]
			else:
				operator = operator[0:-1]

			txtDisplay.set(operator.replace(' ', ""))
		else:
			txtDisplay.set(operator.replace(' ', ''))	
        #Diese Methode gibt das Ergebnis der Rechnug aus und löscht sämtliche vorige Zeichen in der Anzeigeleiste
	def Answer_Output(self):
		global operator

		App_Function.display.config(fg="black")

		DisplayAnswer = Functional_Output(operator)
                #Gibt das Ergebnis im Textfeld aus
		txtDisplay.set(DisplayAnswer)
                #Leert das Feld von Operatoren
		operator = ""

	                       
#Diese Methode versucht das Ergebnis der Rechnung auszugeben und gibt einen Error aus, falls die Rechnung durch falsche Zeicheneingabe etc. zu keinem Ergebnis kommt.(Auch hier Hilfe aus dem Internet)
def Functional_Output(Validate_Input):
	try:
		while '(' in Validate_Input and ')' in Validate_Input:
			Validate_Output = Validate_Input.count('(')

			Intake_Input = Validate_Input.find('(')	
			fin = Validate_Input.find(')')+1

			while Validate_Output > 1:
				Intake_Input = Validate_Input.find('(', Intake_Input+1) 
				Validate_Output -= 1

			receive_value = Validate_Input[Intake_Input:fin]
			receive_input = calcula(receive_value.replace('(', '').replace(')', ''))
			Validate_Input = Validate_Input.replace(receive_value, receive_input)

		DisplayAnswer = float(AddFunction(Validate_Input))
	except:
		DisplayAnswer = "Error"
        #Übergibt das Ergebnis der Rechnung
	return DisplayAnswer
#Diese Methode berechnet das Ergebnis der Rechnung, falls * in der Rechnung vor kommt, soll das vor und nach dem Zeichen stehende multipliziert werden, steht ein / in der Rechnung, so soll das vor dem / stehende durch das dahinter stehende geteilt werden, und keins der Zeichen in der Rechnung, so sollen die einzelnen Werte addiert werden.
def AddFunction(Validate_Input):
	add_selection = Validate_Input.split()

	while len(add_selection) != 1:
		#Der index zeigt hier, wo welches Zeichen steht
		for index in range(len(add_selection)):

			if add_selection[index] == '/':
				add_selection[index] = str(float(add_selection[index-1]) / float(add_selection[index+1]))

				add_selection.pop(index+1)
				add_selection.pop(index-1)
				break

			elif add_selection[index] == '*':
				add_selection[index] = str(float(add_selection[index-1]) * float(add_selection[index+1]))

				add_selection.pop(index+1)
				add_selection.pop(index-1)
				break

		if not '/' in add_selection and not '*' in add_selection:
			while len(add_selection) != 1:
				for index in range(len(add_selection)):
					add_selection[index] = str(float(add_selection[index]) + float(add_selection[index+1]))

					add_selection.pop(index+1)
					break
	#am Ende soll das Ergebnis übergeben werden			
	return add_selection[0]
	
root = tkinter.Tk()
#Dieser Befehl verhindert, dass die Fenstergröße angepasst werden kann.
root.resizable(0, 0)
#Gibt den Titel des Fensters an
root.title("Calculator")
txtDisplay = tkinter.StringVar()
#Das Feld soll beim Start der Anwedung leer sein
operator = ""
App_Function = Calculator_App(root)

root.mainloop()














