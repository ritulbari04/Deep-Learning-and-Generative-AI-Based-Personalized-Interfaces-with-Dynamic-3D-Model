import weaviate
from pypdf import PdfReader

reader=PdfReader(r"C:\Users\ishan\Desktop\Minor Project\pdf_files\social science\history'\10\jess305.pdf")

client = weaviate.connect_to_local()

school= client.collections.get("School")

with school.batch.dynamic() as batch:
    for i in reader.pages:
        batch.add_object({"history105":i.extract_text()})
        if batch.number_errors>10:
            print("Batch import stopped due to excessive errors.")
            break

failed_object= school.batch.failed_objects
if failed_object:
    print("number of failed imports: ",len(failed_object))
    print("first failed object: ",failed_object[0])

print("successfully inserted!!")

client.close()