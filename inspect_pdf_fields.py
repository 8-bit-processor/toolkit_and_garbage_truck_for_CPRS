from pypdf import PdfReader

def inspect_pdf_fields(pdf_path):
    reader = PdfReader(pdf_path)
    fields = reader.get_fields()
    if not fields:
        print(f"No form fields found in {pdf_path}")
        return

    print(f"Form fields in {pdf_path}:")
    for field_name in fields:
        print(f"- {field_name}")

if __name__ == "__main__":
    pdf_file = "cover sheet template.pdf"
    inspect_pdf_fields(pdf_file)
