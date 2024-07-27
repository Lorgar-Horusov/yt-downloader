import streamlit as st
from pytubefix import YouTube
import tempfile
import os
import re

app_name = 'YT Downloader'


def main():
    st.header(app_name)
    col1, col2 = st.columns(2)
    with col1:
        url = st.text_input(label='YouTube URL', placeholder='https://youtu.be/qR7bhXNtwRU', value=None)
    with col2:
        if url:
            try:
                yt = YouTube(url)
                st.subheader(yt.title)
                st.video(data=url, autoplay=True, muted=True)
                download = st.button('Download')
                if download:
                    tmp_file = tempfile.NamedTemporaryFile(delete=False, suffix='.mp4')
                    yt.streams.get_highest_resolution().download(output_path=os.path.dirname(tmp_file.name),
                                                                 filename=os.path.basename(tmp_file.name))
                    tmp_file_path = tmp_file.name
                    tmp_file.close()

                    st.success('Download successful')
                    safe_title = re.sub(r'[^a-zA-Z0-9_\-]', '_', yt.title)
                    with open(tmp_file_path, 'rb') as file:
                        btn = st.download_button(
                            label='Save',
                            data=file,
                            file_name=f'{safe_title}.mp4',
                        )
                    if os.path.exists(tmp_file_path):
                        os.remove(tmp_file_path)
            except Exception as e:
                st.error('URL error, please check the URL and try again')
                print(e)


if __name__ == '__main__':
    main()
