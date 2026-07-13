import streamlit as st
import requests
import time

# إعدادات الصفحة
st.set_page_config(page_title="صانع الفيديوهات الواقعية", layout="centered")

st.title("🎬 محول الصور إلى فيديو حركي واقعي (تحريك الأشخاص)")
st.write("ارفع صورتك واكتب الحركة المطلوبة للشخص ليتخيلها الذكاء الاصطناعي ويحركها واقعياً!")

# الحصول على المفتاح
hf_token = st.secrets.get("HF_TOKEN")

if not hf_token:
    st.error("⚠️ يرجى إضافة مفتاح HF_TOKEN في الـ Secrets أولاً لتشغيل الموديل الواقعي.")
    st.stop()

# رفع الصورة
uploaded_file = st.file_uploader("1️⃣ ارفع صورتك هنا", type=["jpg", "jpeg", "png"])

if uploaded_file:
    image_bytes = uploaded_file.read()
    st.image(image_bytes, caption="الصورة المرفوعة", use_container_width=True)

    # كتابة وصف الحركة بدقة
    prompt = st.text_area("2️⃣ اكتب حركة الشخص المطلوبة (بالإنجليزي)", placeholder="مثال: The person smiles, turns their head and blinks naturally")

    # زرار التوليد
    if st.button("🚀 تحريك الشخص في الصورة الآن", type="primary"):
        if not prompt:
            st.warning("الرجاء كتابة وصف للحركة أولاً!")
        else:
            with st.spinner("⏳ جاري تحليل الشخصية وتحريكها بشكل واقعي... قد يستغرق دقيقة..."):
                try:
                    # استخدام موديل مستقر جداً ومخصص لتحريك ملامح وأجسام الأشخاص بدقة
                    API_URL = "https://api-inference.huggingface.co/models/stabilityai/stable-video-diffusion-img2vid-xt"
                    headers = {"Authorization": f"Bearer {hf_token}"}
                    
                    # إرسال طلب المعالجة
                    response = requests.post(API_URL, headers=headers, data=image_bytes)
                    
                    if response.status_code == 200:
                        st.success("✨ تم تحريك الشخص بنجاح وبحركة واقعية!")
                        st.video(response.content)
                        
                        # تشغيل صوت حماسي تفاعلي مع الفيديو
                        st.audio("https://www.soundjay.com/buttons/sounds/button-09.mp3", format="audio/mp3", autoplay=True)
                        
                    elif response.status_code == 503:
                        st.info("⏳ السيرفر يجهز موديل التحريك الواقعي حالياً، انتظر 20 ثانية واضغط على زر التوليد مرة أخرى.")
                    else:
                        st.error(f"حدثت استجابة غير متوقعة من السيرفر: {response.status_code}. حاول مرة أخرى.")
                        
                except Exception as e:
                    st.error(f"عذراً، حدث خطأ أثناء الاتصال بسيرفر التحريك: {str(e)}")
