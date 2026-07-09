import streamlit as st

# إعدادات الصفحة
st.set_page_config(page_title="AI Image to Video Maker", layout="centered")

# عنوان الموقع
st.title("🎬 صانع الفيديوهات بالذكاء الاصطناعي")
st.write("حول صورك إلى فيديوهات إبداعية في ثوانٍ معدودة!")

st.divider()

# الجزء الخاص برفع الصورة
st.subheader("1️⃣ ارفع صورتك هنا")
uploaded_file = st.file_uploader("اختار صورة بصيغة PNG أو JPG...", type=["jpg", "jpeg", "png"])

if uploaded_file is not None:
    # عرض الصورة للمستخدم بعد الرفع
    st.image(uploaded_file, caption="الصورة التي تم رفعها", use_container_width=True)

st.divider()

# الجزء الخاص بكتابة الوصف
st.subheader("2️⃣ اكتب ماذا تريد أن يحدث في الفيديو (Prompt)")
prompt = st.text_area("اكتب الوصف بالإنجليزي لأفضل نتائج (مثلاً: A majestic dragon flying over mountains)...")

st.divider()

# زر التشغيل
if st.button("🚀 توليد الفيديو الآن", type="primary"):
    if uploaded_file is not None and prompt != "":
        with st.spinner("جاري تهيئة التصميم... (شكل الموقع المبدئي جاهز)"):
            st.info("ممتاز! الواجهة شغال تمام. في الخطوة الجاية هنربط الـ API عشان الفيديو يشتغل بجد.")
    else:
        st.warning("من فضلك ارفع صورة واكتب الوصف أولاً!")
