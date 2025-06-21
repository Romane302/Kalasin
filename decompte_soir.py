import streamlit as st
from fpdf import FPDF
from datetime import date
from io import BytesIO

#formatting web page
left_co, cent_co,last_co = st.columns(3)
with last_co:
     st.image("images/logo.png", width=170)
with left_co: 
     st.title("Décompte du jour")


#definition of variables
CA=st.number_input("Chiffre d'affaire selon ticket")
CB1= st.number_input("Encaissé par carte avec machine 1")
CB2 = st.number_input("Encaissé par carte avec machine 2")
CB_sum = CB1 + CB2
CA_cash = CA-CB_sum
Bon_cash = st.number_input("Bons vendus par cash")
Bon_carte = st.number_input("Bons vendus par carte")
Bon_encaisse = st.number_input("Bons encaissé")
correction_bon= CA_cash + Bon_cash + Bon_carte - Bon_encaisse#a recontroler !!!!!!!

data1 = [["Chiffre d'affaire", CA],
        ["Chiffre d'affaire encaissé par carte", CB_sum],] 

data2 = [["Bons vendus par cash", Bon_cash],
         ["Bons vendus par carte", Bon_carte],
         ["Bons encaissés", Bon_encaisse]]

aujourdhui = date.today().strftime("%d.%m.%Y")

#pdf formating
def create_pdf():
    pdf = FPDF()
    pdf.add_page()
    pdf.set_title(f"Décompte du {aujourdhui}") #titre du document

    
    pdf.image(name="images/logo.png", w = 35, h= 30, x = 20, y = 15) #logo sur le pdf

    pdf.set_font("Arial", size=15, style= 'B')
    pdf.cell(60,20)
    pdf.cell(70, 20, txt=f"Décompte du {aujourdhui}", ln=True, align='C', border = "B")

    pdf.set_font("Times", size = 12)
    pdf.cell(200,30, txt= "", ln=True)
    for row in data1: 
         pdf.cell(160,10, txt= row[0])
         pdf.cell(20,10, txt= str(row[1]), ln=True, align = "R")
    pdf.cell(180,5, ln=True, border = "B")
    pdf.cell(160, 10, txt= "Chiffre d'affaire en cash")
    pdf.cell(20,10, txt=f"{CA_cash}", ln=True, align ="R")
    for elements in data2: 
         pdf.cell(160,10, txt= elements[0])
         pdf.cell(20,10, txt= str(elements[1]), ln=True, align= "R")
    pdf.cell(180,5, ln=True, border = "B")
    pdf.cell(160, 10, txt=f"Cash en bourse")
    pdf.cell(20,10, txt=f"{correction_bon}", ln=True, align = "R")
    
    buffer= BytesIO()
    pdf.output(buffer)
    buffer.seek(0)
    return buffer.read()

#button genéré + télécharger
if st.button("Générer PDF"):
    pdf_bytes = create_pdf()
    st.download_button(
        label="Télécharger le PDF",
        data=pdf_bytes,
        file_name= f"decompte_{aujourdhui}.pdf",
        mime='application/pdf'
    )
