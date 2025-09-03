import streamlit as st
from fpdf import FPDF
from datetime import date
from PIL import Image
import tempfile
from pypdf import PdfReader, PdfWriter
from mailersend import MailerSendClient, EmailBuilder
from dotenv import load_dotenv
import os
import base64
from dotenv import load_dotenv


load_dotenv()
api_key = os.getenv("MAILERSEND_API_KEY")


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
Facture = st.number_input("Montant encaissé sur facture")
correction_bon = CA_cash + Bon_cash + Bon_carte - Bon_encaisse - Facture


# Initialize session state variables
if "show_ticket_form" not in st.session_state:
    st.session_state["show_ticket_form"] = False

if "tickets" not in st.session_state:
    st.session_state["tickets"] = []

# Show input form when button is clicked
if st.button("Ajouter un ticket"):
    st.session_state["show_ticket_form"] = True


if st.session_state["show_ticket_form"]:
    with st.form("ticket_form"):
        nom = st.text_input("Nom du ticket")
        montant = st.number_input("Montant du ticket", min_value=0.0, step=0.1)
        submitted = st.form_submit_button("Valider")

        if submitted:
            if nom and montant > 0:
                st.session_state["tickets"].append({"nom": nom, "montant": montant})
                st.success(f"Ticket ajouté: {nom}, {montant} CHF")
            else:
                st.warning("Veuillez entrer un nom et un montant supérieur à 0.")
            # st.session_state["show_ticket_form"] = False  # Hide form immediately after click

sum_ticket = 0

# Display list of all tickets
st.markdown("### Tickets enregistrés :")
if st.session_state["tickets"]:
    for i, ticket in enumerate(st.session_state["tickets"], start=1):
        st.write(f"{i}. {ticket['nom']} – {ticket['montant']} CHF")
        sum_ticket += int(ticket["montant"])
else:
    st.write("Aucun ticket pour l'instant.")



cash_final = correction_bon - sum_ticket

data1 = [["Chiffre d'affaire", CA],
         ["Chiffre d'affaire encaissé par carte", CB_sum]]

data2 = [["Bons vendus par cash", Bon_cash],
         ["Bons vendus par carte", Bon_carte],
         ["Bons encaissés", Bon_encaisse],
         ["Montant facturés", Facture]]

aujourdhui = date.today().strftime("%d.%m.%Y")

uploaded_file = st.file_uploader("Ajouter une pièce jointe (image ou PDF)", type=["jpg", "jpeg", "png", "pdf"], accept_multiple_files = True)




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
        pdf.cell(20, 10, txt=f'-{str(row[1])}', ln=True, align="R")

    pdf.cell(180, 5, ln=True, border="B")
    pdf.cell(160, 10, txt="Chiffre d'affaire en cash")
    pdf.cell(20, 10, txt=f"{CA_cash}", ln=True, align="R")

    for row in data2:
        pdf.cell(160, 10, txt=row[0])
        pdf.cell(20, 10, txt=f'-{str(row[1])}', ln=True, align="R")

    pdf.cell(180, 5, ln=True, border="B")
    pdf.cell(160, 10, txt="Cash en bourse")
    pdf.cell(20, 10, txt=f"{correction_bon}", ln=True, align="R")

    pdf.set_font("Times", size=12, style = "I")
    pdf.cell(20, 10,  txt= "Tickets", ln=True)
    pdf.set_font("Times", size=12)
    
    for i, ticket in enumerate(st.session_state["tickets"], start=1):
        pdf.cell(160, 10, txt=ticket["nom"])
        pdf.cell(20, 10, txt=f' -{str(ticket["montant"])}', ln=True, align="R")

    pdf.cell(180, 5, ln=True, border="B")
    pdf.cell(160, 10, txt="Cash en bourse sans les tickets")
    pdf.cell(20, 10, txt=f"{cash_final}", ln=True, align="R")
    


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
        generate_main_pdf(generated_pdf_path)

        # Prepare merger
        writer = PdfWriter()

        # Add generated main PDF
        reader_generated = PdfReader(generated_pdf_path)
        for page in reader_generated.pages:
            writer.add_page(page)

        # Process each uploaded file
        for file in uploaded_file:
            if file.type == "application/pdf":
                uploaded_path = f"{tmpdir}/{file.name}"
                with open(uploaded_path, "wb") as f:
                    f.write(file.read())

                reader_uploaded = PdfReader(uploaded_path)
                for page in reader_uploaded.pages:
                    writer.add_page(page)

            elif file.type.startswith("image/"):
                # Save image temporarily
                image_path = f"{tmpdir}/{file.name}"
                image = Image.open(file)
                image.save(image_path)

                # Convert image to a one-page PDF
                pdf = FPDF()
                pdf.add_page()
                pdf.image(image_path, x=10, y=10, w=pdf.w - 20)
                image_pdf_path = f"{tmpdir}/{file.name}.pdf"
                pdf.output(image_pdf_path)

                # Read and add to writer
                reader_image_pdf = PdfReader(image_pdf_path)
                for page in reader_image_pdf.pages:
                    writer.add_page(page)

        # Write final PDF
        final_pdf_path = f"decompte_{aujourdhui}.pdf"
        with open(final_pdf_path, "wb") as f_out:
            writer.write(f_out)

        st.session_state.final_pdf_path = final_pdf_path

        # Download button
        with open(final_pdf_path, "rb") as f:
            st.download_button(
                label="Télécharger le PDF",
                data=f,
                file_name=f"decompte_{aujourdhui}.pdf",
                mime="application/pdf"
            )



if st.button("Envoyer le décompte par mail"):
    if "final_pdf_path" not in st.session_state:
        st.error("⚠️ You need to generate the PDF before sending it by email.")
    else:
        try:
            with open(st.session_state.final_pdf_path, "rb") as f:
                pdf_content = base64.b64encode(f.read()).decode("utf-8")
            ms = MailerSendClient(api_key)

            email = (EmailBuilder()
                    .from_email("decompte@test-2p0347zkvp7lzdrn.mlsender.net", "Romane Cotting")
                    .to_many([{"email": "romane.cotting@gmail.com", "name": "Recipient"}])
                    .subject(f"Décompte du soir - {aujourdhui}")
                    .html(f"Ci-joint, le décompte du soir du {aujourdhui} ")
                    .text(f"Please find attached the daily report for {aujourdhui}.")
                    .attach_file(st.session_state.final_pdf_path)
                    .build())

            response = ms.emails.send(email)
            st.success("Email envoyé avec succès!")

        except Exception as e:
            st.error(f"L'email n'a pas pu être envoyé: {e}")
