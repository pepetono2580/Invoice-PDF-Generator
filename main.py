import pandas as pd
import glob
from fpdf import FPDF
from pathlib import Path

filepaths = glob.glob("invoices/*.xlsx")

for filepath in filepaths:

    pdf = FPDF(orientation="P", unit="mm", format="A4")
    pdf.add_page()

    filename = Path(filepath).stem
    invoice_number, date = filename.split("-")

    pdf.set_font(family="Times", size=16, style="B")
    pdf.cell(w=50, h=8, txt=f"Invoice nr. {invoice_number}", ln=1)

    pdf.set_font(family="Times", size=16, style="B")
    pdf.cell(w=50, h=8, txt=f"Date {date}", ln=2)

    df = pd.read_excel(filepath, sheet_name="Sheet 1")

    # Add the headers
    headers = df.columns
    headers = [item.replace("_", " ").title() for item in headers]

    pdf.set_font(family="Times", size=10, style="B")
    pdf.set_text_color(80, 80, 80)
    pdf.cell(w=30, h=8, txt=str(headers[0]), border=1)
    pdf.cell(w=70, h=8, txt=str(headers[1]), border=1)
    pdf.cell(w=30, h=8, txt=str(headers[2]), border=1)
    pdf.cell(w=30, h=8, txt=str(headers[3]), border=1)
    pdf.cell(w=30, h=8, txt=str(headers[4]), border=1, ln=1)

    # Add rows to the table
    for index, row in df.iterrows():

        pdf.set_font(family="Times", size=10)
        pdf.set_text_color(80, 80, 80)
        pdf.cell(w=30, h=8, txt= str(row["product_id"]), border=1)
        pdf.cell(w=70, h=8, txt= str(row["product_name"]), border=1)
        pdf.cell(w=30, h=8, txt= str(row["amount_purchased"]), border=1)
        pdf.cell(w=30, h=8, txt= str(row["price_per_unit"]), border=1)
        pdf.cell(w=30, h=8, txt= str(row["total_price"]), border=1, ln=1)

    # Add sum of total price
    total_sum = df["total_price"].sum()
    pdf.set_font(family="Times", size=10)
    pdf.set_text_color(80, 80, 80)
    pdf.cell(w=30, h=8, txt="")
    pdf.cell(w=70, h=8, txt="")
    pdf.cell(w=30, h=8, txt="")
    pdf.cell(w=30, h=8, txt="")
    pdf.cell(w=30, h=8, txt=str(total_sum), border=1, ln=1)

    # Add total sum sentence
    pdf.set_font(family="Times", size=10, style="B")
    pdf.cell(w=30, h=8, txt=f"The total price is ${total_sum}", ln=1)

    #Add company name
    pdf.set_font(family="Times", size=14, style="B")
    pdf.cell(w=25, h=8, txt=f"PythonHow")
    pdf.image("pythonhow.png", w=10)

    pdf.output(f"PDFs/{filename}.pdf")
