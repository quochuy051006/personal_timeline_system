from exif import Image as ExifImage
from cryptography.fernet import Fernet

# Tạo một Secret Key cố định để mã hóa/giải mã trong buổi Demo
# (Trong thực tế key này sẽ sinh ra từ mật khẩu của User)
DEMO_KEY = b'G5K39fX9T2vB_mZ1pQW4eR7tY8uI0oP_aS2dF5gH1jK=' 
cipher_suite = Fernet(DEMO_KEY)

def extract_gps_from_photo(image_path):
    """Đọc header nhị phân EXIF để lấy tọa độ GPS (Block B)"""
    try:
        with open(image_path, 'rb') as img_file:
            img = ExifImage(img_file)
            
        if img.has_exif and hasattr(img, 'gps_latitude') and hasattr(img, 'gps_longitude'):
            lat = img.gps_latitude
            lon = img.gps_longitude
            # Đổi từ độ-phút-giây sang thập phân để hiển thị trực quan
            lat_dec = lat[0] + lat[1]/60 + lat[2]/3600
            lon_dec = lon[0] + lon[1]/60 + lon[2]/3600
            return f"{lat_dec:.4f} N, {lon_dec:.4f} E"
    except Exception as e:
        print(f"EXIF Parsing Error: {e}")
    return "No GPS Data (Unknown Location)"

def encrypt_payload(text_story):
    """Mã hóa đối xứng văn bản nhật ký sang Ciphertext (Block C)"""
    if not text_story:
        return ""
    encrypted_bytes = cipher_suite.encrypt(text_story.encode('utf-8'))
    return encrypted_bytes.decode('utf-8') # Trả về chuỗi string để lưu vào DB

def decrypt_payload(ciphertext):
    """Giải mã Ciphertext ngược lại thành văn bản gốc để hiển thị"""
    try:
        decrypted_bytes = cipher_suite.decrypt(ciphertext.encode('utf-8'))
        return decrypted_bytes.decode('utf-8')
    except Exception:
        return "[Decryption Failed - Invalid Key]"