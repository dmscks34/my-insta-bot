import instaloader
import os
import time

# --- [필수 설정] 내 인스타 로그인 정보 입력 ---
# ⚠️ 주의: 본계정 대신 인스타 부계정을 하나 만들어서 입력하는 것을 강력히 추천합니다!
INSTA_USER = "merck081"
INSTA_PASS = "ip13578041!"

# --- [필수 설정] 감시할 타겟 인스타 ID 입력 ---
TARGET_USER = ["utility.kang", "pe_study_note", "engineering_in_one]

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
   # 여러 명의 타겟을 순서대로 수집합니다
for target in TARGET_USERS:
    try:
        print(f"@{target} 계정의 최신 게시물을 확인합니다...")
        profile = instaloader.Profile.from_username(L.context, target)

        # 각 계정당 최신 게시물 5개씩 다운로드
        for count, post in enumerate(profile.get_posts()):
            if count >= 5: 
                break
            L.download_post(post, target=target)

        # 인스타 서버 차단을 피하기 위해 계정 사이에 5초씩 쉬어줍니다
        time.sleep(5) 
    except Exception as target_error:
        print(f"❌ @{target} 수집 중 에러 발생: {target_error}")
        continue
