# from spire.presentation import *
#
# presentation = Presentation()
# presentation.LoadFromFile("data/decks/[WK07] US Weekly Business Review _ Feb 13 - 17.pptx")
# presentation.SaveToFile("data/pdfs/[WK07] US Weekly Business Review _ Feb 13 - 17.pdf", FileFormat.PDF)
# presentation.Dispose()


from spire.presentation import *


def convert_pptx_to_pdf(input_path, output_path):
    presentation = Presentation()
    presentation.LoadFromFile(input_path)
    presentation.SaveToFile(output_path, FileFormat.PDF)
    presentation.Dispose()


def batch_convert_pptx_to_pdf(input_directory, output_directory):
    if not os.path.exists(output_directory):
        os.makedirs(output_directory)

    input_files = os.listdir(input_directory)

    for file_name in input_files:
        if file_name.lower().endswith(('.ppt', '.pptx')):
            input_path = os.path.join(input_directory, file_name)
            output_path = os.path.join(output_directory, f"{os.path.splitext(file_name)[0]}.pdf")

            if not os.path.exists(output_path):
                try:
                    convert_pptx_to_pdf(input_path, output_path)
                    print(f"Converted {file_name} to {os.path.basename(output_path)}")
                except:
                    print(f"Couldn't Convert {file_name}")
            else:
                print(f"Skipped {file_name} - PDF already exists")


if __name__ == "__main__":
    input_directory = "data/decks"
    output_directory = "data/pdfs"

    batch_convert_pptx_to_pdf(input_directory, output_directory)
