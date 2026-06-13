# Violin Lessons — landing page (Alice Jeon)

포스터 QR이 가리킬 모바일 친화형 한 페이지. 정적 사이트(HTML 1장) → **GitHub Pages** 무료 호스팅.
연락 폼은 **Formsubmit.co**(가입·키 없는 무료 폼 백엔드)가 받아서 `jjyvn@hotmail.com` 으로 전달.

## 파일
- `index.html` — 페이지 전체(스타일·스크립트 포함, 외부 의존성은 Google Fonts뿐)

## 폼 활성화 (가입·키·대시보드 전부 없음)
폼은 이미 `https://formsubmit.co/ajax/jjyvn@hotmail.com` 으로 보내도록 설정돼 있음. 따로 넣을 키 없음.

1. **배포 후** 페이지에서 폼을 한 번 제출(테스트로 아무거나).
2. 그러면 Formsubmit이 **선생님 hotmail로 "Activate Form" 확인 메일 1통**을 보냄.
3. 선생님(또는 메일 확인 가능한 사람)이 그 메일의 **버튼 1번 클릭** → 끝. 이후 모든 문의가 선생님 받은편지함으로 직행.
   - 선생님이 평생 할 일: 이 활성화 버튼 1번 클릭. 가입·로그인·키 일절 없음.
   - 폼의 학생 `email` 칸 덕분에 선생님이 메일에 **"답장"하면 학생에게 회신**됨.

### (선택) 이메일 주소 숨기기 — 스팸봇 차단
위 활성화 메일 안에 **랜덤 별칭(alias) URL**(예: `https://formsubmit.co/a1b2c3...`)이 들어 있음.
`index.html` 의 fetch URL을 `https://formsubmit.co/ajax/jjyvn@hotmail.com` → `https://formsubmit.co/ajax/a1b2c3...` 로 바꾸면
소스코드에 선생님 이메일이 노출되지 않아 스팸 수집을 막을 수 있음.

## GitHub Pages 배포
```bash
cd ~/violin-lessons
git init && git add -A && git commit -m "Violin lessons landing page"
gh repo create alice-violin --public --source=. --push   # public 이어야 Pages 무료
gh api -X POST repos/TaehyungAlexKim/alice-violin/pages -f source[branch]=main -f source[path]=/ 2>/dev/null || true
```
또는 GitHub 웹에서: repo → Settings → Pages → Source = `main` / `/ (root)` → Save.
1~2분 뒤 `https://taehyungalexkim.github.io/alice-violin/` 에서 확인.

## QR 코드
배포된 URL 끝에 **`?ref=poster`** 를 붙여 QR 생성:
`https://taehyungalexkim.github.io/alice-violin/?ref=poster`
- 이러면 GoatCounter가 "포스터 QR로 들어온 방문"을 referrer로 구분해 보여줌(다른 경로 유입과 분리 집계).
- 포스터의 기존 QR은 이 URL을 가리키도록 교체 필요(현재 포스터 QR이 무엇을 가리키는지 확인 후).

## 방문 카운터 (GoatCounter — 비공개, 무료, 쿠키 없음)
방문자에겐 아무것도 안 보이고, 통계는 본인만 로그인해서 봅니다.
1. https://www.goatcounter.com 가입 완료 → **이 페이지는 코드 `alexkim`로 설정돼 있음.**
   - 다른 코드로 만들면 `index.html` 의 `data-goatcounter` URL을 그 코드로 바꿀 것.
2. 비공개 대시보드: `https://alexkim.goatcounter.com` (로그인해야 보임)
3. 끝. 페이지가 열릴 때마다 자동 집계됨.

### NAS homepage 대시보드에 카운터 위젯 띄우기
GoatCounter는 `https://alexkim.goatcounter.com/counter/TOTAL.json` 으로 누적 카운트를 JSON으로 줍니다(`{"count":"1,234","count_unique":"1,000"}`). homepage `customapi` 위젯으로 표시:

```yaml
# homepage services.yaml (원하는 그룹 아래에 추가)
- Violin Page:
    icon: mdi-violin
    href: https://taehyungalexkim.github.io/alice-violin/
    siteMonitor: https://taehyungalexkim.github.io/alice-violin/
    widget:
      type: customapi
      url: https://alexkim.goatcounter.com/counter/TOTAL.json
      refreshInterval: 600000   # 10분
      mappings:
        - field: count
          label: Total visits
          format: text
        - field: count_unique
          label: Unique
          format: text
```
(`count` 값이 `"1,234"` 처럼 콤마 포함 문자열이라 `format: text` 사용. 숫자만 원하면 GoatCounter 설정에서 raw 옵션 확인.)

## 커스텀 도메인(선택)
`alexkim.uk` 하위 서브도메인(예: `violin.alexkim.uk`)을 Pages에 CNAME 연결 가능.
Cloudflare DNS에 CNAME → `taehyungalexkim.github.io`, repo Settings → Pages → Custom domain 입력.

## 수정 포인트
- 본문/문구: `index.html` 의 `<section>` 안 텍스트.
- 색/폰트: `<style>` 상단 `:root` 변수(navy/gold/cream).
- 포스터 이미지 넣고 싶으면 hero 영역에 `<img>` 추가(권장: 가로 1080px 내로 압축).
