from pathlib import Path
import re

path = Path("index.html")
s = path.read_text(encoding="utf-8")

if 'id="project-shrimp-kit"' in s:
    print("Shrimp kit section already exists; no duplicate inserted.")
    raise SystemExit(0)

# Add the project after project 4 in all matching business submenus.
nav_pat = re.compile(r'(<li>\s*<a\s+href=["\']#project-4["\'][^>]*>\s*④\s*컨테이너\s*모듈러\s*</a>\s*</li>)')
nav_item = '\n<li><a href="#project-shrimp-kit">⑤ 새우 소금구이 키트</a></li>'
s, nav_count = nav_pat.subn(lambda m: m.group(1) + nav_item, s)
if nav_count == 0:
    raise SystemExit("Could not find project-4 submenu item; aborting without writing.")

# Renumber Future Business from 5 to 6 where linked.
s = re.sub(
    r'(<a\b[^>]*href=["\']#future-business["\'][^>]*>)\s*⑤\s*향후\s*준비사업\s*(</a>)',
    r'\1⑥ 향후 준비사업\2',
    s,
)

# Update the Korean four-business heading if present.
s = s.replace("주요 4대 사업", "주요 5대 사업")

# Insert a full business section immediately before Future Business.
future = re.search(r'<(?:section|div)\b[^>]*\bid=["\']future-business["\'][^>]*>', s, flags=re.I)
if not future:
    raise SystemExit("Could not find future-business section; aborting without writing.")

shrimp_section = '''
<section class="section alt" id="project-shrimp-kit">
  <div class="wrap">
    <div class="label">MAJOR BUSINESS · FOOD IP / HMR</div>
    <h2>새우 소금구이 키트</h2>
    <p class="sectionIntro">포장용기가 곧 조리용기가 되는 새우·소금·버터소스 일체형 수산물 간편조리 키트입니다. 가정·캠핑·HMR·유통 PB 시장으로 확장할 수 있도록 제품 구조와 사업모델을 함께 설계합니다.</p>
    <div class="ventures">
      <div class="venture">
        <div class="type">PRODUCT / IP BUSINESS MODEL</div>
        <h3>열고, 올리고, 바로 조리하는<br/>새우 소금구이 경험</h3>
        <p>별도 조리도구와 복잡한 준비를 줄이고, 새우와 소금구이 조리 구조를 하나의 패키지에 통합했습니다. 중앙 보조용기에는 버터소스 등 부재료를 구성할 수 있어 새우 몸통과 머리 조리를 하나의 키트 경험으로 연결할 수 있습니다.</p>
        <div class="pillrow">
          <span class="pill">SEAFOOD HMR</span><span class="pill">COOK-IN-PACK</span><span class="pill">CAMPING</span><span class="pill">RETAIL PB</span>
        </div>
      </div>
      <div class="stack">
        <div class="venture small lightcard">
          <div class="type">COMMERCIALIZATION</div>
          <h3>다양한 사업화 방식</h3>
          <p>식품·수산·HMR·유통기업과 제품화, OEM/ODM, PB, 공동사업 및 국내외 유통을 협의합니다.</p>
          <div class="pillrow"><span class="pill">공동사업</span><span class="pill">OEM / ODM</span><span class="pill">PB / 유통</span></div>
        </div>
        <div class="venture small">
          <div class="type">PARTNERSHIP OPTIONS</div>
          <h3>IP · 사업권 협의 가능</h3>
          <p>파트너의 역량과 시장에 맞춰 IP 라이선스·IP 양도·사업 양도·공동개발 등 다양한 구조를 열어두고 협의합니다.</p>
          <div class="pillrow"><span class="pill">IP LICENSE</span><span class="pill">IP TRANSFER</span><span class="pill">BUSINESS TRANSFER</span><span class="pill">CO-DEVELOPMENT</span></div>
        </div>
      </div>
    </div>
  </div>
</section>
'''

s = s[:future.start()] + shrimp_section + "\n" + s[future.start():]
path.write_text(s, encoding="utf-8")
print(f"Updated index.html; added submenu after project-4 in {nav_count} location(s).")
