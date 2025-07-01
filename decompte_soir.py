# import streamlit as st
# from fpdf import FPDF
# from datetime import date
# from io import BytesIO
# from PIL import Image
# import tempfile
# from PyPDF2 import PdfReader, PdfWriter

# #formatting web page
# left_co, cent_co,last_co = st.columns(3)
# with last_co:
#      st.image("images/logo.png", width=170)
# with left_co: 
#      st.title("Décompte du jour")


# #definition of variables
# CA=st.number_input("Chiffre d'affaire selon ticket")
# CB1= st.number_input("Encaissé par carte avec machine 1")
# CB2 = st.number_input("Encaissé par carte avec machine 2")
# CB_sum = CB1 + CB2
# CA_cash = CA-CB_sum
# Bon_cash = st.number_input("Bons vendus par cash")
# Bon_carte = st.number_input("Bons vendus par carte")
# Bon_encaisse = st.number_input("Bons encaissé")
# correction_bon= CA_cash + Bon_cash + Bon_carte - Bon_encaisse#a recontroler !!!!!!!

# data1 = [["Chiffre d'affaire", CA],
#         ["Chiffre d'affaire encaissé par carte", CB_sum],] 

# data2 = [["Bons vendus par cash", Bon_cash],
#          ["Bons vendus par carte", Bon_carte],
#          ["Bons encaissés", Bon_encaisse]]

# aujourdhui = date.today().strftime("%d.%m.%Y")

# #pdf formating
# def create_pdf(uploaded_file):
#     buffer = BytesIO()
#     pdf = FPDF()
#     pdf.add_page()
#     pdf.set_title(f"Décompte du {aujourdhui}") #titre du document

    
#     pdf.image(name="images/logo.png", w = 35, h= 30, x = 20, y = 15) #logo sur le pdf

#     pdf.set_font("Arial", size=15, style= 'B')
#     pdf.cell(60,20)
#     pdf.cell(70, 20, txt=f"Décompte du {aujourdhui}", ln=True, align='C', border = "B")

#     pdf.set_font("Times", size = 12)
#     pdf.cell(200,30, txt= "", ln=True)
#     for row in data1: 
#          pdf.cell(160,10, txt= row[0])
#          pdf.cell(20,10, txt= str(row[1]), ln=True, align = "R")
#     pdf.cell(180,5, ln=True, border = "B")
#     pdf.cell(160, 10, txt= "Chiffre d'affaire en cash")
#     pdf.cell(20,10, txt=f"{CA_cash}", ln=True, align ="R")
#     for elements in data2: 
#          pdf.cell(160,10, txt= elements[0])
#          pdf.cell(20,10, txt= str(elements[1]), ln=True, align= "R")
#     pdf.cell(180,5, ln=True, border = "B")
#     pdf.cell(160, 10, txt=f"Cash en bourse")
#     pdf.cell(20,10, txt=f"{correction_bon}", ln=True, align = "R")
    

#     pdf.output(buffer)
#     buffer.seek(0)

#     # Step 2: If uploaded file is a PDF, merge it
#     if uploaded_file and type(uploaded_file) == "streamlit.runtime.uploaded_file_manager.UploadedFile":
#         writer = PdfWriter()

#         # Add generated PDF
#         reader_generated = PdfReader(buffer)
#         for page in reader_generated.pages:
#             writer.add_page(page)

#         # Add uploaded PDF
#         reader_uploaded = PdfReader(uploaded_file)
#         for page in reader_uploaded.pages:
#             writer.add_page(page)

#         merged_buffer = BytesIO()
#         writer.write(merged_buffer)
#         merged_buffer.seek(0)
#         return merged_buffer

#     # Step 3: If uploaded image, just return the buffer with image already handled
#     if uploaded_file and hasattr(uploaded_file, "type") and str(type(uploaded_file)).startswith("image/"):
#         with tempfile.NamedTemporaryFile(delete=False, suffix=".png") as tmpfile:
#             image = Image.open(uploaded_file)
#             image.save(tmpfile.name)
#             pdf.add_page()
#             pdf.image(tmpfile.name, x=10, y=10, w=pdf.w - 20)

#         buffer = BytesIO()
#         pdf.output(buffer)
#         buffer.seek(0)
#         return buffer

#     # Default: just return the generated PDF
#     return buffer


# #     #if uploaded_file and hasattr(uploaded_file, "type") and uploaded_file.type and uploaded_file.type.startswith("image/"):
# #     if uploaded_file:
# #           pdf.add_page()
# #           with tempfile.NamedTemporaryFile(delete=False, suffix=".png") as tmpfile:
# #                image = Image.open(uploaded_file)
# #                image.save(tmpfile.name)
# #                pdf.image(tmpfile.name, x=10, y=10, w=pdf.w - 20)


          


# # # for app version
# #     #pdf_output = pdf.output(dest='S').encode("latin-1")
# #     #return bytes(pdf_output)


# #     #only for local host
# #     buffer = BytesIO()
# #     pdf.output(buffer)
# #     buffer.seek(0)
# #     return buffer
                     
# uploaded_file = st.file_uploader("Upload a scanned document", type=["jpg", "jpeg", "png", "pdf"])
# if uploaded_file: 
#           st.success("File uploaded successfully")
#           st.text(type(uploaded_file))


# #button genéré + télécharger
# if st.button("Générer PDF") and uploaded_file:
#     pdf_bytes = create_pdf(uploaded_file)
#     st.download_button(
#         label="Télécharger le PDF",
#         data=pdf_bytes,
#         file_name= f"decompte_{aujourdhui}.pdf",
#         mime='application/pdf'
#     )




import streamlit as st
from fpdf import FPDF
from datetime import date
from PIL import Image
import tempfile
import pypdf

st.set_page_config(layout="centered")

# Layout
left_co, cent_co, last_co = st.columns(3)
with last_co:
    st.image("images/logo.png", width=170)
with left_co:
    st.title("Décompte du jour")

# Variables
CA = st.number_input("Chiffre d'affaire selon ticket")
CB1 = st.number_input("Encaissé par carte avec machine 1")
CB2 = st.number_input("Encaissé par carte avec machine 2")
CB_sum = CB1 + CB2
CA_cash = CA - CB_sum
Bon_cash = st.number_input("Bons vendus par cash")
Bon_carte = st.number_input("Bons vendus par carte")
Bon_encaisse = st.number_input("Bons encaissés")
correction_bon = CA_cash + Bon_cash + Bon_carte - Bon_encaisse

data1 = [["Chiffre d'affaire", CA],
         ["Chiffre d'affaire encaissé par carte", CB_sum]]

data2 = [["Bons vendus par cash", Bon_cash],
         ["Bons vendus par carte", Bon_carte],
         ["Bons encaissés", Bon_encaisse]]

aujourdhui = date.today().strftime("%d.%m.%Y")
uploaded_file = st.file_uploader("Ajouter une pièce jointe (image ou PDF)", type=["jpg", "jpeg", "png", "pdf"])


def generate_main_pdf(output_path):
    pdf = FPDF()
    pdf.add_page()
    pdf.set_title(f"Décompte du {aujourdhui}")
    pdf.image(name="images/logo.png", w=35, h=30, x=20, y=15)

    pdf.set_font("Arial", size=15, style='B')
    pdf.cell(60, 20)
    pdf.cell(70, 20, txt=f"Décompte du {aujourdhui}", ln=True, align='C', border="B")

    pdf.set_font("Times", size=12)
    pdf.cell(200, 30, txt="", ln=True)

    for row in data1:
        pdf.cell(160, 10, txt=row[0])
        pdf.cell(20, 10, txt=str(row[1]), ln=True, align="R")

    pdf.cell(180, 5, ln=True, border="B")
    pdf.cell(160, 10, txt="Chiffre d'affaire en cash")
    pdf.cell(20, 10, txt=f"{CA_cash}", ln=True, align="R")

    for row in data2:
        pdf.cell(160, 10, txt=row[0])
        pdf.cell(20, 10, txt=str(row[1]), ln=True, align="R")

    pdf.cell(180, 5, ln=True, border="B")
    pdf.cell(160, 10, txt="Cash en bourse")
    pdf.cell(20, 10, txt=f"{correction_bon}", ln=True, align="R")

    pdf.output(output_path)


def merge_with_uploaded_file(generated_pdf_path, uploaded_file_path, final_path):
    writer = PdfWriter()

    # Add generated PDF
    reader_generated = PdfReader(generated_pdf_path)
    for page in reader_generated.pages:
        writer.add_page(page)

    # Add uploaded PDF
    reader_uploaded = PdfReader(uploaded_file_path)
    for page in reader_uploaded.pages:
        writer.add_page(page)

    with open(final_path, "wb") as f:
        writer.write(f)


if st.button("Générer PDF") and uploaded_file:
    with tempfile.TemporaryDirectory() as tmpdir:
        generated_pdf_path = f"{tmpdir}/main.pdf"
        final_pdf_path = f"{tmpdir}/merged.pdf"
        generate_main_pdf(generated_pdf_path)

        if uploaded_file.type == "application/pdf":
            # Save uploaded PDF to temp file
            uploaded_path = f"{tmpdir}/upload.pdf"
            with open(uploaded_path, "wb") as f:
                f.write(uploaded_file.read())
            merge_with_uploaded_file(generated_pdf_path, uploaded_path, final_pdf_path)

        elif uploaded_file.type.startswith("image/"):
            # Save image and insert into generated PDF as new page
            image_path = f"{tmpdir}/upload.png"
            image = Image.open(uploaded_file)
            image.save(image_path)

            # Open existing PDF to add image as new page
            pdf = FPDF()
            pdf.add_page()
            pdf.image(image_path, x=10, y=10, w=pdf.w - 20)
            image_pdf_path = f"{tmpdir}/image_page.pdf"
            pdf.output(image_pdf_path)

            # Merge
            merge_with_uploaded_file(generated_pdf_path, image_pdf_path, final_pdf_path)
        else:
            final_pdf_path = generated_pdf_path  # no merge needed

        with open(final_pdf_path, "rb") as f:
            st.download_button(
                label="Télécharger le PDF",
                data=f,
                file_name=f"decompte_{aujourdhui}.pdf",
                mime="application/pdf"
            )
