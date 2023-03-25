from docx import Document

class Bill:
    # def __init__(self, date, contract_nr, name_and_surname, hours_in_constract, salary, schedule, payment_date, statement):
    #     self.date = None
    #     self.contract_nr = None
    #     self.name_and_surname = "Aleksandra Duda"
    #     self.hours_in_contract = None
    #     self.salary = None
    #     self.schedule = None
    #     self.payment_date = None
    #     self.statement = "X"

    def save_to_file(self):

        # Wczytaj plik DOC jako obiekt Document
        document = Document('bills/wzor.docx')

        # Znajdź tabelki w dokumencie
        tables = document.tables

        # Wstaw wartość do odpowiedniej komórki w wierszu z MIEJSCE_1
        for table in tables:
            for row in table.rows:
                for cell in row.cells:
                    print(cell.text)

                if 'Data wystawienia rachunku' in row.cells[0].text:
                    # Wstaw wartość do drugiej kolumny
                    row.cells[1].text = 'WARTOŚĆ'

        # Zapisz zmiany do pliku DOC
        document.save('bills/testy.docx')


Bill().save_to_file()