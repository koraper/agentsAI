#!/bin/bash

# 한글 완전 번역 스크립트
# pluginsK 폴더의 모든 md 파일을 100% 한글로 번역합니다

BASE_DIR="/Users/kevinjang0301/workprivate/agentsAI/pluginsK"
TEMP_DIR="/tmp/translation_work"
TRANSLATED_COUNT=0
TOTAL_COUNT=0

mkdir -p "$TEMP_DIR"

# 모든 md 파일 처리
find "$BASE_DIR" -name "*.md" -type f | while read FILE; do
    TOTAL_COUNT=$((TOTAL_COUNT + 1))
    REL_PATH="${FILE#$BASE_DIR/}"

    echo "번역 중: [$TOTAL_COUNT] $REL_PATH"

    # 파일 내용을 temp 파일에 저장
    TEMP_INPUT="$TEMP_DIR/input_$RANDOM.txt"
    cat "$FILE" > "$TEMP_INPUT"

    # Claude CLI를 사용해서 번역
    # 프롬프트: 이 마크다운 파일을 완전히 한글로 번역해줘. 코드 블록, 링크, 기술 용어(REST, GraphQL, API 등)와 브랜드명(Stripe, PayPal 등)은 그대로 둬.
    TEMP_OUTPUT="$TEMP_DIR/output_$RANDOM.txt"

    cat "$TEMP_INPUT" | claude -m claude-opus "이 마크다운 문서를 완전히 한글로 번역해줘. 다음 규칙을 따라:
1. YAML frontmatter의 필드명(name, description, model)은 그대로 두고 값만 한글로 번역
2. \`\`\` 안의 코드블록은 번역하지 말기
3. 기술 용어(REST, GraphQL, API, HTTP, SQL, JSON 등)는 영어로 유지
4. 프로그래밍 언어명(Python, JavaScript, Java 등)은 영어로 유지
5. 브랜드/서비스명(AWS, Azure, Stripe, PayPal, Docker, Kubernetes 등)은 영어로 유지
6. 링크와 이미지 경로는 그대로 두기
7. 마크다운 포맷(제목, 리스트, 코드 블록 등)은 유지
8. 마크다운 특수문자(-, *, [], () 등)는 보존

번역된 파일만 출력(주석이나 추가 설명 없이):" > "$TEMP_OUTPUT" 2>/dev/null

    if [ -s "$TEMP_OUTPUT" ]; then
        # 번역 결과를 원본 파일에 저장
        cat "$TEMP_OUTPUT" > "$FILE"
        TRANSLATED_COUNT=$((TRANSLATED_COUNT + 1))
        echo "✓ 완료"
    else
        echo "✗ 번역 실패"
    fi

    # Temp 파일 정리
    rm -f "$TEMP_INPUT" "$TEMP_OUTPUT"
done

echo ""
echo "================================"
echo "번역 완료!"
echo "처리된 파일: $TRANSLATED_COUNT / $TOTAL_COUNT"
echo "================================"