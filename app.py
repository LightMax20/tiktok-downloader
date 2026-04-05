import streamlit as st
import yt_dlp
import os

st.set_page_config(page_title="TikTok Downloader", page_icon="🎬")

st.title("🎬 TikTok Video Downloader")
st.write("Paste a TikTok link and download the video")

url = st.text_input("Enter TikTok URL")

if st.button("Download"):
    if not url:
        st.error("Please enter a URL")
    else:
        st.info("Downloading...")

        ydl_opts = {
            'format': 'mp4/best',
            'outtmpl': '%(title)s.%(ext)s',
            'noplaylist': True,
        }

        try:
            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                info = ydl.extract_info(url, download=True)
                filename = ydl.prepare_filename(info)

            st.success("Download complete!")

            with open(filename, "rb") as f:
                st.download_button(
                    label="📥 Download Video",
                    data=f,
                    file_name=os.path.basename(filename),
                    mime="video/mp4"
                )

        except Exception as e:
            st.error(f"Error: {str(e)}")
