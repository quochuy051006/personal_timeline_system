import streamlit as st
import os
import database as db
import services as sv

# Tự động kích hoạt tạo DB khi ứng dụng chạy
db.init_db()

# Tạo thư mục lưu ảnh tạm thời nếu chưa tồn tại
if not os.path.exists("stored_photos"):
    os.makedirs("stored_photos")

st.set_page_config(page_title="Personal Timeline", layout="centered")
st.title("🔒 Personal Timeline - Local-First PoC")

# --- VÙNG THÊM KỶ NIỆM MỚI ---
st.header("📸 Add New Memory")
user_story = st.text_area("Write your diary text here:")
uploaded_file = st.file_uploader("Choose a photo", type=["jpg", "jpeg"])

if st.button("Process & Save Securely"):
    if user_story and uploaded_file:
        # Bước 1: Lưu file tạm (Trạng thái UNPROCESSED)
        local_path = os.path.join("stored_photos", uploaded_file.name)
        with open(local_path, "wb") as f:
            f.write(uploaded_file.getbuffer())
        st.write("`[STATE 1]: UNPROCESSED -> File staged locally.`")
        
        # Bước 2: Trích xuất GPS (Trạng thái METADATA_EXTRACTED)
        gps_info = sv.extract_gps_from_photo(local_path)
        st.write(f"`[STATE 2]: METADATA_EXTRACTED -> Found GPS: {gps_info}`")
        
        # Bước 3: Mã hóa E2EE (Trạng thái ENCRYPTED)
        encrypted_text = sv.encrypt_payload(user_story)
        st.write("`[STATE 3]: ENCRYPTED -> Plaintext converted to Ciphertext:`")
        st.code(encrypted_text, language="text") # Hiện chuỗi băm cho thầy cô xem
        
        # Bước 4: Ghi vào DB (Trạng thái SAVED_LOCALLY)
        db.insert_media(local_path, gps_info, encrypted_text, "SAVED_LOCALLY")
        st.success("`[STATE 4]: SAVED_LOCALLY -> Encrypted record committed to SQLite!`")
        st.rerun() # Làm mới trang để cập nhật dòng thời gian
    else:
        st.error("Please provide both a story and a photo.")

# --- VÙNG HIỂN THỊ DÒNG THỜI GIAN (TIMELINE) ---
st.markdown("---")
st.header("📜 Your Secure Timeline")

memories = db.get_all_media()

for item in memories:
    # item[1]: file_path, item[2]: gps_coords, item[3]: encrypted_payload, item[4]: status
    with st.container():
        col1, col2 = st.columns([1, 2])
        with col1:
            if os.path.exists(item[1]):
                st.image(item[1], use_container_width=True)
        with col2:
            st.write(f"📍 **Location:** {item[2]}")
            st.caption(f"⚙️ **System State:** `{item[4]}`")
            
            # Tính năng giải mã trực quan ngay trên giao diện lúc xem
            decrypted_story = sv.decrypt_payload(item[3])
            st.info(f"✍️ **Decrypted Story:** {decrypted_story}")
            
            # Nút ẩn mở để xem chuỗi Ciphertext thô trong DB
            with st.expander("See Raw DB Ciphertext"):
                st.code(item[3], language="text")
        st.markdown("---")