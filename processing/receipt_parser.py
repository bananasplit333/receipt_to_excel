#parse text into readable json format 
def parse_receipt_to_json(receipt_text):
  # Splitting the text into lines
  lines = receipt_text.strip().split("\n")
  
  # Initializing variables
  current_category = ""
  parsed_data = {}
  # Iterating through each line
  for line in lines:
      # Check if the line represents a category
      if line.strip() and line[0] != " ":
          # New category
          current_category = line.strip()
          parsed_data[current_category] = []
      elif line.strip():
          # Item line, assumed to have the format "NAME, PRICE"
          item_name, item_price = line.strip().rsplit(", ", 1)
          parsed_data[current_category].append({"name": item_name, "price": float(item_price)})
  return parsed_data


