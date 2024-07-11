
from processing import encode64, parse_receipt_to_json
from processing.openai_vision import ocr_processing
from processing.receipt_processing import process_receipt
from processing.bill_processing import process_bills
from data_access import get_topHeadings
from utilities.openai_client import client
# from groq import Groq
import os 
import base64

def run(uploaded_file, temp_file_path, image_type):
  client
  print('starting kickoff')

  try:
    # Process the uploaded file
    print(f'processing {uploaded_file}')
    img_data = uploaded_file.read()
    processed_img = base64.b64encode(img_data).decode('utf-8')
    try:
      #use vision to extract all text from images 
      extracted_texts = []
      print('extracting text from img...')
      image_to_text = ocr_processing(processed_img) #process image to text  
      extracted_texts.append(image_to_text) # append to msg array
       #combine all texts 
      combined_text = "\n".join(extracted_texts)

      if (image_type == 'receipt'): 
        try:
          #processing receipt into expense format 
          topHeadings = get_topHeadings()
          msg = process_receipt(combined_text, topHeadings)
          print(msg)
          return msg 
        except Exception as e:
          print(f"Error processing receipt: {str(e)}")
      else:
        try:
          #process invoice into expense format 
          msg = process_bills(combined_text)
          print(msg)
          return msg
        except Exception as e:
          print(f"Error processing invoice: {str(e)}")
    except Exception as e:
      print(f"Error parsing image to text")
  except Exception as e:
    print(f"Error processing image: {str(e)}")
    return {"error": str(e)}


  """
   print("CREATING EXCEL FILE")
  print(json_response)
  excel_sheet = create_excel_sheet(json_response, temp_file_path)
  return excel_sheet
  """ 

