import re
import PyPDF2


# Replace these with your actual PDF file paths pairs
pdf_pairs = [
    ("202410/Apergu-202410C.pdf", "202410/Apergu.pdf", "202410/Apergu-202410C.pdf"),
    ("202410/BNI Sekuritas-202410C.pdf", "202410/BNI.pdf", "202410/BNI Sekuritas-202410C.pdf"),
    ("202410/Citroen-202410C.pdf", "202410/Citroen.pdf", "202410/Citroen-202410C.pdf"),
    ("202410/DP World-202410C.pdf", "202410/DP World.pdf", "202410/DP World-202410C.pdf"),
    ("202410/Efishery VC-202410C.pdf", "202410/Efishery VC.pdf", "202410/Efishery VC-202410C.pdf"),
    ("202410/Efishery-202410C.pdf", "202410/Efishery.pdf", "202410/Efishery-202410C.pdf"),
    ("202410/Hatra Group-202410C.pdf", "202410/Hatra Group.pdf", "202410/Hatra Group-202410C.pdf"),
    ("202410/Human Initiative-202410C.pdf", "202410/HI.pdf", "202410/Human Initiative-202410C.pdf"),
    ("202410/IATA-202410C.pdf", "202410/IATA.pdf", "202410/IATA-202410C.pdf"),
    ("202410/CC/JW Integra-2024-09C.pdf", "202410/CC/JW Integra.pdf", "202410/CC/JW Integra-2024-09C.pdf"),
    ("202410/CC/Maxima-2024-09C.pdf", "202410/CC/Maxima.pdf", "202410/CC/Maxima-2024-09C.pdf"),
    ("202410/CC/Meval-2024-09C.pdf", "202410/CC/Meval.pdf", "202410/CC/Meval-2024-09C.pdf"),
    ("202410/CC/MyNavi-2024-09C.pdf", "202410/CC/MyNavi.pdf", "202410/CC/MyNavi-2024-09C.pdf"),
    ("202410/CC/OTG-2024-09C.pdf", "202410/CC/OTG.pdf", "202410/CC/OTG-2024-09C.pdf"),
    ("202410/CC/Qiscus-2024-09C.pdf", "202410/CC/Qiscus.pdf", "202410/CC/Qiscus-2024-09C.pdf"),
    ("202410/CC/TDI-2024-09C.pdf", "202410/CC/TDI.pdf", "202410/CC/Reckitt-2024-09C.pdf"),
    ("202410/CC/Rohul Mineral-2024-09C.pdf", "202410/CC/Rohul.pdf", "202410/CC/Rohul Mineral-2024-09C.pdf"),
    ("202410/CC/RTS-2024-09C.pdf", "202410/CC/RTS.pdf", "202410/CC/RTS-2024-09C.pdf"),
    ("202410/CC/TDI-2024-09C.pdf", "202410/CC/TDI.pdf", "202410/CC/TDI-2024-09C.pdf"),
    ("202410/CC/Webuy-2024-09C.pdf", "202410/CC/Webuy.pdf", "202410/CC/Webuy-2024-09C.pdf"),
    ("202410/Yappika-202410C.pdf", "202410/Yappika.pdf", "202410/Yappika-202410C.pdf"),
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
    invoice_subtotal = extract_value_from_pdf(invoice_pdf, "Sub Total")
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
