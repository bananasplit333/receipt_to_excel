from utilities.openai_client import client 

def process_receipt(input, categories):
    message = [{
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
          Categories can be found here ```{categories}```

          Your output should resemble the following structure, strictly adhering to these categories and format:
          ````
          Item: 
            Groceries & Food
              ORG SUGAR, 4.99
              DC FIGS, 2.99
            Electronics & Appliances
            Home & Living
          Store: Costco
          Tax: 4.20
          Total Cost: 50.00
          ````
          Ensure the returned file strictly follows this format, with items and categories correctly placed based on the receipt(s) provided. Make sure not to hallucinate any values or items.
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
    return result 