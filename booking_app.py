import streamlit as st
import gspread
from oauth2client.service_account import ServiceAccountCredentials
from datetime import datetime, timedelta

# เชื่อมต่อ Google Sheet
scope = ["https://spreadsheets.google.com/feeds","https://www.googleapis.com/auth/drive"]
creds = ServiceAccountCredentials.from_json_keyfile_name("credentials.json", scope)
client = gspread.authorize(creds)
SHEET_ID = "1Pi2vH3ME2usLqaSYPc2ZtlG0xYyY6r7oOsdKh8-T-IQ"
sheet = client.open_by_key(SHEET_ID).sheet1

st.set_page_config(page_title="Booking System", layout="centered")

# CSS สำหรับฟอนต์ Kanit สี #158dc8
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Kanit:wght@600&display=swap');

.header-title {
    font-family: 'Kanit', sans-serif;
    font-weight: 600;
    color: #158dc8;
    font-size: 2.8rem;
    text-align: center;
    margin-bottom: 0.2rem;
}

.section-header {
    font-family: 'Kanit', sans-serif;
    font-weight: 600;
    color: #158dc8;
    font-size: 1.6rem;
    margin-top: 1.5rem;
    margin-bottom: 0.5rem;
}
</style>
""", unsafe_allow_html=True)

# หัวข้อใหญ่
st.markdown('<h1 class="header-title">ระบบจองคิว</h1>', unsafe_allow_html=True)
st.markdown("---")

# ข้อมูลผู้จอง
st.markdown('<div class="section-header">ข้อมูลผู้จอง</div>', unsafe_allow_html=True)
customer_name = st.text_input("ชื่อผู้จอง", max_chars=50)
customer_phone = st.text_input("เบอร์โทรศัพท์", max_chars=15)

st.markdown("---")

# วันที่จัดงาน
st.markdown('<div class="section-header">วันที่จัดงาน</div>', unsafe_allow_html=True)
col1, col2, col3 = st.columns([2, 2, 1])
with col1:
    start_date = st.date_input("วันเริ่มงาน")
with col2:
    work_days = st.number_input("จำนวนวันจัดงาน", min_value=1, step=1, value=1)
with col3:
    end_date = start_date + timedelta(days=work_days - 1)
    st.markdown(f"วันสิ้นสุดงาน: {end_date.strftime('%d/%m/%Y')}")

st.markdown("---")

# สถานที่จัดงาน
location = st.text_input("สถานที่จัดงาน", placeholder="โลเคชั่นสถานที่จัดงาน")

st.markdown("---")

# ประเภทเวลา
st.markdown('<div class="section-header">ประเภทเวลา</div>', unsafe_allow_html=True)
time_type = st.radio("เลือกช่วงเวลา", ["ครึ่งวัน (4 ชั่วโมง)", "เต็มวัน (8 ชั่วโมง)"])
half_day_slot = None
if time_type.startswith("ครึ่งวัน"):
    half_day_slot = st.selectbox("เลือกช่วงเวลาครึ่งวัน", ["07.00–11.00", "13.00–17.00"])

st.markdown("---")

# ทีมงานที่ต้องการ
st.markdown('<div class="section-header">ทีมงานที่ต้องการ</div>', unsafe_allow_html=True)
col1, col2 = st.columns(2)
with col1:
    num_photo = st.number_input("จำนวนช่างภาพ", min_value=0, step=1)
with col2:
    num_video = st.number_input("จำนวนช่างวิดีโอ", min_value=0, step=1)

st.markdown("---")

# ฟังก์ชันคำนวณราคาตามโจทย์
def get_photo_base_price(day_count):
    if day_count == 1:
        return 4500
    elif day_count == 2:
        return 8500
    else:
        # ถ้าจำนวนวันมากกว่า 2 ใช้ราคาวันละ 8500 + เพิ่มวันละ 1500 (หรือปรับตามจริง)
        return 8500 + (day_count - 2)*1500

def get_video_base_price(day_count):
    if day_count == 1:
        return 5500
    elif day_count == 2:
        return 9500
    else:
        return 9500 + (day_count - 2)*1500

def get_extra_price(day_count):
    if day_count == 1:
        return 3000
    elif day_count == 2:
        return 6000
    else:
        return 6000 + (day_count - 2)*1500

# คำนวณราคาช่างภาพ
photo_total = 0
if num_photo > 0:
    base_photo = get_photo_base_price(work_days)
    extra_photo = get_extra_price(work_days)
    photo_total = base_photo + extra_photo * max(0, num_photo - 1)

# คำนวณราคาช่างวิดีโอ
video_total = 0
if num_video > 0:
    base_video = get_video_base_price(work_days)
    extra_video = get_extra_price(work_days)
    video_total = base_video + extra_video * max(0, num_video - 1)

total_price = photo_total + video_total
deposit = 1000
balance = total_price - deposit

st.markdown('<div class="section-header">สรุปค่าใช้จ่าย</div>', unsafe_allow_html=True)
st.markdown(f"""
- ค่าช่างภาพ: {photo_total:,.0f} บาท  
- ค่าช่างวิดีโอ: {video_total:,.0f} บาท  
- รวมทั้งหมด: {total_price:,.0f} บาท  
- มัดจำล่วงหน้า: {deposit:,.0f} บาท  
- คงเหลือชำระวันงาน: {balance:,.0f} บาท
""")

st.markdown("---")

# ข้อมูลการชำระเงิน
st.markdown('<div class="section-header">ข้อมูลการชำระเงิน</div>', unsafe_allow_html=True)
st.markdown("""
**บัญชี**: พร้อมเพย์  
**เลขที่บัญชี**: 0651185880  
**ชื่อบัญชี**: วุฒิพงษ์ คำคง
""")

receipt = st.file_uploader("อัปโหลดสลิป/หลักฐานการชำระเงิน", type=["png", "jpg", "jpeg", "pdf"])

st.markdown("---")

# ยืนยันและแสดงสรุปการจอง
if st.button("ยืนยันการจอง"):
    if not customer_name or not customer_phone:
        st.error("กรุณากรอกชื่อผู้จองและเบอร์โทรศัพท์ให้ครบถ้วน")
    elif num_photo == 0 and num_video == 0:
        st.error("กรุณาเลือกจำนวนช่างภาพหรือช่างวิดีโออย่างน้อย 1 คน")
    else:
        timestamp = datetime.now().strftime("%d/%m/%Y %H:%M:%S")
        booking_info = [
            timestamp,
            customer_name,
            customer_phone,
            f"{start_date.strftime('%d/%m/%Y')} - {end_date.strftime('%d/%m/%Y')}",
            location,
            f"{time_type}" + (f" ({half_day_slot})" if half_day_slot else ""),
            num_photo,
            num_video,
            photo_total,
            video_total,
            total_price,
            deposit,
            balance
        ]
        sheet.append_row(booking_info)

        booking_data = {
            "ชื่อผู้จอง": customer_name,
            "เบอร์โทรศัพท์": customer_phone,
            "วันเริ่มงาน": start_date.strftime('%d/%m/%Y'),
            "วันสิ้นสุดงาน": end_date.strftime('%d/%m/%Y'),
            "จำนวนวันจัดงาน": f"{work_days} วัน",
            "สถานที่จัดงาน": location,
            "ช่วงเวลา": f"{time_type}" + (f" ({half_day_slot})" if half_day_slot else ""),
            "จำนวนช่างภาพ": f"{num_photo} คน",
            "จำนวนช่างวิดีโอ": f"{num_video} คน",
            "ค่าช่างภาพ": f"{photo_total:,.0f} บาท",
            "ค่าช่างวิดีโอ": f"{video_total:,.0f} บาท",
            "รวมทั้งหมด": f"{total_price:,.0f} บาท",
            "มัดจำ": f"{deposit:,.0f} บาท",
            "คงเหลือชำระ": f"{balance:,.0f} บาท",
        }

        st.success("จองคิวเรียบร้อยแล้ว!")

        st.markdown('<div class="section-header">สรุปข้อมูลการจอง</div>', unsafe_allow_html=True)
        for key, val in booking_data.items():
            st.write(f"**{key}**: {val}")
