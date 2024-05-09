# Overview

This code utilizes OpenAI's GPT-4 Vision API to parse information from a series of receipts, and outputs an Excel file with the extracted information.

# Functionality

The code defines a function parse_receipt that takes an image URL and image data as input, and uses the GPT-4 Vision API to extract information from the receipt. The function then parses the extracted information and returns the extracted name, category, and cost.

# Output
The output of the code is an Excel file containing the extracted information in the following format:

Name	Category    Cost
[Name]	[Category]	[Cost]
Example Usage

The example usage demonstrates how to use the parse_receipt function to parse a receipt image and extract the information.


# Code example: 
image_url = "https://example.com/image.jpg"
image_data = httpx.get(image_url).content
name, category, cost = parse_receipt(image_url, image_data)

print("Name:", name)
print("Category:", category)
print("Cost:", cost)

# Save the extracted information to an Excel file
df = pd.DataFrame({
    "Name": [name],
    "Category": [category],
    "Cost": [cost]
})
df.to_excel("receipt_info.xlsx", index=False)
Note

This code assumes that the receipt images are in JPEG format and contain the extracted information in the format specified in the prompt. You may need to modify the code to accommodate different image formats or extracted information formats.

