import os
import time
import random
import instaloader

# ==================================================
# ⚙️ [필수 설정] 로그인 정보 입력 구역
# ==================================================
INSTA_USER = "merck081"
INSTA_PW = "ip13578041!"
# ==================================================

# 수집 타겟 계정 및 폴더 설정
TARGET_USERS = ["utility.kang", "pe_study_note", "engineering_in_one"]
SAVE_DIR = "downloaded_media"

if not os.path.exists(SAVE_DIR):
    os.makedirs(SAVE_DIR)

def run_automation():
    print("🚀 인스타그램 안전 자동 수집을 시작합니다...")
    L = instaloader.Instaloader(
        dirname_pattern=os.path.join(SAVE_DIR, "{target}"),
        download_pictures=True,
        download_videos=True,
        download_geotags=False,
        download_comments=False,
        save_metadata=False,
        user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
    )
    
    # 🔒 [로그인 시도]
    try:
        print(f"🔑 @{INSTA_USER} 계정으로 인스타그램 로그인 시도 중...")
        L.login(INSTA_USER, INSTA_PW)
        print("✅ 로그인 성공! 안전하게 수집을 시작합니다.")
    except Exception as e:
        print(f"❌ 로그인 실패 (2단계 인증 미해제 또는 비번 오류 가능성): {e}")
        print("💡 로그인 없이 비회원 상태로 수집을 강제 시도합니다.")

    # 🔄 [타겟 계정 순회 수집]
    for target in TARGET_USERS:
        # 사람처럼 보이기 위한 무작위 대기 (10초 ~ 25초 사이)
        delay = random.randint(10, 25)
        print(f"💤 인스타 보안 우회를 위해 {delay}초 동안 대기 후 탐색합니다...")
        time.sleep(delay)
        
        print(f"📦 현재 수집 중인 계정: @{target}")
        try:
            profile = instaloader.Profile.from_username(L.context, target)
            
            # 최신 게시물 3개 가져오기
            for count, post in enumerate(profile.get_posts()):
                if count >= 3:
                    break
                L.download_post(post, target=target)
                time.sleep(random.randint(3, 7)) # 게시물 다운로드 사이에도 짧은 휴식
                
            print(f"✅ @{target} 계정 수집 및 저장 완료!")
            
        except Exception as e:
            print(f"❌ @{target} 수집 중 에러 발생 (429 차단 지속 또는 비공개 계정): {e}")
            continue

if __name__ == "__main__":
    run_automation()
    print("🏁 모든 자동화 수집 프로세스가 안전하게 종료되었습니다.")
