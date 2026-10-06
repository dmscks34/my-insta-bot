import os
import instaloader

# 1. 수집 타겟 계정 설정
TARGET_USERS = ["utility.kang", "pe_study_note", "engineering_in_one"]

# 2. 데이터 저장 폴더 설정
SAVE_DIR = "downloaded_media"
if not os.path.exists(SAVE_DIR):
    os.makedirs(SAVE_DIR)

def run_automation():
    print("🚀 인스타그램 자동 수집을 시작합니다...")
    L = instaloader.Instaloader(
        dirname_pattern=os.path.join(SAVE_DIR, "{target}"), # 계정별 폴더 자동 분류
        download_pictures=True,
        download_videos=True,
        download_geotags=False,
        download_comments=False,
        save_metadata=False
    )
    
    for target in TARGET_USERS:
        print(f"📦 계정 수집 중: @{target}")
        try:
            profile = instaloader.Profile.from_username(L.context, target)
            
            # 각 계정별 최신 게시물 3개씩 가져오기
            for count, post in enumerate(profile.get_posts()):
                if count >= 3:
                    break
                L.download_post(post, target=target)
                
            print(f"✅ @{target} 수집 완료")
            
        except Exception as e:
            # 인스타 차단이나 에러가 발생해도 멈추지 않고 다음 계정으로 넘어가도록 안전망 구축
            print(f"❌ @{target} 수집 중 에러 발생: {e}")
            continue

if __name__ == "__main__":
    run_automation()
    print("🏁 모든 자동화 작업이 종료되었습니다.")
