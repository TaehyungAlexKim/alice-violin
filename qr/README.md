# QR codes

- `violin-qr-poster.png` / `.svg` — encodes **https://taehyungalexkim.github.io/alice-violin/?ref=poster**
  - `?ref=poster` 로 GoatCounter에서 포스터 유입을 따로 집계.
  - PNG: 인쇄/화면용(scale 14, 여백 4). SVG: 무한 확대 가능(대형 인쇄용).
  - error correction = H(최대), version 6, 49×49 모듈. OpenCV로 디코드 검증 완료.

## 다시 만들려면
```bash
python3 -m venv /tmp/qrvenv && /tmp/qrvenv/bin/pip install segno
/tmp/qrvenv/bin/python -c "import segno; segno.make('https://taehyungalexkim.github.io/alice-violin/?ref=poster', error='h').save('violin-qr-poster.png', scale=14, border=4)"
```
URL이 바뀌면(예: 커스텀 도메인 violin.alexkim.uk) 위 문자열만 교체해 재생성.
