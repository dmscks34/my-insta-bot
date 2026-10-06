import streamlit as st
import instaloader
import os
import re
import requests

# 파일 저장 폴더 설정 (테스트용)
DOWNLOAD_DIR = "manual_downloads"
if not os.path.exists(DOWNLOAD_DIR):
    os.makedirs(DOWNLOAD_DIR)

st.set_page_config(page_title="인스타 업무 자료 수집기", layout="wide")

st.title("📸 인스타그램 사진/동영상 수동 수집기")
st.write("회사 보안을 우회하기 위해 링크를 통해 원하는 미디어만 안전하게 추출합니다.")

# 🔗 1. 인스타 주소 입력창
insta_url = st.text_input(
    "수집할 인스타그램 게시물(피드/릴스) 주소를 입력하세요:",
    placeholder="https://instagram.com... 또는 https://instagram.com..."
)

# 인스타 주소에서 숏코드(Shortcode) 추출하는 함수
def extract_shortcode(url):
    match = re.search(r'/(p|reel|reels)/([^/?#&]+)', url)
    if match:
        return match.group(2)
    return None

# 🚀 2. 추출하기 버튼 클릭 시 작동
if st.button("🔍 미디어 추출 및 미리보기"):
    if insta_url:
        shortcode = extract_shortcode(insta_url)
        
        if shortcode:
            with st.spinner("인스타그램 서버에서 미디어를 안전하게 읽어오는 중..."):
                try:
                    # 인스타로더 초기화 (로그인 없이 브라우저인 척 접근)
                    L = instaloader.Instaloader(
                        download_pictures=True,
                        download_videos=True,
                        download_geotags=False,
                        download_comments=False,
                        save_metadata=False,
                        user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
                    )
                    
                    # 숏코드로 게시물 정보 가져오기
                    post = instaloader.Post.from_shortcode(L.context, shortcode)
                    
                    st.success("✅ 미디어를 성공적으로 찾아왔습니다!")
                    
                    # 화면 좌우 분할 (왼쪽: 미리보기, 오른쪽: 다운로드 버튼)
                    col1, col2 = st.columns([2, 1])
                    
                    with col1:
                        st.subheader("🖼️ 미디어 미리보기")
                        # 1. 동영상인 경우
                        if post.is_video:
                            st.video(post.video_url)
                            media_url = post.video_url
                            file_ext = ".mp4"
                        # 2. 사진인 경우
                        else:
                            st.image(post.url, use_container_width=True)
                            media_url = post.url
                            file_ext = ".jpg"
                            
                        # 본문 글 요약 표시
                        if post.caption:
                            st.info(f"📝 **게시물 본문 내용:**\n\n{post.caption[:200]}...")
                    
                    with col2:
                        st.subheader("💾 파일 내 컴퓨터 저장")
                        
                        # 파일 다운로드 처리
                        response = requests.get(media_url, stream=True)
                        if response.status_code == 200:
                            file_data = response.content
                            file_name = f"insta_{shortcode}{file_ext}"
                            
                            # Streamlit 자체 다운로드 버튼 생성 (회사 PC에서도 작동함)
                            st.download_button(
                                label="📥 사진/동영상 파일 다운로드",
                                data=file_data,
                                file_name=file_name,
                                mime="video/mp4" if post.is_video else "image/jpeg"
                            )
                            st.write(f"파일명: `{file_name}`")
                            
                except Exception as e:
                    st.error(f"❌ 데이터를 가져오지 못했습니다. (원인: 오픈되지 않은 비공개 계정이거나 인스타 IP 일시 차단)")
                    st.info("💡 계속 실패할 경우, 앞서 논의한 본계정 쿠키(cookies.txt)를 연동하면 100% 해결됩니다.")
        else:
            st.error("올바른 인스타그램 주소 형식이 아닙니다. 주소를 다시 확인해 주세요.")
    else:
        st.warning("인스타 링크 주소를 먼저 입력해 주세요.")
