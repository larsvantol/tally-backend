import re
from io import StringIO

import numpy as np
import pandas as pd

# from pdfminer.high_level import extract_text
from pdfminer.converter import TextConverter
from pdfminer.converter import TextConverter
from pdfminer.high_level import extract_text
from pdfminer.layout import LAParams
from pdfminer.pdfdocument import PDFDocument
from pdfminer.pdfinterp import PDFPageInterpreter, PDFResourceManager
from pdfminer.pdfpage import PDFPage
from pdfminer.pdfparser import PDFParser

from .models import Product


def read_makro_invoice(pdf_file):
    output_string = StringIO()
    parser = PDFParser(pdf_file)
    doc = PDFDocument(parser)
    rsrcmgr = PDFResourceManager()
    device = TextConverter(rsrcmgr, output_string, laparams=LAParams())
    interpreter = PDFPageInterpreter(rsrcmgr, device)
    for page in PDFPage.create_pages(doc):
        interpreter.process_page(page)
    lines = output_string.getvalue().splitlines()

    # find the line which contains the word "Factuurdatum"
    date_line = [i for i, line in enumerate(lines) if "Factuurdatum" in line][0]
    date_pattern = re.compile(r"\b\d{2}-\d{2}-\d{4}\b")
    invoice_date = date_pattern.search(lines[date_line]).group()

    # find the line which contains the word "Factuurnummer"
    invoice_num_line = [i for i, line in enumerate(lines) if "Factuurnummer" in line][0]
    invoice_number_pattern = re.compile(r"Factuurnummer:\s*(\S+)")
    invoice_number_string = invoice_number_pattern.search(lines[invoice_num_line]).group(1)

    invoice_data = {
        "invoice_number": invoice_number_string,
        "invoice_date": invoice_date,
    }

    # find the line which contains the word "Artikelnummer"
    start_line = [i for i, line in enumerate(lines) if "Artikelnummer" in line][0]

    # find the line which contains the word "Aantal stuks"
    end_line = [i for i, line in enumerate(lines) if "Aantal stuks" in line][0]

    # dataframe that will contain all articles and their information
    articles_dtypes = np.dtype(
        [
            ("Statiegeld", bool),
            ("Artikelnummer", str),
            ("Artikelomschrijving", str),
            ("Prijs st/kg", str),
            ("Stuks per eenheid", str),
            ("Prijs per collo", str),
            ("Aantal", str),
            ("Bedrag", str),
            ("BTW", str),
            ("Code korting", str),
            ("Prijs st/kg na korting", str),
        ]
    )
    articles = pd.DataFrame(np.empty(0, dtype=articles_dtypes))

    # go trough all lines containing articles and extract the information
    for i, line in enumerate(lines[start_line + 3 : end_line]):
        if "----------------" in line:
            end_articles = i
            break

        if not line == "" and not "ARTIKELEN---" in line:
            split_line = line.split()[::-1]
            article = pd.DataFrame(np.empty(1, dtype=articles_dtypes))

            first_entry = split_line.pop()
            if first_entry == "+":
                article["Artikelnummer"] = split_line.pop()
                article["Statiegeld"] = True
            else:
                article["Artikelnummer"] = first_entry
                article["Statiegeld"] = False

            # find stuks per eenheid indicator
            for i, entry in enumerate(split_line):
                if len(entry) == 2 and entry.isupper():
                    article["Stuks per eenheid"] = split_line[i + 1]
                    article["Prijs st/kg"] = split_line[i + 2]
                    article["Prijs per collo"] = split_line[i - 1]
                    article["Aantal"] = split_line[i - 2]
                    article["Bedrag"] = split_line[i - 3]
                    article["BTW"] = split_line[i - 4]
                    article["Artikelomschrijving"] = " ".join(split_line[: i + 2 : -1])

                    split_line = split_line[: i - 4]
                    if split_line[0] == "A":
                        split_line = split_line[1:]
                    if len(split_line) == 2:
                        article["Code korting"] = split_line[1]
                        article["Prijs st/kg na korting"] = split_line[0]
                    if len(split_line) == 1:
                        article["Code korting"] = ""
                        article["Prijs st/kg na korting"] = split_line[0]
                    break

            # append article to articles
            articles = pd.concat([articles, article], ignore_index=True)

    return invoice_data, articles


def to_list(df):
    result = []
    for index, row in df.iterrows():
        try:
            result.append({
                "article_number": int(row['Artikelnummer']),
                "name": row['Artikelomschrijving'], 
                "price": float(row['Prijs st/kg'].replace(',','.')), 
                "stock": int(float(row['Stuks per eenheid'].replace(',','.'))*int(row['Aantal'])),
                "product_group": 1,
                "vat_percentage": row['BTW']
            })
            result.append(
                {
                    "article_number": int(row["Artikelnummer"]),
                    "name": row["Artikelomschrijving"],
                    "price": float(row["Prijs st/kg"].replace(",", ".")),
                    "stock": int(
                        float(row["Stuks per eenheid"].replace(",", ".")) * int(row["Aantal"])
                    ),
                    "product_group": 1,
                }
            )
        except:
            continue
    return result


def filter_list(list):
    final_list = []
    for item in list:
        try:
            product = Product.objects.get(article_number=item["article_number"])
            new_item = {
                'article_number': product.article_number, 
                'name': product.name, 
                'price': product.price, 
                'stock': item['stock'], 
                'product_group': product.product_group,
                'vat_percentage': product.vat_percentage
                "article_number": product.article_number,
                "name": product.name,
                "price": product.price,
                "stock": item["stock"],
                "product_group": product.product_group,
            }
            final_list.append(new_item)
        except Product.DoesNotExist:
            final_list.append(item)
    return final_list
