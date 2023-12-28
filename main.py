from PyPDF2 import PdfReader, PdfWriter
from PyPDF2.generic import ContentStream, NameObject, TextStringObject

def remove_watermarks(input_pdf_file, watermark_texts, replace_with=""):
    # Load PDF into PyPDF2
    reader = PdfReader(input_pdf_file)
    writer = PdfWriter()

    for page in reader.pages:
        # Get the current page's contents
        content_object = page["/Contents"]
        content = ContentStream(content_object, reader)

        # Loop over all PDF elements
        for operands, operator in content.operations:
            # Check if the operand is in the list of watermark texts
            if operator == b"Tj" and operands[0] in watermark_texts:
                operands[0] = TextStringObject(replace_with)

        # Set the modified content as a content object on the page
        page.__setitem__(NameObject("/Contents"), content)

        # Add the page to the output
        writer.add_page(page)

    # Write the modified PDF to a new file
    output_pdf_file = input_pdf_file.replace(".pdf", "_new.pdf")
    with open(output_pdf_file, "wb") as fh:
        writer.write(fh)

    print(f"Watermarks removed. Output saved to {output_pdf_file}")

if __name__ == "__main__":
    input_pdf_file = input("Enter the input PDF file name: ")
    num_watermarks = int(input("Enter the number of watermarks to remove: "))

    watermark_texts = []
    for i in range(num_watermarks):
        watermark_text = input(f"Enter watermark text {i + 1}: ")
        watermark_texts.append(watermark_text)

    replace_with = input("Enter the text to replace the watermark with (leave blank for removal): ")

    remove_watermarks(input_pdf_file, watermark_texts, replace_with)

