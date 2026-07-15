import streamlit as st
import requests
import time

# إعدادات الصفحة
st.set_page_config(page_title="مُرمم الصور القديمة", layout="centered")

st.title("📸 مُرمم الصور القديمة بالذكاء الاصطناعي")
st.write("ارفع صورتك القديمة أو الباهتة، وشاهدها تتحول إلى صورة حديثة وعالية الدقة فوراً بدون تغيير الملامح!")

# الحصول على المفتاح من الـ Secrets (هنستخدم سيرفر Hugging Face المستقر جداً في الصور)
hf_token = st.secrets.get("HF_TOKEN")

if not hf_token:
    st.error("⚠️ يرجى إضافة مفتاح HF_TOKEN في الـ Secrets أولاً لتشغيل نظام الترميم.")
    st.stop()

# رفع الصورة القديمة
uploaded_file = st.file_uploader("1️⃣ ارفع الصورة القديمة هنا", type=["jpg", "jpeg", "png"])

if uploaded_file:
    image_bytes = uploaded_file.read()
    
    # عرض الصورة الأصلية والنتيجة جنب بعض
    col1, col2 = st.columns(2)
    
    with col1:
        st.image(image_bytes, caption="الصورة الأصلية (القديمة)", use_container_width=True)

    # زرار بدء الترميم
    if st.button("✨ ابدأ ترميم وتحسين الصورة الآن", type="primary"):
        with col2:
            with st.spinner("⏳ جاري إزالة الخدوش وتحسين الملامح بدقة..."):
                try:
                    # استخدام رابط سيرفر الترميم وتوضيح الوجوه (CodeFormer) المستقر جداً للصور
                    API_URL = "https://api-inference.huggingface.co/models/sczhou/CodeFormer"
                    headers = {"Authorization": f"Bearer {hf_token}"}
                    
                    # إرسال الصورة للسيرفر
                    response = requests.post(API_URL, headers=headers, data=image_bytes)
                    
                    if response.status_code == 200:
                        st.success("⚡ تم الترميم بنجاح!")
                        st.image(response.content, caption="الصورة بعد الترميم الحديث", use_container_width=True)
                        st.balloons() # حركة احتفالية بالنجاح
                    elif response.status_code == 503:
                        st.info("⏳ السيرفر بيجهز موديل الترميم حالياً، انتظر 15 ثانية واضغط على الزرار مرة أخرى.")
                    else:
                        st.error(f"استجابة السيرفر: {response.status_code}. اضغط على الزرار لإعادة المحاولة.")
                        
                except Exception as e:
                    st.error(f"عذراً، حدث خطأ أثناء الاتصال بسيرفر الترميم: {str(e)}")
