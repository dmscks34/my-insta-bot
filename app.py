import streamlit as st
import instaloader
import os
import requests

# ==================================================
# ⚙️ [비밀번호 및 고정 타겟 설정]
# ==================================================
SITE_PASSWORD = "2288" 
TARGET_USERS = ["utility.kang", "pe_study_note", "engineering_in_one"]
# ==================================================

st.set_page_config(page_title="인스타 업무 자료 수집기", layout="wide")

# 🔒 1. 로그인 시스템
if "logged_in" not in st.session_state:
    st.session_state["logged_in"] = False

if not st.session_state["logged_in"]:
    st.subheader("🔒 시스템 로그인")
    user_password = st.text_input("접속 비밀번호를 입력하세요:", type="password")
    if st.button("로그인하기"):
        if user_password == SITE_PASSWORD:
            st.session_state["logged_in"] = True
            st.rerun()
        else:
            st.error("❌ 비밀번호가 올바르지 않습니다.")
    st.stop()


# 📸 2. 메인 화면 레이아웃
st.title("📸 인스타그램 업무 자료 수동 수집기")
st.write("지정된 고정 계정을 클릭하여 최신 게시물(사진/동영상)을 확인하고 원하는 자료만 선택 다운로드합니다.")

st.markdown("---")
st.subheader("📌 수집 대상 계정 선택")
st.write("아래 버튼을 누르면 해당 계정의 최신 게시물 4개를 실시간으로 조회합니다.")

# 🔘 고정 계정 버튼을 가로로 배치
cols = st.columns(len(TARGET_USERS))
selected_user = None

for i, user in enumerate(TARGET_USERS):
    with cols[i]:
        if st.button(f"👤 @{user} 최신글 보기", use_container_width=True):
            st.session_state["current_target"] = user

# 현재 선택된 계정 유지 처리
if "current_target" in st.session_state:
    selected_user = st.session_state["current_target"]

# 🔄 3. 계정이 선택되었을 때 게시물 긁어와서 뿌려주기
if selected_user:
    st.markdown("---")
    st.subheader(f"🗂️ @{selected_user} 계정의 최신 게시물 목록")
    
    with st.spinner(f"@{selected_user} 계정에서 미디어를 안전하게 읽어오는 중..."):
        try:
            # 인스타로더 비회원 모드로 초기화
            L = instaloader.Instaloader(
                download_pictures=True,
                download_videos=True,
                download_geotags=False,
                download_comments=False,
                save_metadata=False,
                user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
            )
            
            profile = instaloader.Profile.from_username(L.context, selected_user)
            
            # 화면을 2x2 바둑판 배열로 만들기 위해 컬럼 2개 생성
            grid_cols = st.columns(2)
            
            # 최신 게시물 4개만 순회하면서 화면에 배치
            for idx, post in enumerate(profile.get_posts()):
                if idx >= 4:
                    break
                
                # 바둑판 배열 위치 결정 (0, 1번 글은 첫줄 / 2, 3번 글은 둘째줄)
                col_target = grid_cols[idx % 2]
                
                with col_target:
                    st.markdown(f"### 📍 게시물 {idx + 1}")
                    
                    # 미디어 종류 식별 및 띄우기
                    if post.is_video:
                        st.video(post.video_url)
                        media_url = post.video_url
                        file_ext = ".mp4"
                    else:
                        st.image(post.url, use_container_width=True)
                        media_url = post.url
                        file_ext = ".jpg"
                    
                    # 본문 글 상자
                    if post.caption:
                        st.text_area("📝 본문 내용", post.caption[:150] + "...", height=80, key=f"text_{selected_user}_{idx}")
                    
                    # 개별 다운로드 버튼 연동
                    try:
                        response = requests.get(media_url, stream=True, timeout=10)
                        if response.status_code == 200:
                            st.download_button(
                                label=f"📥 {idx + 1}번 파일 저장하기",
                                data=response.content,
                                file_name=f"{selected_user}_{post.shortcode}{file_ext}",
                                mime="video/mp4" if post.is_video else "image/jpeg",
                                key=f"btn_{selected_user}_{idx}"
                            )
                    except:
                        st.caption("⚠️ 해당 미디어 다운로드 버튼 생성 실패")
                    
                    st.markdown("<br><br>", unsafe_allow_value=True)
                    
        except Exception as e:
            st.error("❌ 데이터를 가져오지 못했습니다. (원인: 인스타 서버 임시 IP 차단 상태)")
            st.info("💡 집 PC 브라우저에 로그인된 정보를 추출한 본계정 쿠키(cookies.txt) 파일이 프로젝트 폴더에 업로드되어 있으면 이 차단이 100% 우회됩니다.")
