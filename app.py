import streamlit as st
import fal_client
import os

# إعدادات الصفحة
st.set_page_config(page_title="صانع الفيديوهات بالذكاء الاصطناعي", layout="centered")

st.title("🎬 صانع الفيديوهات بالذكاء الاصطناعي")
st.write("حوّل صورك إلى فيديوهات إبداعية في ثوانٍ معدودة.")

# التأكد من وجود المفتاح السري
if "FAL_KEY" in st.secrets:
    os.environ["FAL_KEY"] = st.secrets["FAL_KEY"]
else:
    st.error("رجاءً قم بإضافة FAL_KEY في إعدادات Secrets أولاً.")

# رفع الصورة
uploaded_file = st.file_uploader("1️⃣ ارفع صورتك هنا", type=["jpg", "jpeg", "png"])

if uploaded_file:
    st.image(uploaded_file, caption="الصورة التي تم رفعها", use_container_width=True)

# كتابة الوصف
prompt = st.text_area("2️⃣ اكتب ماذا تريد أن يحدث في الفيديو (Prompt)", placeholder="مثال: A majestic dragon flying over mountains...")

# زرار التوليد الفعلي
if st.button("🚀 توليد الفيديو الآن", type="primary"):
    if not uploaded_file:
        st.warning("الرجاء رفع صورة أولاً!")
    elif not prompt:
        st.warning("الرجاء كتابة وصف للفيديو!")
    else:
        with st.spinner("⏳ جاري توليد الفيديو... قد يستغرق الأمر دقيقة، يرجى الانتظار."):
            try:
                # حفظ الصورة مؤقتاً لإرسالها للـ API
                with open("temp_image.png", "wb") as f:
                    f.write(uploaded_file.getbuffer())
                
                # رفع الصورة مؤقتاً لـ fal
                image_url = fal_client.upload_file("temp_image.png")
                
                # استدعاء موديل توليد الفيديو (Luma Dream Machine)
                result = fal_client.subscribe(
                    "fal-ai/luma-dream-machine/image-to-video",
                    max_concurrency=10,
                    arguments={
                        "image_url": image_url,
                        "prompt": prompt
                    }
                )
                
                # عرض الفيديو الناتج
                video_url = result['video']['url']
                st.success("✨ تم توليد الفيديو بنجاح!")
                st.video(video_url)
                
                # مسح الملف المؤقت
                if os.path.exists("temp_image.png"):
                    os.remove("temp_image.png")
                    
            except Exception as e:
                st.error(f"حدث خطأ أثناء التوليد: {str(e)}")
