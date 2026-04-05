import streamlit as st
import yt_dlp
import os

st.set_page_config(page_title="TikTok Downloader Pro", page_icon="🎬", layout="centered")

# --- Styling ---
st.markdown("""
<style>
.stButton>button {
    width: 100%;
    border-radius: 10px;
    height: 3em;
    font-size: 16px;
}
</style>
""", unsafe_allow_html=True)

# --- Header ---
st.title("🎬 TikTok Downloader Pro")
st.caption("Fast • Clean • No Watermark (when possible)")

# --- Input ---
urls_input = st.text_area(
    "📌 Paste TikTok URLs (one per line)",
    placeholder="https://www.tiktok.com/@user/video/...\nhttps://www.tiktok.com/@user/video/..."
)

download_btn = st.button("⬇️ Download Videos")

# --- Function to get info ---
def get_video_info(url):
    ydl_opts = {'quiet': True}
    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        return ydl.extract_info(url, download=False)

# --- Download logic ---
if download_btn:
    urls = [u.strip() for u in urls_input.split("\n") if u.strip()]

    if not urls:
        st.error("❌ Please enter at least one URL")
    else:
        for url in urls:
            st.divider()
            st.write(f"🔗 {url}")

            try:
                info = get_video_info(url)

                # --- Show preview ---
                st.image(info.get("thumbnail"), width=250)
                st.write(f"**Title:** {info.get('title')}")
                st.write(f"⏱ Duration: {info.get('duration')} sec")

                # --- Download ---
                with st.spinner("Downloading..."):
                    ydl_opts = {
                        'format': 'mp4/best',
                        'outtmpl': '%(title)s.%(ext)s',
                        'noplaylist': True,
                    }

                    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                        ydl.download([url])

                    filename = f"{info['title']}.mp4"

                st.success("✅ Downloaded!")

                # --- Download button ---
                if os.path.exists(filename):
                    with open(filename, "rb") as f:
                        st.download_button(
                            label="📥 Download Video",
                            data=f,
                            file_name=filename,
                            mime="video/mp4"
                        )

            except Exception as e:
                st.error(f"❌ Failed: {str(e)}")
