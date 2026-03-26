import pathlib, re
t = pathlib.Path('b2b/index.html').read_text('utf-8')
for m in re.finditer(r"'fondente':", t):
    line_start = t.rfind('\n', 0, m.start()) + 1
    line_end = t.find('\n', m.start())
    line = t[line_start:line_end].strip()
    print(f'At {m.start()}: {line[:120]}')
