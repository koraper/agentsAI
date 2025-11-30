#!/usr/bin/env node

const Anthropic = require("@anthropic-ai/sdk");
const fs = require("fs").promises;
const path = require("path");

const anthropic = new Anthropic({
  apiKey: process.env.ANTHROPIC_API_KEY,
});

const SYSTEM_PROMPT = `당신은 전문 기술 번역가입니다. 마크다운 파일을 한국어로 완전히 번역합니다.

번역 규칙:
1. **모든 텍스트를 한국어로 번역**:
   - 모든 설명문
   - 모든 섹션 헤더
   - 모든 리스트 항목
   - 모든 문단과 설명

2. **보존 (번역하지 않음)**:
   - 코드 블록과 코드 예제
   - URL과 링크
   - API, SDK, REST, GraphQL 같은 기술 용어
   - 변수명과 식별자
   - 고유명사 (도구명, 라이브러리명: Stripe, PayPal, AWS 등)
   - YAML 필드명 (name, model, description 키는 영문 유지)
   - Markdown 구조

3. **번역 스타일**:
   - 자연스럽고 전문적인 한국어 사용
   - 원문의 기술적 톤 유지
   - 명확하고 읽기 쉬운 문장

4. **출력**: 완전히 번역된 마크다운만 반환하세요. 추가 설명 없이.`;

async function translateFile(content, filePath) {
  try {
    const message = await anthropic.messages.create({
      model: "claude-sonnet-4-20250514",
      max_tokens: 16000,
      temperature: 0,
      system: SYSTEM_PROMPT,
      messages: [
        {
          role: "user",
          content: `다음 마크다운 파일을 완전히 한국어로 번역하세요.\n\n파일 경로: ${filePath}\n\n내용:\n${content}\n\n완전히 번역된 한국어 마크다운을 반환하세요:`
        }
      ]
    });

    let translated = message.content[0].text.trim();

    // Remove markdown code fence if added
    if (translated.startsWith("```markdown")) {
      translated = translated.slice(11);
    }
    if (translated.startsWith("```")) {
      translated = translated.slice(3);
    }
    if (translated.endsWith("```")) {
      translated = translated.slice(0, -3);
    }

    return translated.trim();
  } catch (error) {
    console.error(`  ❌ Translation error: ${error.message}`);
    return content;
  }
}

async function processFile(sourcePath, targetPath) {
  try {
    // Read source file
    const content = await fs.readFile(sourcePath, "utf-8");

    // Check if already translated (basic heuristic)
    try {
      const existing = await fs.readFile(targetPath, "utf-8");
      const englishWords = (existing.match(/\b[a-zA-Z]{4,}\b/g) || []).length;
      const koreanChars = (existing.match(/[가-힣]/g) || []).length;

      if (koreanChars > englishWords * 2) {
        console.log(`  ✓ Already translated`);
        return true;
      }
    } catch {
      // File doesn't exist, continue
    }

    // Translate
    console.log(`  🔄 Translating...`);
    const translated = await translateFile(content, sourcePath);

    // Ensure target directory exists
    await fs.mkdir(path.dirname(targetPath), { recursive: true });

    // Save translated file
    await fs.writeFile(targetPath, translated, "utf-8");
    console.log(`  ✅ Saved`);
    return true;
  } catch (error) {
    console.error(`  ❌ Error: ${error.message}`);
    return false;
  }
}

async function getAllMarkdownFiles(dir) {
  const files = [];

  async function walk(currentPath) {
    const entries = await fs.readdir(currentPath, { withFileTypes: true });

    for (const entry of entries) {
      const fullPath = path.join(currentPath, entry.name);

      if (entry.isDirectory()) {
        await walk(fullPath);
      } else if (entry.isFile() && entry.name.endsWith('.md')) {
        files.push(fullPath);
      }
    }
  }

  await walk(dir);
  return files.sort();
}

async function main() {
  const sourceDir = "/Users/kevinjang0301/workprivate/agentsAI/plugins";
  const targetDir = "/Users/kevinjang0301/workprivate/agentsAI/pluginsK";

  console.log("🚀 Starting complete Korean translation");
  console.log(`📁 Source: ${sourceDir}`);
  console.log(`📁 Target: ${targetDir}`);
  console.log("=" .repeat(80));

  const files = await getAllMarkdownFiles(sourceDir);
  const total = files.length;

  console.log(`\n📝 Found ${total} markdown files\n`);

  let successCount = 0;

  for (let i = 0; i < total; i++) {
    const sourcePath = files[i];
    const relPath = path.relative(sourceDir, sourcePath);
    const targetPath = path.join(targetDir, relPath);

    console.log(`\n[${i + 1}/${total}] ${relPath}`);

    if (await processFile(sourcePath, targetPath)) {
      successCount++;
    }

    // Rate limiting - wait 1 second between requests
    if (i < total - 1) {
      await new Promise(resolve => setTimeout(resolve, 1000));
    }
  }

  console.log("\n" + "=".repeat(80));
  console.log(`✅ Translation complete: ${successCount}/${total} files`);
  if (successCount < total) {
    console.log(`⚠️  Failed: ${total - successCount} files`);
  }
}

main().catch(console.error);
