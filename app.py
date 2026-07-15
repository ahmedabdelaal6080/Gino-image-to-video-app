import streamlit as st
from PIL import Image, ImageEnhance
import numpy as np
import imageio
import os
import random

# إعدادات الصفحة
st.set_page_config(page_title="صانع الفيديوهات الذكي", layout="centered")

st.title("🎬 صانع الفيديوهات الحركية والأكشن")
st.write("ارفع صورتك واختر طريقة التحريك المناسبة لك مجاناً وبدون حدود!")

# اختيار وضع التشغيل
mode = st.radio(
    "⚙️ اختر وضع توليد الفيديو:",
    ["الوضع الاقتصادي (مجاني 100% وبدون حدود)", "الوضع الاحترافي الواقعي (يتطلب مفتاح API)"]
)

# لو اختار الوضع الواقعي، نظهر له خانة يحط فيها مفتاح Fal الخاص بيه ونشرح له يجيبه منين
user_fal_key = ""
if mode == "الوضع الاحترافي الواقعي (يتطلب مفتاح API)":
    st.info("💡 هذا الوضع يحرك ملامح الشخص وجسده بشكل واقعي جداً. لتشغيله مجاناً:")
    st.markdown("1. سجل دخولك في موقع [Fal.ai](https://fal.ai) باستخدام حساب GitHub.\n2. اذهب لصفحة الـ Keys واعمل مفتاح جديد وانسخه.\n3. ضعه في الخانة بالأسفل.")
    user_fal_key = st.text_input("🔑 اكتب مفتاح FAL_KEY الخاص بك هنا:", type="password")

# رفع الصورة
uploaded_file = st.file_uploader("1️⃣ ارفع صورتك هنا", type=["jpg", "jpeg", "png"])

if uploaded_file:
    # حفظ الصورة للتعامل معها
    with open("temp_img.png", "wb") as f:
        f.write(uploaded_file.getbuffer())
        
    image = Image.open("temp_img.png")
    st.image(image, caption="الصورة المرفوعة", use_container_width=True)

    # كتابة وصف الحركة
    prompt = st.text_area("2️⃣ اكتب الحركة أو الأكشن المطلوب (بالإنجليزي)", placeholder="مثال للواقعي: The person smiles | مثال للاقتصادي: explosion")

    # زرار التوليد
    if st.button("🚀 توليد الفيديو الآن", type="primary"):
        if not prompt:
            st.warning("الرجاء كتابة وصف للحركة أولاً!")
        else:
            # --- تشغيل الوضع الاحترافي الواقعي ---
            if mode == "الوضع الاحترافي الواقعي (يتطلب مفتاح API)":
                if not user_fal_key:
                    st.error("⚠️ يرجى كتابة مفتاح الـ FAL_KEY الخاص بك لتشغيل هذا الوضع!")
                else:
                    with st.spinner("⏳ جاري تحريك الشخصية واقعياً عبر سيرفر Fal AI..."):
                        try:
                            import fal_client
                            os.environ["FAL_KEY"] = user_fal_key
                            
                            # رفع الصورة وتوليد الفيديو
                            image_url = fal_client.upload_file("temp_img.png")
                            result = fal_client.subscribe(
                                "fal-ai/ltx-video/image-to-video",
                                arguments={
                                    "image_url": image_url,
                                    "prompt": prompt,
                                    "num_frames": 97,
                                    "fps": 24
                                }
                            )
                            video_url = result.get("video", {}).get("url")
                            if video_url:
                                st.success("✨ تم تحريك الشخصية واقعياً بنجاح!")
                                st.video(video_url)
                            else:
                                st.error("فشل الحصول على الفيديو، تأكد من صحة المفتاح ورصيدك.")
                        except Exception as e:
                            st.error(f"حدث خطأ في السيرفر: {str(e)}")

            # --- تشغيل الوضع الاقتصادي (المجاني والآمن للأبد) ---
            else:
                with st.spinner("⏳ جاري توليد تأثيرات الحركة والأكشن محلياً..."):
                    try:
                        if image.mode != 'RGB':
                            image = image.convert('RGB')
                        w, h = image.size
                        w, h = (w // 16) * 16, (h // 16) * 16
                        base_img = image.resize((w, h))
                        
                        frames = []
                        user_prompt = prompt.lower()
                        is_action = any(word in user_prompt for word in ["jump", "explosion", "shake", "action", "attack"])
                        
                        for i in range(120):
                            frame = base_img.copy()
                            if is_action:
                                dx, dy = random.randint(-14, 14), random.randint(-14, 14)
                                frame = frame.transform((w, h), Image.Transform.AFFINE, (1, 0, dx, 0, 1, dy))
                                if i % 8 < 3:
                                    frame = ImageEnhance.Brightness(frame).enhance(1.6)
                            else:
                                scale = 1.0 + (i * 0.0015)
                                nw, nh = int(w * scale), int(h * scale)
                                frame = frame.resize((nw, nh)).crop(((nw-w)//2, (nh-h)//2, (nw-w)//2+w, (nh-h)//2+h))
                            frames.append(np.array(frame))
                        
                        video_path = "action_movie.mp4"
                        imageio.mimsave(video_path, frames, fps=12, macro_block_size=None)
                        
                        st.success("💥 تم توليد الفيديو الحركي بنجاح!")
                        st.video(video_path)
                        
                        # تشغيل الصوت المناسب
                        if is_action:
                            st.audio("https://www.soundjay.com/mechanical/sounds/explosion-01.mp3", format="audio/mp3", autoplay=True)
                        else:
                            st.audio("https://www.soundjay.com/buttons/sounds/button-09.mp3", format="audio/mp3", autoplay=True)
                    except Exception as e:
                        st.error(f"حدث خطأ أثناء المعالجة المحلية: {str(e)}")
