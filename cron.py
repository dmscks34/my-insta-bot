import instaloader
import os
import time

# --- [필수 설정] 내 인스타 로그인 정보 입력 ---
# ⚠️ 주의: 본계정 대신 인스타 부계정을 하나 만들어서 입력하는 것을 강력히 추천합니다!
INSTA_USER = "merck081"
INSTA_PASS = "ip13578041!"

# --- [필수 설정] 감시할 타겟 인스타 ID 입력 ---
TARGET_USER = "utility.kang" 

# 저장할 폴더 설정
SAVE_DIR = "downloaded_media"
if not os.path.exists(SAVE_DIR):
    os.makedirs(SAVE_DIR)

print(f"[{time.strftime('%Y-%m-%d %H:%M:%S')}] 인스타그램 자동 수집기를 시작합니다...")

try:
    # 인스타 로더 설정
    L = instaloader.Instaloader(
        dirname_pattern=os.path.join(SAVE_DIR, TARGET_USER),
        download_pictures=True,
        download_videos=True,
        download_geotags=False,
        download_comments=False,
        save_metadata=False
    )
    
    # 로그인 시도
    print("인스타그램 로그인 중...")
    L.login(INSTA_USER, INSTA_PASS)
    print("로그인 성공!")
    
    # 상대방 프로필 가져오기
    profile = instaloader.Profile.from_username(L.context, TARGET_USER)
    
    # 최신 게시물 5개만 확인하며 다운로드 (이미 다운로드된 파일은 프로그램이 알아서 건너뜁니다)
    print(f"@{TARGET_USER} 계정의 최신 게시물을 확인합니다...")
    for count, post in enumerate(profile.get_posts()):
        if count >= 5: 
            break
        L.download_post(post, target=TARGET_USER)
        
    print("🎉 최신 게시물 수집 및 업데이트 완료!")

except Exception as e:
    print(f"❌ 에러 발생: {e}")
