import streamlit as st
import requests
import time

# إعدادات الصفحة
st.set_page_config(page_title="صانع الفيديوهات الذكي", layout="centered")

st.title("🎬 صانع الفيديوهات بالذكاء الاصطناعي")
st.write("تحويل صورتك إلى فيديو حقيقي وحركي مجاناً.")

# الحصول على المفتاح من الـ Secrets
hf_token = st.secrets.get("HF_TOKEN")

if not hf_token:
    st.error("⚠️ يرجى إضافة مفتاح HF_TOKEN في الـ Secrets أولاً.")
    st.stop()

# رفع الصورة
uploaded_file = st.file_uploader("1️⃣ ارفع صورتك هنا", type=["jpg", "jpeg", "png"])

if uploaded_file:
    image_bytes = uploaded_file.read()
    st.image(image_bytes, caption="الصورة التي تم رفعها", use_container_width=True)

# كتابة الوصف
prompt = st.text_area("2️⃣ اكتب ماذا تريد أن يحدث في الفيديو (Prompt)", placeholder="مثال: Make the person blink and smile")

# زرار التوليد
if st.button("🚀 توليد الفيديو الآن", type="primary"):
    if not uploaded_file:
        st.warning("الرجاء رفع صورة أولاً!")
    elif not prompt:
        st.warning("الرجاء كتابة وصف للفيديو!")
    else:
        with st.spinner("⏳ جاري إرسال الصورة للسيرفر وتوليد الفيديو الحقيقي... قد يستغرق دقيقة..."):
            try:
                # الرابط والمفتاح بالمسافات الصحيحة تماماً لبايثون
                API_URL = "https://api-inference.huggingface.co/models/stabilityai/stable-video-diffusion-img2vid-xt"
                headers = {"Authorization": f"Bearer {hf_token}"}
                
                # إرسال الصورة للموديل
                response = requests.post(API_URL, headers=headers, data=image_bytes)
                
                if response.status_code == 200:
                    st.success("✨ تم توليد الفيديو الحقيقي بنجاح!")
                    st.video(response.content)
                elif response.status_code == 503:
                    st.info("⏳ السيرفر المجاني بيحمل الموديل حالياً (بياخد حوالي دقيقة)، استنى ثواني واضغط على الزرار تاني.")
                else:
                    st.error(f"حدث خطأ في السيرفر: {response.status_code}")
                    
            except Exception as e:
                st.error(f"عذراً، حدث خطأ أثناء الاتصال: {str(e)}")
