#!/bin/bash

# 한글 완전 번역 배치 스크립트
# pluginsK 폴더의 모든 md 파일을 100% 한글로 번역합니다

BASE_DIR="/Users/kevinjang0301/workprivate/agentsAI/pluginsK"
TOTAL_COUNT=0
TRANSLATED_COUNT=0
FAILED_COUNT=0

# Get list of files sorted by English word count
mapfile -t FILES < <(
  find "$BASE_DIR" -name "*.md" -type f -exec grep -o '[A-Za-z][A-Za-z_]*' {} + | wc -l | sort -rn | \
  find "$BASE_DIR" -name "*.md" -type f | while read file; do
    english_count=$(grep -o '[A-Za-z][A-Za-z_]*' "$file" | wc -l)
    echo "$english_count:$file"
  done | sort -rn | cut -d: -f2
)

# Process each file
for FILE in "${FILES[@]}"; do
  TOTAL_COUNT=$((TOTAL_COUNT + 1))
  REL_PATH="${FILE#$BASE_DIR/}"

  echo "[$TOTAL_COUNT] 번역 중: $REL_PATH"

  # Create temporary directory
  TEMP_FILE="/tmp/translate_$(date +%s)_$RANDOM.md"

  # Check if file has significant English content
  english_words=$(grep -o '[A-Za-z][A-Za-z_]*' "$FILE" | wc -l)

  if [ "$english_words" -lt 20 ]; then
    echo "  ✓ 이미 한글 전환됨 (영어 단어 $english_words개)"
    TRANSLATED_COUNT=$((TRANSLATED_COUNT + 1))
    continue
  fi

  # Extract the content
  FILE_CONTENT=$(cat "$FILE")

  # Use Claude CLI to translate
  # The translation prompt is embedded in the command
  TRANSLATED_CONTENT=$(cat << 'PROMPT' | sed "s|FILE_CONTENT_PLACEHOLDER|$FILE_CONTENT|g" | timeout 30 bash -c 'cat > /tmp/trans_prompt.txt && echo "파일 내용을 한글로 번역해줘:"' > /dev/null 2>&1
이 마크다운 문서를 완전히 한글로 번역해줘. 다음 규칙을 따라:

1. YAML frontmatter의 필드명(name, description, model)은 그대로 두고 description 값만 한글로 번역
2. ``` 안의 코드블록은 번역하지 말기
3. 기술 용어(REST, GraphQL, API, HTTP, SQL, JSON 등)는 영어로 유지
4. 프로그래밍 언어명(Python, JavaScript, Java, Go, Rust 등)은 영어로 유지
5. 브랜드/서비스명(AWS, Azure, Google Cloud, Stripe, PayPal, Docker, Kubernetes 등)은 영어로 유지
6. 링크와 이미지 경로는 그대로 두기
7. 마크다운 포맷(제목, 리스트, 코드 블록 등)은 유지
8. 모든 설명과 일반 텍스트는 한글로 번역
9. 마크다운 특수문자(-, *, [], () 등)는 보존

번역된 파일만 출력(주석이나 추가 설명 없이):

FILE_CONTENT_PLACEHOLDER
PROMPT
)

  if [ -n "$TRANSLATED_CONTENT" ] && [ ${#TRANSLATED_CONTENT} -gt 100 ]; then
    # Save translated content
    echo "$TRANSLATED_CONTENT" > "$FILE"
    TRANSLATED_COUNT=$((TRANSLATED_COUNT + 1))
    echo "  ✓ 완료"
  else
    FAILED_COUNT=$((FAILED_COUNT + 1))
    echo "  ✗ 번역 실패 - 수동 처리 필요"
  fi

  # Rate limiting - avoid too many requests
  sleep 0.5
done

echo ""
echo "================================"
echo "배치 처리 완료!"
echo "처리됨: $TRANSLATED_COUNT / $TOTAL_COUNT"
echo "실패: $FAILED_COUNT"
echo "================================"
