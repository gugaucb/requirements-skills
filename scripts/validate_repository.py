from pathlib import Path
import re,sys
R=Path(__file__).resolve().parents[1]
def check():
 problems=[]
 canonical=list((R/'.agents/skills').glob('*/SKILL.md'))
 adapters=list((R/'.claude/skills').glob('*/SKILL.md'))
 if len(canonical)!=15 or len(adapters)!=15:problems.append('Expected 15 canonical skills and 15 adapters')
 for f in canonical+adapters:
  s=f.read_text(); name=f.parent.name
  if not s.startswith('---\n') or not re.search(r'^name: '+re.escape(name)+r'$',s,re.M) or not re.search(r'^description: .+',s,re.M):problems.append(f'Bad frontmatter: {f}')
  if 'Call the Skill tool with' in s:problems.append(f'Non-portable trigger: {f}')
  if f in adapters and f'.agents/skills/{name}/SKILL.md' not in s:problems.append(f'Bad adapter reference: {f}')
 for name in ('setup-requirements-repo','create-product-vision'):
  for prefix in ('.agents/skills','.claude/skills'):
   if 'disable-model-invocation: true' not in (R/prefix/name/'SKILL.md').read_text():problems.append(f'Expected manual trigger: {name}')
 for f in R.rglob('*.md'):
  for target in re.findall(r'(?<!!)\[[^\]]+\]\(([^)]+)\)',f.read_text()):
   if target.startswith(('https:','http:','#','mailto:')):continue
   if not (f.parent/target.split('#')[0]).exists():problems.append(f'Broken link: {f} -> {target}')
 v=(R/'docs/VOCABULARY.md').read_text()
 for ident in ('GOAL-','CAP-','EPIC-','US-','FR-','NFR-','AC-','TC-'):
  if ident not in v:problems.append(f'Missing vocabulary ID: {ident}')
 example=(R/'examples/vision/PRODUCT-VISION.md').read_text()
 if 'GOAL-001' not in example or 'CAP-001' not in example:problems.append('Bad example')
 return problems
if __name__=='__main__':
 p=check()
 for x in p:print(x)
 print('PASS' if not p else 'FAIL',len(list((R/'.agents/skills').glob('*/SKILL.md'))),'skills')
 sys.exit(bool(p))
