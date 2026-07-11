import streamlit as st
import requests
import time

# إعدادات الصفحة
st.set_page_config(page_title="صانع فيديوهات الصور", layout="centered")

st.title("🎬 محول الصور إلى فيديو بالذكاء الاصطناعي")
st.write("ارفع صورتك واكتب الحركة اللي عايزها عشان تتحول لفيديو حقيقي مجاناً.")

# الحصول على المفتاح من الـ Secrets
hf_token = st.secrets.get("HF_TOKEN")

if not hf_token:
    st.error("⚠️ يرجى إضافة مفتاح HF_TOKEN في الـ Secrets أولاً.")
    st.stop()

# رفع الصورة
uploaded_file = st.file_uploader("1️⃣ ارفع صورتك هنا", type=["jpg", "jpeg", "png"])

if uploaded_file:
    image_bytes = uploaded_file.read()
    st.image(image_bytes, caption="الصورة المرفوعة", use_container_width=True)

# كتابة الوصف
prompt = st.text_area("2️⃣ اكتب ماذا تريد أن يحدث في الصورة (بالإنجليزية)", placeholder="مثال: Make the person smile and wave hand")

# زرار التوليد
if st.button("🚀 تحويل الصورة إلى فيديو الآن", type="primary"):
    if not uploaded_file:
        st.warning("الرجاء رفع صورة أولاً!")
    elif not prompt:
        st.warning("الرجاء كتابة وصف للحركة!")
    else:
        with st.spinner("⏳ جاري معالجة الصورة وتحويلها إلى فيديو... يرجى الانتظار دقيقة..."):
            try:
                # استخدام رابط سيرفر مخصص ومستقر للصور
                API_URL = "https://api-inference.huggingface.co/models/stabilityai/stable-video-diffusion-img2vid"
                headers = {"Authorization": f"Bearer {hf_token}"}
                
                # إرسال الصورة كبيانات مباشرة
                response = requests.post(API_URL, headers=headers, data=image_bytes)
                
                if response.status_code == 200:
                    st.success("✨ تم تحويل الصورة إلى فيديو بنجاح!")
                    st.video(response.content)
                elif response.status_code == 503:
                    st.info("⏳ السيرفر المجاني بيجهز الموديل حالياً، انتظر 30 ثانية واضغط على الزرار مرة ثانية.")
                else:
                    st.error(f"استجابة السيرفر: {response.status_code}. اضغط على الزرار مرة أخرى لإعادة المحاولة.")
                    
            except Exception as e:
                st.error(f"عذراً، حدث خطأ أثناء الاتصال: {str(e)}")
