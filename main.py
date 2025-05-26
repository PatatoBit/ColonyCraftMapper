from PIL import Image, ImageDraw, ImageFont

# Load image
image_path = "map.png"
img = Image.open(image_path).convert("RGB")
draw = ImageDraw.Draw(img)
width, height = img.size

# Define world bounds (in blocks)
world_x_min, world_x_max = -6144, 6144   # total 122,880 blocks width
world_z_min, world_z_max = -3072, 3072   # total 61,440 blocks height

# Calculate scale (blocks per pixel)
scale_x = (world_x_max - world_x_min) / width   # 10 blocks/pixel
scale_z = (world_z_max - world_z_min) / height  # 10 blocks/pixel

# Convert world coordinate (wx, wz) to pixel coordinate (px, py)
def world_to_pixel(wx, wz):
    px = int((wx - world_x_min) / scale_x)
    py = int((wz - world_z_min) / scale_z)
    return px, py

# Setup font
try:
    font = ImageFont.truetype("arial.ttf", 32)  # Increased font size from 20 to 32
except:
    font = ImageFont.load_default()

# Grid spacing in world blocks
spacing = 100  # 1,000 blocks

# Draw vertical grid lines (x axis)
for x in range(((world_x_min // spacing) + 1) * spacing, world_x_max, spacing):
    px, _ = world_to_pixel(x, 0)
    if 0 <= px < width:
        draw.line([(px, 0), (px, height)], fill=(255, 0, 0), width=1)
        draw.text((px + 3, 3), f"x={x}", fill=(255, 255, 255), font=font)

# Draw horizontal grid lines (z axis)
for z in range(((world_z_min // spacing) + 1) * spacing, world_z_max, spacing):
    _, py = world_to_pixel(0, z)
    if 0 <= py < height:
        draw.line([(0, py), (width, py)], fill=(0, 255, 0), width=1)
        draw.text((3, py + 3), f"z={z}", fill=(255, 255, 255), font=font)

# Save output image
output_path = "earth_map_labeled_1k.png"
img.save(output_path)
print(f"Labeled map saved to {output_path}")
