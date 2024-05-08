from utilities import load_environment_variables
from processing import encode64, parse_receipt_to_json
import time 
from data_access import get_topHeadings
from openai import OpenAI
from groq import Groq
from anthropic import Anthropic
import os 
import base64

def run(uploaded_file, temp_file_path):
  print('starting kickoff')
  #load environment variables
  load_environment_variables()
  OpenAI.api_key = os.getenv('OPENAI_API_KEY')
  Groq.api_key = os.getenv('GROQ_API_KEY')
  client = OpenAI()
  claude_client = Anthropic()
  groq_client = Groq()
  
  processed_images = []
  # Process the uploaded file
  print(f'processing {uploaded_file}')
  img_data = uploaded_file.read()
  processed_img = base64.b64encode(img_data).decode('utf-8')


  print('extracting text..')
  #use vision to extract all text from images 
  extracted_texts = []
  
  gpt_time = time.time() 
  ##gpt 4 vision 
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
            "image_url": {"url" : f"data:image/jpeg;base64,{processed_img}"},
          },
        ],
      },
    ],
    max_tokens = 4096,
  )
  gpt_end_time = time.time() 
  gpt_t = gpt_end_time - gpt_time 
  print(f"GPT TOTAL TIME : {gpt_t}")
  
  print('starting claude..')
  start_time = time.time() 
  #claude vision 
  message = claude_client.messages.create(
    model="claude-3-opus-20240229",
    max_tokens=1024,
    messages=[
        {
            "role": "user",
            "content": [
                {
                    "type": "url",
                    "source": {
                        "type": "base64",
                        "media_type": "image/jpeg",
                        "data": {processed_img}
                    }
                },
                {
                    "type": "text",
                    "text": "translate the receipt into text."
                }
            ]
        }
    ]
  )
  end_time = time.time() 
  claude_t = end_time - start_time
  print(f"CLAUDE TOTAL TIME: {claude_t}")
  print(message)
  
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
  print(json_response)


  """
  excel_sheet = create_excel_sheet(json_response, temp_file_path)
  return excel_sheet
  """ 

