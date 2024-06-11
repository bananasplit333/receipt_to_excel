from utilities import load_environment_variables
from processing import encode64, parse_receipt_to_json
import time 
from data_access import get_topHeadings
from openai import OpenAI
from groq import Groq
import os 
import base64

def run(uploaded_file, temp_file_path):
  print('starting kickoff')
  #load environment variables
  load_environment_variables()
  OpenAI.api_key = os.getenv('OPENAI_API_KEY')
  Groq.api_key = os.getenv('GROQ_API_KEY')
  client = OpenAI()
  #groq_client = Groq()
  
  #processed_images = []
  # Process the uploaded file
  print(f'processing {uploaded_file}')
  img_data = uploaded_file.read()
  processed_img = base64.b64encode(img_data).decode('utf-8')


  print('extracting text..')
  #use vision to extract all text from images 
  extracted_texts = []
  '''
  for img in processed_images:
    response = client.chat.completions.create(
      model="gpt-4o",
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
  '''
  ##gpt 4 vision 
  response = client.chat.completions.create(
    
    model="gpt-4o",
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
            "image_url": {"url" : f"data:image/jpeg;base64,{processed_img}"},
          },
        ],
      },
    ],
    max_tokens = 4096,
  )

  extracted_text = response.choices[0].message.content
  extracted_texts.append(extracted_text)
  
  print('extracted text')
  #combine all texts 
  combined_text = "\n".join(extracted_texts)
  print(f"COMBINED TEXT: {combined_text}")
  topHeadings = get_topHeadings()
  #refining prompt 
  message_obj = [{
        "role": "system",
        "content": f"""
          You are developing an expense tracker that processes text blocks containing receipt details. Your task is to :
          1. extract each item's name and price, then categorize each item according to a predefined list of expense categories.
          2. identify the store that the photo belongs to - ie. Costco, Shoppers, etc.
          3. Display the tax 
          4. Display total cost 
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
          Return the result in JSON format.
          """
      },
      {
        "role": "user",
        "content": combined_text,
      }]
  print('extraction successful')
  print('refining output..')
  #refine output
  response = client.chat.completions.create(
    model="gpt-4o",
    response_format={"type": "json_object"},
    messages=message_obj,
  )
  msg = response.choices[0].message.content
  print(msg)
  #json_response = (parse_receipt_to_json(msg))
  return msg 
  print("CREATING EXCEL FILE")
  print(json_response)


  """
  excel_sheet = create_excel_sheet(json_response, temp_file_path)
  return excel_sheet
  """ 

