# Reload the newly uploaded image and process it again
input_path_new = "/mnt/data/WhatsApp Image 2025-05-10 at 15.36.47_5602f8d5.jpg"
output_path_new = "/mnt/data/final_resized_image.jpg"

# Open and resize the image to 240px width and 320px height
with Image.open(input_path_new) as img:
    resized_img = img.resize((240, 320))  # width=240, height=320

# Gradually adjust quality to fall within 100KB–140KB
for quality in range(100, 10, -1):
    resized_img.save(output_path_new, format='JPEG', quality=quality)
    file_size = os.path.getsize(output_path_new)
    if 100 * 1024 <= file_size <= 140 * 1024:
        break

output_path_new, file_size / 1024 