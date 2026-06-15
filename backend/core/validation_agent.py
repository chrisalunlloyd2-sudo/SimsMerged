# [TIMESTAMP: 2026-06-11T13:00:00.000Z] [PROJECT_ID: SimsMerged-v1.4.2] [AGENT_ID: Gemini-CLI-Architect]

import os
import sys

def validate_research_paper(file_path: str):
    """
    Step 24: Validates word count and cohesion of the research paper.
    Target: 35 pages (approx 17,500 words).
    """
    if not os.path.exists(file_path):
        print(f"❌ Validation Failed: File {file_path} not found.")
        return False

    with open(file_path, "r", encoding='utf-8') as f:
        content = f.read()

    word_count = len(content.split())
    page_estimate = word_count / 500.0

    print(f"📊 [VALIDATION] Word Count: {word_count}")
    print(f"📊 [VALIDATION] Estimated Pages: {page_estimate:.2f}")

    # Cohesion Check (Chapter presence and Bibliography)
    has_bib = "## BIBLIOGRAPHY" in content
    chapter_count = content.count("### Chapter")

    print(f"📊 [VALIDATION] Chapters Detected: {chapter_count}")
    print(f"📊 [VALIDATION] Bibliography Present: {has_bib}")

    if word_count >= 17500 and has_bib and chapter_count >= 15:
        print("✅ [VALIDATION SUCCESS] Paper meets the 35-page articulate study requirement.")
        return True
    else:
        print("❌ [VALIDATION FAILED] Paper does not meet high-fidelity metrics.")
        return False

if __name__ == "__main__":
    if len(sys.argv) > 1:
        validate_research_paper(sys.argv[1])
    else:
        print("Usage: python validation_agent.py <path_to_paper>")
