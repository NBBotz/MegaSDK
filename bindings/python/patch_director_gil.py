#!/usr/bin/env python3

import pathlib
import re
import sys

if len(sys.argv) != 2:
    print("Usage: patch_director_gil.py <megaapiPYTHON_wrap.cxx>")
    sys.exit(1)

path = pathlib.Path(sys.argv[1])
text = path.read_text()

director_re = re.compile(
    r'((?:[\w:<>~]+\s+)+SwigDirector_[\w:]+::[\w~]+\([^)]*\)\s*\{)',
    re.MULTILINE,
)

matches = list(director_re.finditer(text))

if not matches:
    print("No director methods found")
    sys.exit(1)

result = []
last = 0
patched = 0

for m in matches:
    start = m.start()
    body_start = m.end()

    result.append(text[last:body_start])

    depth = 1
    pos = body_start

    while pos < len(text) and depth:
        ch = text[pos]

        if ch == "{":
            depth += 1
        elif ch == "}":
            depth -= 1

        pos += 1

    body = text[body_start:pos - 1]

    body = body.replace(
        "SWIG_PYTHON_THREAD_BEGIN_BLOCK;",
        ""
    )

    body = body.replace(
        "SWIG_PYTHON_THREAD_END_BLOCK;",
        ""
    )

    replacement = f"""
  PyGILState_STATE __gil = PyGILState_Ensure();

  {{
{body}
  }}

  PyGILState_Release(__gil);
"""

    result.append(replacement)

    last = pos - 1
    patched += 1

result.append(text[last:])

path.write_text("".join(result))

print(f"Patched {patched} director methods.")