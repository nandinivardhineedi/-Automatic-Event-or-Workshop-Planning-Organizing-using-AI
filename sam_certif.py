import gspread
from oauth2client.service_account import ServiceAccountCredentials
import pandas as pd
import os
from PIL import Image, ImageDraw, ImageFont

# Configure the Google Sheets API
scope = ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/drive"]
creds = ServiceAccountCredentials.from_json_keyfile_name("credentials.json", scope)
client = gspread.authorize(creds)

# Google Sheet ID (Replace with your actual spreadsheet ID)
spreadsheet_id = "1Veye3gr_6n5vAZqK179R2V5dzM5Eb_6112kgnBfiJb4"
spreadsheet = client.open_by_key(spreadsheet_id)

# Select the first worksheet
sheet = spreadsheet.get_worksheet(0)

# Get all the data from the sheet
data = sheet.get_all_records()

# Convert data to DataFrame
df = pd.DataFrame(data)

# Check the structure of the DataFrame
print("Data loaded successfully. Columns are:")
print(df.columns)

# Column names (modify as per your sheet structure)
name_column = "Name"  # Column with participant names

# Create a folder to store generated certificates
certificate_folder = "generated_certificates"
if not os.path.exists(certificate_folder):
    os.makedirs(certificate_folder)

# Certificate template path (provide your template file path here)
certificate_template = "certificate_template.png"  # Replace with your template image file
font_path = "arial.ttf"  # Replace with your font file path

# Generate and save certificates
for index, row in df.iterrows():
    name = row[name_column]

    try:
        # Open the certificate template
        image = Image.open(certificate_template)
        draw = ImageDraw.Draw(image)

        # Customize font size, style, and color
        font_size = 60  # Adjust as needed
        font = ImageFont.truetype(font_path, font_size)
        text_color = (255, 215, 0)  # Gold color for a luxurious look

        # Get the size of the text to center it
        text_bbox = font.getbbox(name)
        text_width = text_bbox[2] - text_bbox[0]
        text_height = text_bbox[3] - text_bbox[1]

        # Calculate the position (centered horizontally)
        image_width, image_height = image.size
        x_position = (image_width - text_width) / 2
        y_position = image_height / 2  # Adjust as needed

        # Add the participant's name to the certificate
        draw.text((x_position, y_position), name, font=font, fill=text_color)

        # Save the generated certificate
        file_name = f"{name.replace(' ', '_')}_certificate.png"
        file_path = os.path.join(certificate_folder, file_name)
        image.save(file_path)

        print(f"Generated certificate for {name} as {file_name}.")
    except Exception as e:
        print(f"Error generating certificate for {name}: {str(e)}")

print("All certificates generated!")
