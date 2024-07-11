from utilities.openai_client import client

def ocr_processing(processed_img):
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
  return extracted_text