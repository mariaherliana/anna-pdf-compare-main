import re
import PyPDF2


# Replace these with your actual PDF file paths pairs
pdf_pairs = [
    ("202409/Agatha-202409.pdf", "202409/agatha.pdf", "202409/Agatha-202409.pdf"),
    ("202409/Anugrah Pratama-202409.pdf", "202409/AP.pdf", "202409/Anugrah Pratama-202409.pdf"),
    ("202409/Arora-202409.pdf", "202409/Arora.pdf", "202409/Arora-202409.pdf"),
    ("202409/ATD Law-202409.pdf", "202409/ATD.pdf", "202409/ATD Law-202409.pdf"),
    ("202409/Atlas Beachfest-202409.pdf", "202409/Atlas.pdf", "202409/Atlas Beachfest-202409.pdf"),
    ("202409/BKSI-202409.pdf", "202409/BKSI.pdf", "202409/BKSI-202409.pdf"),
    ("202409/Casa Universal-202409.pdf", "202409/Casa.pdf", "202409/Casa Universal-202409.pdf"),
    ("202409/Deepublish-202409.pdf", "202409/Deepublish.pdf", "202409/Deepublish-202409.pdf"),
    ("202409/Duha Madani-202409.pdf", "202409/Duha.pdf", "202409/Duha Madani-202409.pdf"),
    ("202409/Klik Eat-202409.pdf", "202409/Klik Eat.pdf", "202409/Klik Eat-202409.pdf"),
    ("202409/Koperasi BEST-202409.pdf", "202409/Koperasi best.pdf", "202409/Koperasi BEST-202409.pdf"),
    ("202409/Legalku-202409.pdf", "202409/Legalku.pdf", "202409/Legalku-202409.pdf"),
    ("202409/Madev-202409.pdf", "202409/Madev.pdf", "202409/Madev-202409.pdf"),
    ("202409/Mceasy Parts-202409.pdf", "202409/Mceasy Parts.pdf", "202409/Mceasy Parts-202409.pdf"),
    ("202409/Mceasy-202409.pdf", "202409/Mceasy.pdf", "202409/Mceasy-202409.pdf"),
    ("202409/Moladin-202409.pdf", "202409/Moladin 1.pdf", "202409/Moladin-202409.pdf"),
    ("202409/Moladin-202409_02.pdf", "202409/Moladin 2.pdf", "202409/Moladin-202409_02.pdf"),
    ("202409/Moladin-202409_03.pdf", "202409/Moladin 3.pdf", "202409/Moladin-202409_03.pdf"),
    ("202409/Mortgage Master-202409.pdf", "202409/Mortgage.pdf", "202409/Mortgage Master-202409.pdf"),
    ("202409/Nobi-202409.pdf", "202409/Nobi.pdf", "202409/Nobi-202409.pdf"),
    ("202409/Officenow-202409.pdf", "202409/Officenow.pdf", "202409/Officenow-202409.pdf"),
    ("202409/Online Pajak-202409_02.pdf", "202409/OP 2.pdf", "202409/Online Pajak-202409_02.pdf"),
    ("202409/Online Pajak-202409.pdf", "202409/OP.pdf", "202409/Online Pajak-202409.pdf"),
    ("202409/Padmacahaya-202409.pdf", "202409/Padma.pdf", "202409/Padmacahaya-202409.pdf"),
    ("202409/Prasetia-202409.pdf", "202409/Prasetia.pdf", "202409/Prasetia-202409.pdf"),
    ("202409/Prossi-202409.pdf", "202409/Prossi.pdf", "202409/Prossi-202409.pdf"),
    ("202409/Qiscus - Cakap-202409.pdf", "202409/cakap.pdf", "202409/Qiscus - Cakap-202409.pdf"),
    ("202409/Qiscus - Fisiohome-202409.pdf", "202409/Fisiohome.pdf", "202409/Qiscus - Fisiohome-202409.pdf"),
    ("202409/RTS-202409.pdf", "202409/RTS.pdf", "202409/RTS-202409.pdf"),
    ("202409/Satu Dental-202409.pdf", "202409/Satu Dental.pdf", "202409/Satu Dental-202409.pdf"),
    ("202409/Senri-202409.pdf", "202409/Senri.pdf", "202409/Senri-202409.pdf"),
    ("202409/Telexindo-202409.pdf", "202409/Telexindo.pdf", "202409/Telexindo-202409.pdf"),
    ("202409/UNRISK-202409.pdf", "202409/UNRISK.pdf", "202409/UNRISK-202409.pdf"),
    # Add more pairs here if you want to add
]


def extract_value_from_pdf(pdf_file: str, keyword: str) -> float:
    with open(pdf_file, "rb") as f:
        reader = PyPDF2.PdfReader(f)
        text = ""
        for page_num in range(len(reader.pages)):
            text += reader.pages[page_num].extract_text()

    # Use regular expression to find the value next to the keyword
    pattern = rf"Sub Total\s*(\d+(?:[.,]\d{3})*(?:[.,]\d{2}))"
    value_match = re.search(pattern, text)
    if value_match:
        value = float(value_match.group(1).replace(".", "").replace(",", "."))
        return value
    else:
        return -1


def compare_pdf_values(invoice_pdf: str, facture_pdf: str) -> bool:
    # Extract values from Invoice
    print(f"- Extracting data from {invoice_pdf}")
    invoice_subtotal = extract_value_from_pdf(invoice_pdf, "Subtotal")
    invoice_vat = extract_value_from_pdf(invoice_pdf, "VAT \(11%\)")
    # Extract values from Facture
    print(f"- Extracting data from {facture_pdf}")
    facture_taxable_base_amount = extract_value_from_pdf(
        facture_pdf, "Dasar Pengenaan Pajak"
    )
    facture_total_ppn = extract_value_from_pdf(facture_pdf, "Total PPN")
    return (invoice_subtotal == facture_taxable_base_amount) and (
        invoice_vat == facture_total_ppn
    )


def merge_pdfs(pdf1_path: str, pdf2_path: str, output_path: str) -> None:
    print(f"- Merging PDF files in {output_path}")
    with open(pdf1_path, "rb") as pdf1_file, open(pdf2_path, "rb") as pdf2_file:
        pdf1_reader = PyPDF2.PdfReader(pdf1_file)
        pdf2_reader = PyPDF2.PdfReader(pdf2_file)

        pdf_writer = PyPDF2.PdfWriter()
        for page_num in range(len(pdf1_reader.pages)):
            page = pdf1_reader.pages[page_num]
            pdf_writer.add_page(page)
        for page_num in range(len(pdf2_reader.pages)):
            page = pdf2_reader.pages[page_num]
            pdf_writer.add_page(page)

        with open(output_path, "wb") as output_file:
            pdf_writer.write(output_file)


def __main__():
    print("Starting script")
    for invoice, facture, output in pdf_pairs:
        if compare_pdf_values(invoice, facture):
            print("- Values do MATCH between the two PDF files")
            merge_pdfs(invoice, facture, output)
        else:
            print(f"(!) Warning: Values DO NOT match between PDF files {invoice} and {facture}")
    print("Ending script")


__main__()
