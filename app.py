import streamlit as st
from PIL import Image, ImageEnhance
import numpy as np
import imageio
import os
import random

# إعدادات الصفحة
st.set_page_config(page_title="صانع فيديوهات الأكشن المطور", layout="centered")

st.title("🎬 صانع فيديوهات الأكشن والمؤثرات الصوتية")
st.write("ارفع صورتك واكتب الحركة أو الأكشن المطلوب (بالإنجليزي) لتوليد فيديو 10 ثواني مجاناً!")

# رفع الصورة
uploaded_file = st.file_uploader("1️⃣ ارفع صورتك هنا", type=["jpg", "jpeg", "png"])

if uploaded_file:
    image = Image.open(uploaded_file)
    if image.mode != 'RGB':
        image = image.convert('RGB')
        
    st.image(image, caption="الصورة المرفوعة", use_container_width=True)

    # كتابة وصف الحركة والأكشن
    prompt = st.text_area("2️⃣ اكتب الأكشن المطلوب (مثال: jump, explosion, shake)")

    # زرار التوليد
    if st.button("🚀 توليد فيديو الأكشن بالصوت الآن", type="primary"):
        with st.spinner("⏳ جاري تحريك الصورة وتوليد فيديو 10 ثواني... يرجى الانتظار ثواني..."):
            try:
                w, h = image.size
                # ضبط المقاسات لتكون زوجية ومناسبة للمشغلات
                w = (w // 16) * 16
                h = (h // 16) * 16
                base_img = image.resize((w, h))
                
                frames = []
                user_prompt = prompt.lower() if prompt else ""
                is_action = any(word in user_prompt for word in ["jump", "explosion", "shake", "action", "attack"])
                
                # توليد 120 إطار عشان الفيديو يوصل لـ 10 ثواني تقريباً (على سرعة 12 إطار في الثانية)
                for i in range(120):
                    frame = base_img.copy()
                    
                    if is_action:
                        # تأثير اهتزاز الأكشن العنيف المتواصل
                        dx = random.randint(-14, 14)
                        dy = random.randint(-14, 14)
                        frame = frame.transform((w, h), Image.Transform.AFFINE, (1, 0, dx, 0, 1, dy))
                        
                        # تأثير وميض الانفجارات المتقطع طوال الـ 10 ثواني
                        if i % 8 < 3:
                            enhancer = ImageEnhance.Brightness(frame)
                            frame = enhancer.enhance(1.6)
                    else:
                        # تأثير زووم سينمائي هادئ وبطيء جداً يناسب الـ 10 ثواني
                        scale = 1.0 + (i * 0.0015)
                        nw, nh = int(w * scale), int(h * scale)
                        frame_res = frame.resize((nw, nh))
                        frame = frame_res.crop(((nw-w)//2, (nh-h)//2, (nw-w)//2+w, (nh-h)//2+h))
                    
                    frames.append(np.array(frame))
                
                # حفظ الفيديو بصيغة متوافقة تماماً مع الويب والمتصفحات (WebM / MP4 المتوافق)
                video_path = "action_movie.mp4"
                
                # استخدام فلاتر تضمن تشغيل الفيديو على المتصفح دون شاشة سوداء
                imageio.mimsave(video_path, frames, fps=12, macro_block_size=None)
                
                # عرض الفيديو في التطبيق
                if os.path.exists(video_path):
                    st.success("💥 تم توليد الفيديو الطويل وتحريك الأكشن بنجاح!")
                    st.video(video_path)
                
                # تشغيل الصوت في المتصفح
                if is_action:
                    st.audio("https://www.soundjay.com/mechanical/sounds/explosion-01.mp3", format="audio/mp3", autoplay=True)
                else:
                    st.audio("https://www.soundjay.com/buttons/sounds/button-09.mp3", format="audio/mp3", autoplay=True)
                    
            except Exception as e:
                st.error(f"عذراً، حدث خطأ أثناء المعالجة: {str(e)}")
