from PyPDF2 import PdfReader
import pdfplumber
import spacy

class Extractor:
# creating a pdf reader object
    def __init__(self):
        self.reader = PdfReader('contracts/DR-Katowice-zlecUZ-Aleksandra-Duda-4449.pdf')
        self.nlp = spacy.load("pl_core_news_sm")  # załadowanie modelu języka polskiego
        # self.contract_headlines = ["ZLECENIE","DNIA", "(netto)","szkolenia" ,"wynagrodzenia"]
        self.schedule_dates = []


        self.page = self.reader.pages[0]
        self.content = self.page.extract_text()

    def get_schedule_dates(self):
        with pdfplumber.open("contracts/DR-Katowice-zlecUZ-Aleksandra-Duda-4449.pdf") as pdf:
            for page in pdf.pages:
                tables = page.extract_tables()
                for table in tables:
                    print(table)
                    # znajdź nagłówek "Data" w pierwszym wierszu tabeli
                    data_index = -1
                    for i, cell in enumerate(table[0]):
                        if cell and "Data" in cell:
                            data_index = i
                            print("test")
                            break
                    if data_index == -1:
                        print("test2")

                        continue

                    # wyświetl wartości w kolumnie "Data" dla pozostałych wierszy
                    for row in table[1:]:
                        print("test3")

                        data_cell = row[data_index]
                        print(data_cell)
                # przeszukaj wszystkie strony w poszukiwaniu tabel
        #     for page in pdf.pages:
        #         tables = page.find_tables()
        #         # przejdź przez znalezione tabele
        #         for table in tables:
        #             # wyświetl zawartość pierwszej kolumny
        #             for row in table.rows:
        #                 for cell in row.cells:
        #                     print(cell)
        # # Wyświetlenie danych z pierwszej kolumny


    def find_contract_headlines_values(self):
        for page_num in range(len(self.reader.pages)):
            page = self.reader.pages[page_num]
            content = page.extract_text()
            doc = self.nlp(content)
            print(content)

            headline_value = ''
            headline_values = {}
            for t, token in enumerate(doc):
                # print(token.text)

                if token.text == 'ZLECENIE':
                    for i in range(0, 3):
                        headline_value += doc[token.i + 1 + i].text
                        headline_value_shortened = headline_value[2:].replace('\n','')

                        for sign in headline_value_shortened.split():
                            if sign == "zdnia":
                                continue
                        headline_values[token.text] = headline_value_shortened
                    headline_value = ''

                if token.text == 'DNIA':
                    for i in range(0,5):
                        headline_value += doc[token.i+1+i].text
                        headline_values[token.text] = headline_value

                    headline_value=''
                if token.lower_ == 'netto':
                    for i in range(1,3):
                        headline_value += doc[token.i+1+i].text
                        headline_values[token.text] = headline_value

                    headline_value=''
                if token.text == 'godzin' and doc[token.i+1].text == 'szkolenia':
                    for i in range(0,1):
                        headline_value += doc[token.i+2+i].text
                        headline_values[token.text] = headline_value
                if token.text == 'ści' and doc[token.i+1].text == 'wynagrodzenia':
                    for i in range(1, 6):
                        headline_value += doc[token.i + 1 + i].text
                        headline_values["termin_płatności"] = headline_value

                    headline_value=''
            print(headline_values)


Extractor().find_contract_headlines_values()
# Extractor().get_schedule_dates()