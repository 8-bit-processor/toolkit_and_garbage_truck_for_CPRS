from pypdf import PdfReader, PdfWriter

def populate_pdf(input_pdf_path, output_pdf_path, data):
    reader = PdfReader(input_pdf_path)
    writer = PdfWriter()

    writer.clone_document_from_reader(reader)

    writer.update_page_form_field_values(
        writer.get_page(0), data
    )

    with open(output_pdf_path, "wb") as output_stream:
        writer.write(output_stream)
    print(f"Successfully populated {input_pdf_path} and saved to {output_pdf_path}")

if __name__ == "__main__":
    pdf_file = "cover sheet template.pdf"
    output_file = "cover_sheet_populated.pdf"
    
    # Data to populate the form fields
    # Use the exact field names identified by inspect_pdf_fields.py
    data_to_fill = {
        "Last 4 of SSN": "1234",
        "Patient Name": "John Doe",
        "Patient Date of Birth": "01/01/1980",
        "Date Of OCC Consult": "12/10/2025",
        "Consult Number": "CON-56789",
        "Single Visit Date": "12/10/2025",
        "Today's Date_af_date": "12/10/2025",
        "Reviewer Initials": "JD",
        "Status": "Completed",
        "Location Where Care was conducted": "Main Hospital",
        "TOTAL PAGES": "3"
    }

    populate_pdf(pdf_file, output_file, data_to_fill)
