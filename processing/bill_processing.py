from utilities.openai_client import client 

def process_bills(input):
    message = [{
        "role": "system",
        "content": f"""
          You are developing an expense tracker that processes invoices. Your task is to :
          1. extract each item/service name and price
          2. identify the person or company that the invoice is coming from (ie. Gerard Howards, octagon legal group, etc. If you are given both a name and a company, return the company name).
          3. extract invoice number 
          4. extract invoice date 
          5. extract name of the person or company the invoice is going to
          6. extract tax information 
          7. Display total cost 
          Each item will most likely be abberviated. 
          It's critical to accurately extract every item listed in the receipts without adding or omitting any details. Misinterpretation or addition of numbers is not acceptable.
          The output should be a cleanly formatted list, with each item and its price listed. Do not include any additional text or explanation outside of this structured format.
          
          Your output should resemble the following structure, strictly adhering to these categories and format:
          ````
          Item: 
            60 GB 24/7 data plan, 53.99
            2x 1GB data plan, 10.99 
            Disney+ year subscription, 129.99
          Vendor: Fido Wireless Communications
          Invoice number: 123456
          Invoice date: 2022-01-01
          Invoice due date: 2022-03-31
          Owner: John Doe
          Tax: 4.20
          Total Cost: 199.17
          ````
          Ensure the returned file strictly follows this format, with items andcorrectly placed based on the invoice provided. Make sure not to hallucinate any values or items.
          Return the result in JSON format.
          """
      },
      {
        "role": "user",
        "content": input,
      }]
    
    #get response 
    response = client.chat.completions.create(
        model="gpt-3.5-turbo",
        response_format={"type": "json_object"},
        messages=message,
    )
    result = response.choices[0].message.content #get only the content of the message 
    print("INVOICE PROCESSED")
    return result 