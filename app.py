import streamlit as st
import requests
import time

# إعدادات الصفحة
st.set_page_config(page_title="صانع الفيديوهات السريع", layout="centered")

st.title("🎬 صانع الفيديوهات بالذكاء الاصطناعي")
st.write("اكتب وصفاً ليتحول إلى فيديو حقيقي وحركي مجاناً.")

# الحصول على المفتاح من الـ Secrets
hf_token = st.secrets.get("HF_TOKEN")

if not hf_token:
    st.error("⚠️ يرجى إضافة مفتاح HF_TOKEN في الـ Secrets أولاً.")
    st.stop()

# كتابة الوصف
prompt = st.text_area("1️⃣ اكتب وصفاً للفيديو الذي تريده بالإنجليزية (Prompt)", placeholder="مثال: A cute cat playing with a ball, high quality")

# زرار التوليد
if st.button("🚀 توليد الفيديو الآن", type="primary"):
    if not prompt:
        st.warning("الرجاء كتابة وصف للفيديو أولاً!")
    else:
        with st.spinner("⏳ جاري الاتصال بالسيرفر وتوليد فيديو حقيقي من وصفك... يرجى الانتظار دقيقة..."):
            try:
                # استخدام موديل نص إلى فيديو مستقر ومفتوح دايماً في الـ API المجاني
                API_URL = "https://api-inference.huggingface.co/models/damo-vilab/modelscope-damo-text-to-video-hd"
                headers = {"Authorization": f"Bearer {hf_token}"}
                
                # إرسال الوصف
                response = requests.post(API_URL, headers=headers, json={"inputs": prompt})
                
                if response.status_code == 200:
                    st.success("✨ تم توليد الفيديو بنجاح!")
                    st.video(response.content)
                elif response.status_code == 503:
                    st.info("⏳ السيرفر بيحمل الموديل حالياً (بياخد حوالي دقيقة)، استنى شوية واضغط على الزرار تاني.")
                else:
                    st.error(f"حدث خطأ في السيرفر: {response.status_code}. قد يكون الموديل مشغولاً حالياً.")
                    
            except Exception as e:
                st.error(f"عذراً، حدث خطأ أثناء الاتصال: {str(e)}")
