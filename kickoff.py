from utilities import load_environment_variables
from processing import encode64, parse_receipt_to_json
from data_access import get_topHeadings
from output import create_excel_sheet
from openai import OpenAI
from groq import Groq
import os 

def run(uploaded_files, temp_file_path):
  print('starting kickoff')
  print(uploaded_files)
  #load environment variables
  load_environment_variables()
  OpenAI.api_key = os.getenv('OPENAI_API_KEY')
  Groq.api_key = os.getenv('GROQ_API_KEY')
  client = OpenAI()
  groq_client = Groq()
  
  processed_images = []
  #process files 
  for file in uploaded_files:
    print(f'processing {file}')
    processed_img = encode64(file)
    processed_images.append(processed_img)  

  print('extracting text..')
  #use vision to extract all text from images 
  extracted_texts = []
  for img in processed_images:
    response = client.chat.completions.create(
      model="gpt-4-vision-preview",
      messages=[
        {
          "role":"user",
          "content": [
            {
              "type": "text",
              "text": """As an AI, you are an unbiased evaluator tasked with analyzing images of receipts. 
              You use your built-in computer vision to perform careful image analysis in performing this automated task. 
              Your primary goal is to take advantage of your vision to translate the receipt into text. 
              
              Do not provide any clarifying explanations, or any perfunctory messages. Ensure to add duplicates should there be any on the receipt.
              """
            }, 
            {
              "type": "image_url",
              "image_url": {"url" : f"data:image/jpeg;base64,{img}"},
            },
          ],
        },
      ],
      max_tokens = 4096,
    )
    extracted_text = response.choices[0].message.content
    extracted_texts.append(extracted_text)
  print('extracted text')
  print(extracted_text)
  #combine all texts 
  combined_text = "\n".join(extracted_texts)
  print(f"COMBINED TEXT: {combined_text}")
  topHeadings = get_topHeadings()
  #refining prompt 
  message_obj = [{
        "role": "system",
        "content": f"""
          You are developing an expense tracker that processes text blocks containing receipt details. Your task is to extract each item's name and price, then categorize each item according to a predefined list of expense categories.
          Each item will most likely be abberviated. When categorizing, it is a good idea to guess the category based on the brand of the product (if possible). If the category remains unclear, default to placing the item under 'Groceries & Food'
          It's critical to accurately extract and categorize every item listed in the receipts without adding or omitting any details. Misinterpretation or addition of numbers is not acceptable.
          The output should be a cleanly formatted list, categorized by expense type, with each item and its price listed underneath the relevant category heading. Do not include any additional text or explanation outside of this structured format.
          
          Sometimes, the receipt itmes will be split into multiple boxes. Please ensure you get every item on each receipt that is given. 
          Categories can be found here ```{topHeadings}```

          Your output should resemble the following structure, strictly adhering to these categories and format:
          ````
          Groceries & Food
            ORG SUGAR, 4.99
            DC FIGS, 2.99
          Electronics & Appliances

          Home & Living
          ````
          Ensure the returned file strictly follows this format, with items and categories correctly placed based on the receipt(s) provided. Make sure not to hallucinate any values or items.

          """
      },
      {
        "role": "user",
        "content": combined_text,
      }]
  print('extraction successful')
  print('refining output..')
  #refine output
  response = groq_client.chat.completions.create(
    model="llama3-70b-8192",
    messages=message_obj,
  )
  msg = response.choices[0].message.content
  json_response = (parse_receipt_to_json(msg))
  print("CREATING EXCEL FILE")
  excel_sheet = create_excel_sheet(json_response, temp_file_path)
  return excel_sheet


