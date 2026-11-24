# 🎙️ MP3 語音轉文字工具（Whisper + Streamlit）

上傳 MP3 音檔，使用 OpenAI Whisper 自動轉錄成文字，並可下載為 Word 檔。

## 功能
- 上傳 MP3 / WAV / M4A 音檔
- 自動偵測語言（支援中文、粵語、英文等多種語言）
- 顯示帶時間戳的逐段轉錄結果
- 一鍵下載 Word (.docx) 檔

## 本機執行
```bash
pip install -r requirements.txt
streamlit run app.py
```

## 部署到 Streamlit Cloud
1. 將本專案推送到 GitHub
2. 前往 [share.streamlit.io](https://share.streamlit.io)
3. 點選「New app」，選擇你的 GitHub 儲存庫
4. 主程式檔案設為 `app.py`，點「Deploy」即可
