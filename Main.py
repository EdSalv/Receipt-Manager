from tkinter import Tk, Frame, Label, Button, Entry, ttk, Scrollbar, Toplevel, simpledialog, END, messagebox
from datetime import date
import sqlite3
import os

listCompany = []
listCompanyDate = []
listCompanyName = []
main_iid = None
main_row = None

file = open("ListStoredDatabases.txt", "r")
for line in file:
        if line != '' and line != '\n':
            #split line at comma delimiters
            listCompany = line.split(",")
file.close()

for index in range(len(listCompany)):
    if index % 2 == 0:
        listCompanyDate.append(listCompany[index])
    else:
        listCompanyName.append(listCompany[index])

def main_select(__):
    global main_iid, main_row
   
    #Store iid of user's selection
    main_iid = main_tview.selection()
    main_row = main_tview.index(main_iid)

def update_StoredDatabases():
    
    with open("ListStoredDatabases.txt", "w") as file:
        for index in range(len(listCompanyName)):
            if index == len(listCompanyName) - 1:
                file.write(listCompanyDate[index] + ',' + listCompanyName[index])
            else:
                file.write(listCompanyDate[index] + ',' + listCompanyName[index] + ',')

def update_treeview(tview):  
    #Clear tree view data
    for data in tview.get_children():
        tview.delete(data)
    
    if tview == main_tview:
        for index in range(len(listCompanyName)):
            date = listCompanyDate[index]
            name = listCompanyName[index]
            name = name[:len(name) - 3]
            tview.insert("", END, values = (date, name))
    
def add_company():
    
    name = simpledialog.askstring("Name", "Please enter your company name:") + ".db"
    
    today = date.today().strftime("%B %d %Y")
    
    if name in listCompanyName:
        messagebox.showerror("Receipt Manager", "Sorry, that company already exists. \nPlease enter a different name.")
    else:
        sqlite3.connect(name)
        initializeDatabase(name)
        listCompanyDate.append(today)
        listCompanyName.append(name)
        update_StoredDatabases()
        update_treeview(main_tview)

def initializeDatabase(name):
    #Initialize a database with two tables: to store receipts and the company's expense types
    conn = sqlite3.connect(name)
    c = conn.cursor()
    c.execute('''CREATE TABLE receipts (extype, subtype, details, amount, date)''')
    c.execute('''CREATE TABLE extypes (extype, subtype)''')
    conn.commit()
    conn.close()      
  
def delete_company():
    
    global main_iid, main_row
   
    #Display a message if the user has not selected a company
    if main_iid == None:
        messagebox.showinfo("Remove", "Please select a company.")
    else:
        #Get the values of the tview id and ask for confirmation
        values = main_tview.item(main_iid)['values']
        answer = messagebox.askyesno("Remove", 'Are you sure you want to delete ' + values[1] + '?')
       
        if answer == True:
            #Delete company database from folder
            os.remove(values[1] + '.db')
            
            #Delete the company from the tview and company list
            del listCompanyName[main_row]
            del listCompanyDate[main_row]
           
        #Reset selected iid
        main_iid = None
        main_row = None
           
    #Update tview
    update_treeview(main_tview)
    update_StoredDatabases()
    
def open_company():
    main_to_company()
    
    #Display a message if the user has not selected a company
    if main_iid == None:
        messagebox.showinfo("Open", "Please select a company.")
    else:
        #Get the values of the tview id and store company to be opened
        values = main_tview.item(main_iid)['values']
        print(values[1])
        
        
    
    


def openDatabase():
    #Connect to database and store all receipts by creating receipt class objects 
    conn = sqlite3.connect('receipt.db')
    
        

def company_to_main():
    root.deiconify()
    root_company.withdraw()
    
def main_to_company():
    root_company.deiconify()
    root.withdraw()
    
def company_to_receipt():
    root_receipt.deiconify()
    root_company.withdraw()
    
def receipt_to_company():
    root_company.deiconify()
    root_receipt.withdraw()

def company_to_types():
    root_types.deiconify()
    root_company.withdraw()
    
def types_to_company():
    root_company.deiconify()
    root_types.withdraw()
    
root = Tk()
root.title("Receipt Manager")
root.geometry('%dx%d+%d+%d' % (600, 400, root.winfo_screenwidth() // 2 - 300, root.winfo_screenheight() // 2 - 200))
root.resizable(False, False)

main_frame = Frame(root)
main_frame.pack()
main_lblTitle = Label(main_frame, text = 'Welcome!\nPlease Select Your Company')
main_lblTitle.grid(column = 0, row = 0, columnspan = 3, padx = 10, pady = 10)
main_tview = ttk.Treeview(main_frame, selectmode = 'browse', columns = ('1', '2'), show = 'headings', height = 10, style = 'mystyle.Treeview')
main_tview.grid(column = 0, row = 1, columnspan = 3, padx = 10, pady = 10)
main_headingtext = ('DATE CREATED', 'COMPANY NAME')
main_columnwidths = [150, 250]
for i in range(2):
    main_tview.column(str(i + 1), width = main_columnwidths[i], anchor = 'w')
    main_tview.heading(str(i + 1), text = main_headingtext[i], anchor = 'w')
main_vscroll = Scrollbar(main_frame, orient = 'vertical', command = main_tview.yview)
main_vscroll.grid(column = 3, row = 1, sticky = 'ns')
main_tview.configure(yscrollcommand = main_vscroll.set)
main_btnAddCompany = Button(main_frame, text = 'ADD', width = 15, command = add_company)
main_btnOpenCompany = Button(main_frame, text = 'OPEN', width = 15, command = open_company)
main_btnDeleteCompany = Button(main_frame, text = 'DELETE', width = 15, command = delete_company)
main_btnAddCompany.grid(column = 0, row = 2, padx = 5, pady = 10)
main_btnOpenCompany.grid(column = 1, row = 2, padx = 5, pady = 10)
main_btnDeleteCompany.grid(column = 2, row = 2, padx = 5, pady = 10)

root_company = Toplevel(padx = 10, pady = 10)
root_company.title('Company Name')
root_company.resizable(False, False)
root_company.protocol('WM_DELETE_WINDOW', company_to_main)
root_company.geometry('%dx%d+%d+%d' % (800, 600, root.winfo_screenwidth() // 2 - 400, root.winfo_screenheight() // 2 - 300))
root_company.withdraw()
company_frame = Frame(root_company)
company_frame.pack()
company_lblTitle = Label(company_frame, text = 'COMPANY NAME')
company_lblTitle.grid(column = 0, row = 0, columnspan = 3, padx = 10, pady = 10)
company_tview = ttk.Treeview(company_frame, selectmode = 'browse', columns = ('1', '2', '3', '4', '5'), 
                             show = 'headings', height = 20, style = 'mystyle.Treeview')
company_tview.grid(column = 0, row = 1, columnspan = 2, padx = 10, pady = 10)
company_headingtext = ('EXPENSE TYPE', 'SUBTYPE', 'DETAILS', 'DATE', 'AMOUNT')
company_columnwidths = [150, 100, 200, 100, 150]
for i in range(5):
    company_tview.column(str(i + 1), width = company_columnwidths[i], anchor = 'w')
    company_tview.heading(str(i + 1), text = company_headingtext[i], anchor = 'w')
company_vscroll = Scrollbar(company_frame, orient = 'vertical', command = company_tview.yview)
company_vscroll.grid(column = 3, row = 1, sticky = 'ns')
company_tview.configure(yscrollcommand = company_vscroll.set)
company_buttonframe = Frame(company_frame)
company_buttonframe.grid(column = 0, row = 2)
company_btnAdd = Button(company_buttonframe, text = 'ADD', width = 10, command = company_to_receipt)
company_btnEdit = Button(company_buttonframe, text = 'EDIT', width = 10, command = company_to_receipt)
company_btnDelete = Button(company_buttonframe, text = 'DELETE', width = 10)
company_btnSetTypes = Button(company_buttonframe, text = 'SET TYPES', width = 10, command = company_to_types)

company_btnAdd.grid(column = 0, row = 0, padx = 5, pady = 5)
company_btnEdit.grid(column = 0, row = 1, padx = 5, pady = 5)
company_btnDelete.grid(column = 1, row = 1, padx = 5, pady = 5)
company_btnSetTypes.grid(column = 1, row = 0, padx = 5, pady = 5)
company_summaryframe = Frame(company_frame)
company_summaryframe.grid(column = 1, row = 2)

def setDays():
    global monthSelect, days
    month = months_name.index(monthSelect)
    days = []
    if month == 1:
        for i in range(1, 29):
            days.append(i)
    else:
        if month == 0 or month == 2 or month == 4 or month == 6 or month == 7  or month == 9 or month == 11:
            for i in range(1, 32):
                days.append(i)
        else:
            for i in range(1, 31):
                days.append(i)

def setYears():
    global currentYear, years
    startYear = currentYear - 10
    endYear = currentYear + 10 + 1
    years = []
    for i in range(startYear, endYear):
        years.append(i)

months_name = ('January', 'February', 'March', 'April', 'May', 'June', 'July', 'August', 'September', 'October', 'November', 'December')
days = []
monthSelect = months_name[1]
setDays()

years = []

today = date.today()
# Textual month, day and year    
currentYear = int(today.strftime("%Y"))
setYears()

summary_lblFrom = Label(company_summaryframe, text = 'FROM:')
summary_month1 = ttk.Combobox(company_summaryframe, state = "readonly", width = 10, values = months_name)
summary_day1 = ttk.Combobox(company_summaryframe, state = "readonly", width = 3, values = days)
summary_year1 = ttk.Combobox(company_summaryframe, state = "readonly", width = 5, values = years)
summary_lblTo = Label(company_summaryframe, text = 'TO:')
summary_month2 = ttk.Combobox(company_summaryframe, state = "readonly", width = 10, values = months_name)
summary_day2 = ttk.Combobox(company_summaryframe, state = "readonly", width = 3, values = days)
summary_year2 = ttk.Combobox(company_summaryframe, state = "readonly", width = 5, values = years)
summary_lblExType = Label(company_summaryframe, text = 'EXPENSE TYPE:')
summary_ExType = ttk.Combobox(company_summaryframe, state = "readonly", width = 20)
summary_btnFilter = Button(company_summaryframe, text = 'FILTER', width = 7)
summary_btnSummary = Button(company_summaryframe, text = 'SHOW SUMMARY', width = 17)
summary_lblFrom.grid(column = 0, row = 0, padx = 5, pady = 10)
summary_month1.grid(column = 1, row = 0, padx = 5, pady = 10)
summary_day1.grid(column = 2, row = 0, padx = 5, pady = 10)
summary_year1.grid(column = 3, row = 0, padx = 5, pady = 10)
summary_lblTo.grid(column = 4, row = 0, padx = 5, pady = 10)
summary_month2.grid(column = 5, row = 0, padx = 5, pady = 10)
summary_day2.grid(column = 6, row = 0, padx = 5, pady = 10)
summary_year2.grid(column = 7, row = 0, padx = 5, pady = 10)
summary_lblExType.grid(column = 0, row = 1, columnspan = 2, padx = 5, pady = 10, sticky = "w")
summary_ExType.grid(column = 1, row = 1, columnspan = 3, padx = 5, pady = 10, sticky = "e")
summary_btnFilter.grid(column = 5, row = 1, columnspan = 7, padx = 5, pady = 10, sticky = "w")
summary_btnSummary.grid(column = 5, row = 1, columnspan = 7, padx = 5, pady = 10, sticky = "e")

root_receipt = Toplevel(padx = 10, pady = 10)
root_receipt.title('Receipt')
root_receipt.resizable(False, False)
root_receipt.protocol('WM_DELETE_WINDOW', receipt_to_company)
root_receipt.geometry('%dx%d+%d+%d' % (400, 350, root.winfo_screenwidth() // 2 - 200, root.winfo_screenheight() // 2 - 175))
root_receipt.withdraw()
receipt_frame = Frame(root_receipt)
receipt_frame.pack()
receipt_lblTitle = Label(receipt_frame, text = 'COMPANY NAME')
receipt_lblExType = Label(receipt_frame, text = 'EXPENSE TYPE')
receipt_lblSubType = Label(receipt_frame, text = 'SUBTYPE')
receipt_lblDetails = Label(receipt_frame, text = 'DETAILS')
receipt_lblDate = Label(receipt_frame, text = 'DATE')
receipt_lblAmount = Label(receipt_frame, text = 'AMOUNT')
receipt_btnAdd = Button(receipt_frame, text = 'ADD RECEIPT', width = 15)
receipt_btnClear = Button(receipt_frame, text = 'CLEAR', width = 15)
receipt_ExType = ttk.Combobox(receipt_frame, state = "readonly", width = 30)
receipt_SubType = ttk.Combobox(receipt_frame, state = "readonly", width = 30)
receipt_Details = Entry(receipt_frame, width = 30)
receipt_DateMonth = ttk.Combobox(receipt_frame, state = "readonly", width = 10, values = months_name)
receipt_DateDay = ttk.Combobox(receipt_frame, state = "readonly", width = 3, values = days)
receipt_DateYear = ttk.Combobox(receipt_frame, state = "readonly", width = 5, values = years)
receipt_Amount = Entry(receipt_frame, width = 30)
receipt_lblTitle.grid(column = 0, row = 0, columnspan = 5, padx = 5, pady = 10)
receipt_lblExType.grid(column = 0, row = 1, padx = 5, pady = 10, sticky = "w")
receipt_lblSubType.grid(column = 0, row = 2, padx = 5, pady = 10, sticky = "w")
receipt_lblDetails.grid(column = 0, row = 3, padx = 5, pady = 10, sticky = "w")
receipt_lblDate.grid(column = 0, row = 4, padx = 5, pady = 10, sticky = "w")
receipt_lblAmount.grid(column = 0, row = 5, padx = 5, pady = 10, sticky = "w")
receipt_btnAdd.grid(column = 0, row = 6, columnspan = 4, padx = 5, pady = 10, sticky = "w")
receipt_btnClear.grid(column = 3, row = 6, columnspan = 4, padx = 5, pady = 10, sticky = "w")
receipt_ExType.grid(column = 1, row = 1, columnspan = 4, padx = 5, pady = 10, sticky = "w")
receipt_SubType.grid(column = 1, row = 2, columnspan = 4, padx = 5, pady = 10, sticky = "w")
receipt_Details.grid(column = 1, row = 3, columnspan = 4, padx = 5, pady = 10, sticky = "w")
receipt_DateMonth.grid(column = 2, row = 4, padx = 5, pady = 5, sticky = "w")
receipt_DateDay.grid(column = 3, row = 4, padx = 5, pady = 5, sticky = "w")
receipt_DateYear.grid(column = 4, row = 4, padx = 5, pady = 5, sticky = "w")
receipt_Amount.grid(column = 2, row = 5, columnspan = 4, padx = 5, pady = 10, sticky = "w")

root_types = Toplevel(padx = 10, pady = 10)
root_types.title("Set Expense Types")
root_types.resizable(False, False)
root_types.protocol("WM_DELETE_WINDOW", types_to_company)
root_types.geometry('%dx%d+%d+%d' % (400, 350, root.winfo_screenwidth() // 2 - 200, root.winfo_screenheight() // 2 - 175))
root_types.withdraw()
types_frame = Frame(root_types)
types_frame.pack()
types_lblTitle = Label(types_frame, text = 'COMPANY NAME')
types_lblExType = Label(types_frame, text = 'EXPENSE TYPES:')
types_ExType = ttk.Combobox(types_frame, state = "readonly", width = 30)
types_tview = ttk.Treeview(types_frame, selectmode = 'browse', columns = ('1'), show = 'headings', height = 5, style = 'mystyle.Treeview')
types_tview.grid(column = 0, row = 2, columnspan = 2, padx = 10, pady = 10)
types_tview.column(1, width = 340, anchor = 'w')
types_tview.heading(1, text = 'SUBTYPE', anchor = 'w')
types_vscroll = Scrollbar(types_frame, orient = 'vertical', command = types_tview.yview)
types_vscroll.grid(column = 3, row = 2, sticky = 'ns')
types_tview.configure(yscrollcommand = types_vscroll.set)
types_btnAddEx = Button(types_frame, text = 'ADD EXPENSE TYPE', width = 20)
types_btnDeleteEx = Button(types_frame, text = 'DELETE EXPENSE TYPE', width = 20)
types_btnAddSub = Button(types_frame, text = 'ADD EXPENSE SUBTYPE', width = 20, state = "disabled")
types_btnDeleteSub = Button(types_frame, text = 'DELETE EXPENSE SUBTYPE', width = 20, state = "disabled")
types_lblTitle.grid(column = 0, row = 0, columnspan = 3, padx = 5, pady = 10)
types_lblExType.grid(column = 0, row = 1, padx = 5, pady = 10)
types_ExType.grid(column = 1, row = 1, padx = 5, pady = 10, sticky = 'e')
types_btnAddEx.grid(column = 0, row = 3, columnspan = 3, padx = 10, pady = 10, sticky = 'w')
types_btnDeleteEx.grid(column = 0, row = 3, columnspan = 3, padx = 10, pady = 10, sticky = 'e')
types_btnAddSub.grid(column = 0, row = 4, columnspan = 3, padx = 10, pady = 10, sticky = 'w')
types_btnDeleteSub.grid(column = 0, row = 4, columnspan = 3, padx = 10, pady = 10, sticky = 'e')


update_treeview(main_tview)

#Bind the TreeviewSelect event to the widget
main_tview.bind("<<TreeviewSelect>>", main_select)


root.mainloop()