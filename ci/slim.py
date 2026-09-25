"""Build a slim Odoo 19 CE tree: core + dependency closure of ROOTS, without static/i18n/tests."""
import ast, os, shutil, sys, tarfile
SRC, DST = sys.argv[1], sys.argv[2]
ROOTS = ["base", "web", "mail", "crm", "project", "contacts", "base_setup", "web_tour", "html_editor", "iap", "rpc", "test_mail", "mail_bot", "sms", "microsoft_outlook", "google_gmail"]
ADDONS = os.path.join(SRC, "addons")
def manifest(name):
    for root in (ADDONS, os.path.join(SRC, "odoo", "addons")):
        p = os.path.join(root, name, "__manifest__.py")
        if os.path.exists(p):
            return root, ast.literal_eval(open(p).read())
    raise SystemExit("missing addon " + name)
need, todo = set(), list(ROOTS)
while todo:
    n = todo.pop()
    if n in need: continue
    need.add(n)
    todo += manifest(n)[1].get("depends", [])
print("addons:", len(need), sorted(need))
SKIP = {"i18n", "__pycache__"}
def prune(r, dirs):
    dirs[:] = [d for d in dirs if d not in SKIP]
    if os.path.basename(r) == "static":
        dirs[:] = [d for d in dirs if d in ("img", "description")]
def copy(src, dst):
    for r, dirs, files in os.walk(src):
        prune(r, dirs)
        rel = os.path.relpath(r, src)
        os.makedirs(os.path.join(dst, rel), exist_ok=True)
        for f in files:
            if f.endswith((".pyc", ".po", ".pot")): continue
            shutil.copy2(os.path.join(r, f), os.path.join(dst, rel, f))
# core (odoo/ package) but skip odoo/addons/* except base and keep base tests? no
core_src = os.path.join(SRC, "odoo")
for r, dirs, files in os.walk(core_src):
    rel = os.path.relpath(r, core_src)
    if rel.startswith("addons") and rel != "addons":
        # only 'base' and 'test_*' are here; keep base only
        parts = rel.split(os.sep)
        if parts[1] != "base": dirs[:] = []; continue
    prune(r, dirs)
    os.makedirs(os.path.join(DST, "odoo", rel), exist_ok=True)
    for f in files:
        if f.endswith((".pyc", ".po", ".pot")): continue
        shutil.copy2(os.path.join(r, f), os.path.join(DST, "odoo", rel, f))
# web needs a few static files? keep web/static/src/... no. But base/static/description not needed.
for n in need:
    root, _ = manifest(n)
    if root == ADDONS:
        copy(os.path.join(ADDONS, n), os.path.join(DST, "addons", n))
for f in ("odoo-bin", "requirements.txt", "setup.py", "LICENSE"):
    if os.path.exists(os.path.join(SRC, f)): shutil.copy2(os.path.join(SRC, f), DST)
