# ============================================
# MP3 語音轉文字 Streamlit 應用
# 上傳 MP3 → Whisper 轉錄 → 下載 Word 檔
# ============================================

import os
import streamlit as st
import whisper
from docx import Document

# ---------- 頁面設定 ----------
st.set_page_config(page_title="語音轉文字工具", page_icon="🎙️", layout="centered")
st.title("🎙️ MP3 語音轉文字工具")
st.markdown("上傳 MP3 檔案，使用 OpenAI Whisper 自動轉錄成文字，並下載 Word 檔。")

# ---------- 側邊欄：模型選擇 ----------
with st.sidebar:
    st.header("⚙️ 設定")
    model_size = st.selectbox(
        "選擇 Whisper 模型",
        ("tiny", "base", "small", "medium"),
        index=1,
        help="模型越大越準確但越慢。免費雲端記憶體有限，建議使用 base 或 small。"
    )
    st.info("💡 首次執行會下載模型，請耐心等候。")

# ---------- 載入模型（快取，只載入一次） ----------
@st.cache_resource(show_spinner="正在載入 Whisper 模型，首次執行需下載模型檔...")
def load_model(size):
    return whisper.load_model(size)

# ---------- 上傳檔案 ----------
uploaded_file = st.file_uploader("📂 上傳你的 MP3 檔案", type=["mp3", "wav", "m4a"])

if uploaded_file is not None:
    st.audio(uploaded_file, format="audio/mp3")

    if st.button("🚀 開始轉錄", type="primary"):
        # 儲存上傳的檔案到暫存目錄
        audio_path = os.path.join("temp_audio", uploaded_file.name)
        os.makedirs("temp_audio", exist_ok=True)
        with open(audio_path, "wb") as f:
            f.write(uploaded_file.getbuffer())

        # 轉錄
        try:
            model = load_model(model_size)
            with st.spinner("正在轉錄語音，請稍候（時間取決於音檔長度與模型大小）..."):
                result = model.transcribe(audio_path, language=None)
            detected_lang = result.get("language", "未知")
            st.success(f"✅ 轉錄完成！偵測到的語言：{detected_lang}")

            # 顯示轉錄結果
            st.subheader("📝 轉錄結果")
            for segment in result["segments"]:
                start = int(segment["start"])
                end = int(segment["end"])
                st.markdown(
                    f"`[{start//60:02d}:{start%60:02d} - {end//60:02d}:{end%60:02d}]` "
                    f"{segment['text'].strip()}"
                )

            # 生成 Word 檔
            doc = Document()
            doc.add_heading("語音轉文字結果", level=1)
            doc.add_paragraph(f"音訊檔案：{uploaded_file.name}")
            doc.add_paragraph(f"偵測語言：{detected_lang}")
            doc.add_paragraph(f"使用模型：Whisper {model_size}")
            doc.add_paragraph("")
            for segment in result["segments"]:
                start = int(segment["start"])
                end = int(segment["end"])
                doc.add_paragraph(
                    f"[{start//60:02d}:{start%60:02d} - {end//60:02d}:{end%60:02d}] "
                    f"{segment['text'].strip()}"
                )

            word_filename = os.path.splitext(uploaded_file.name)[0] + "_轉錄.docx"
            doc.save(word_filename)

            # 下載 Word 檔
            with open(word_filename, "rb") as f:
                st.download_button(
                    label="⬇️ 下載 Word 檔",
                    data=f.read(),
                    file_name=word_filename,
                    mime="application/vnd.openxmlformats-officedocument.wordprocessingml.document",
                )

            # 清理暫存檔
            os.remove(audio_path)
            os.remove(word_filename)

        except Exception as e:
            st.error(f"轉錄時發生錯誤：{e}")
else:
    st.info("👆 請先上傳 MP3 檔案")
