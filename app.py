import streamlit as st
import instaloader
import os

# --- 1. 보안: 비밀번호 설정 ---
# 내 사이트에 접속할 때 사용할 비밀번호입니다. (원하는 대로 바꾸셔도 됩니다)
CORRECT_PASSWORD = "mysecret1234" 

# 세션 상태 초기화 (로그인 여부 기억)
if "logged_in" not in st.session_state:
    st.session_state.logged_in = False

# 로그인 화면 구현
if not st.session_state.logged_in:
    st.title("🔒 나만의 인스타 보관함 접속")
    password_input = st.text_input("비밀번호를 입력하세요:", type="password")
    if st.button("접속하기"):
        if password_input == CORRECT_PASSWORD:
            st.session_state.logged_in = True
            st.rerun()
        else:
            st.error("비밀번호가 틀렸습니다.")
    st.stop() # 로그인 안 되면 아래 코드는 실행 안 됨

# --- 2. 로그인 성공 시 메인 웹사이트 화면 ---
st.title("📱 인스타 자동 수집 및 분류 대시보드")

# 파일 보관용 폴더 자동 생성
SAVE_DIR = "downloaded_media"
if not os.path.exists(SAVE_DIR):
    os.makedirs(SAVE_DIR)

# 사이드바 - 인스타 수집기 기능
st.sidebar.header("📥 새 게시물 가져오기")
target_profile = st.sidebar.text_input("추적할 인스타 ID 입력 (예: 보셨던 릴스 계정 ID)")

if st.sidebar.button("최신 게시물 긁어오기"):
    if target_profile:
        with st.spinner("인스타에서 데이터를 가져오는 중..."):
            try:
                L = instaloader.Instaloader(
                    dirname_pattern=os.path.join(SAVE_DIR, target_profile), # 계정별 폴더 분류
                    download_pictures=True,
                    download_videos=True,
                    download_geotags=False,
                    download_comments=False,
                    save_metadata=False
                )
                # 실제로 수집하는 명령 (최신 글 위주로 가져옵니다)
                profile = instaloader.Profile.from_username(L.context, target_profile)
                
                # 테스트용으로 최신 게시물 3개만 먼저 긁어오기
                for count, post in enumerate(profile.get_posts()):
                    if count >= 3: 
                        break
                    L.download_post(post, target=target_profile)
                
                st.sidebar.success(f"@{target_profile} 수집 완료!")
            except Exception as e:
                st.sidebar.error(f"에러 발생: {e}")
    else:
        st.sidebar.warning("계정 ID를 입력해주세요.")

# --- 3. 데이터 분류 및 시청 화면 ---
st.header("📂 수집된 데이터 분류 보기")

# 수집된 계정 폴더 목록 가져오기
if os.path.exists(SAVE_DIR):
    accounts = [f for f in os.listdir(SAVE_DIR) if os.path.isdir(os.path.join(SAVE_DIR, f))]
    
    if accounts:
        # 셀렉트박스로 계정별로 데이터 분류해서 보기
        selected_account = st.selectbox("보고 싶은 계정을 선택하세요:", accounts)
        
        account_path = os.path.join(SAVE_DIR, selected_account)
        files = os.listdir(account_path)
        
        # 사진과 동영상 분류해서 보여주기
        for file in files:
            file_path = os.path.join(account_path, file)
            
            # 동영상 파일 재생 (.mp4)
            if file.endswith(".mp4"):
                st.video(file_path)
            # 사진 파일 보여주기 (.jpg, .png)
            elif file.endswith((".jpg", ".png")):
                st.image(file_path, use_container_width=True)
    else:
        st.info("아직 수집된 데이터가 없습니다. 왼쪽에서 인스타 ID를 입력해 보세요.")
