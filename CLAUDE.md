# Violin Lessons — 프로젝트 작업 환경 (violin-lessons)

비기술자(바이올린 선생님)를 위한 **모바일 랜딩 페이지 + 4×6 QR 미니 포스터**. "생활코딩" 수준 — **자체 호스팅 없이 무료/저유지보수**로 구성. 가장 단순하게 필요한 것만. (관련 가치관: nas-admin 메모리 `values-appropriate-tech`.)

> **새 세션(Claude)에게**: 이 파일이 워크스페이스 열 때 자동 로드됩니다. 아래가 출처(source of truth). 사용자에게 보여줄 안내 문서는 `README.md`, 이 파일은 어시스턴트용 컨텍스트.

## 무엇 / 누구
- 선생님: **Ja Young (Alice) Jeon** — 바이올린 1:1 레슨 (Vancouver). 공개 연락처: `jjyvn@hotmail.com` / `604 505 4908`.
- 사용자(나)가 기술 담당. 선생님은 가입·API·대시보드 일절 못/안 함 → **선생님 무관여**가 설계 1원칙.

## 라이브 / 배포
| 항목 | 값 |
|---|---|
| 라이브 | https://taehyungalexkim.github.io/alice-violin/ |
| QR 인코딩 | https://taehyungalexkim.github.io/alice-violin/?ref=poster |
| GitHub repo | `TaehyungAlexKim/alice-violin` (**PUBLIC**, 이 폴더) |
| 호스팅 | GitHub Pages (main / root). **배포 = `git push`** → 1~2분 뒤 반영 |
| 커밋 트레일러 | `Co-Authored-By: Claude Opus 4.8 (1M context) <noreply@anthropic.com>` |

⚠️ **이 repo는 PUBLIC** — 비밀값 절대 커밋 금지. (nas-admin(private)과 별개 repo, 섞지 말 것.)

## 구성 요소 (전부 무료)
- **페이지**: `index.html` 한 장 (빌드 없음. 외부 의존성 Google Fonts뿐). 모바일 친화 + 하단 플로팅 "Book a Lesson" CTA(폼 보이면 사라짐).
- **연락 폼**: **Formsubmit.co** AJAX. **활성화된 별칭** 사용 → 엔드포인트 `https://formsubmit.co/ajax/d86d81472234d48dff7c9f53055a3caa` (선생님 hotmail로 직행, 활성화 완료 2026-06-12). 학생 `email` 칸 → Reply-To 자동.
- **이메일 노출 차단**: 폼은 별칭, 보이는 메일/전화는 JS `String.fromCharCode`로 조립 → **정적 소스에 평문 연락처 0**. (수정 시 이 원칙 유지.)
- **방문 카운터**: **GoatCounter** code `alexkim`. 비공개 대시보드 https://alexkim.goatcounter.com (로그인 필요). "visitor counter" API 켜짐 → `https://alexkim.goatcounter.com/counter/TOTAL.json` = `{"count":"N","count_unique":"N"}`. 포스터 유입은 대시보드 **Referrers**에 "poster"로 집계(위젯엔 미표시 — 무인증 카운터는 referrer별 불가, API+토큰 필요해서 안 함).
- **NAS homepage 위젯**: `/Docker/homepage/config/services.yaml` **Productivity 그룹**에 "Violin Lessons" 카드(`customapi` → TOTAL.json, Total/Unique). 원본 백업 NAS에 `services.yaml.2026-06-12.bak`. ⚠️ 이 파일은 비밀 다수 → **git 금지**, NAS 내부에서만 편집. (NAS 접속 `ssh nas`.)

## 포스터 (`poster/`)
- `violin-mini-poster.png` — **4×6", 300dpi = 1200×1800**, 세로. 카페 게시판 등에 붙이는 용도(사용자가 이 사이즈 선호).
- **`build_poster.py` 가 완전 재생성** — 문구/색/레이아웃/이미지 수정은 여기서. (palette 변수 상단 `:root`격, Didot 제목 + Georgia 본문 = macOS 시스템 폰트.)
- 디자인: 크림 배경 + 딥네이비 세리프 + 골드. 세 도시 **듀오톤(네이비↔크림) 트립틱** = VANCOUVER(BC Place) · FREIBURG(뮌스터) · KOREA(경복궁). "Spaß mit Musik" 악센트.
- **제약 — 절대 준수**:
  - **흑백 잉크 없는 컬러 프린터** → 순수 검정 금지, 어두운 톤은 전부 딥네이비. 사진도 듀오톤.
  - **프린터가 가장자리 ~0.5cm over-scan(테두리없음 인쇄)** → 하단 안전여백 ~1.7cm(198px) 확보됨. 레이아웃 바꾸면 다시 확보.
- 이미지 `poster/assets/`: `vancouver.webp`·`korea.webp`(사용자 제공), `freiburg.jpg`(**CC BY 3.0, Taxiarchos228 — 공개 배포 시 저작자 표기 의무**, `poster/CREDITS.md` 참고). EXIF 방향 보정(`exif_transpose`) 적용됨(경복궁 원본이 뒤집혀 있었음).
- QR: `qr/violin-qr-poster.png`/`.svg` (error H, navy). 포스터 안 QR도 navy 듀오톤.

## 작업 규약
- **포스터/QR을 수정하면 반드시 QR을 OpenCV로 디코드 재검증** (URL 일치 확인) + 하단 안전여백 확인. 인쇄 사고 방지.
- 변경은 commit + push (배포). 큰 변경 전 사용자에게 확인.
- 사진 교체는 사용자가 파일 제공(채팅 첨부는 디스크 접근 불가 → `poster/assets/`에 저장 요청).

## 도구 — Python venv (Pillow/segno/opencv)
`/tmp/qrvenv` 에 만들어 씀. **/tmp는 재부팅 시 사라짐** → 없으면 재생성:
```bash
python3 -m venv /tmp/qrvenv && /tmp/qrvenv/bin/pip install Pillow segno opencv-python-headless numpy
```
실행: `cd ~/violin-lessons/poster && /tmp/qrvenv/bin/python build_poster.py`
(시스템 python은 PEP668로 직접 pip 안 됨 → venv 필수.)

## 상태 / 다음
- ✅ 페이지·폼(활성화)·카운터·homepage 위젯·미니 포스터·QR — 전부 완료/검증.
- 🔜 **다음 작업: 포스터 일부 수정**일 가능성 높음.
- 폴더: `index.html`, `README.md`(사용자 안내), `CLAUDE.md`(이 파일), `poster/`, `qr/`.
