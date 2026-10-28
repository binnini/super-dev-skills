"""이미지 생성 기록 · 고르기(imagegen 스킬 6 · 8단계).

실행(프로젝트 루트에서):
  <python> <skill_dir>/scripts/imagegen_log.py record --key K --purpose draft|game --model M --ratio R --prompt-file P
                                                  [--count N] [--ref F ...] [--original-ref F ...] [--library L] [--note T]
  <python> <skill_dir>/scripts/imagegen_log.py list [--key K]
  <python> <skill_dir>/scripts/imagegen_log.py pick --key K --id N --file F

기록 위치: <work_dir>/imagegen/<key>/<id>.json + <work_dir>/imagegen/log.jsonl(한 줄 = 한 기록 · 고르기)
프로필(.claude/skill-profile.yaml)에서 읽는 값:
  work_dir, imagegen.style_pack(JSON, version을 기록에 남김), imagegen.original_refs(never | draft_only | allow, 기본 never),
  imagegen.out_dir(draft 용도 고른 것), imagegen.draft_dir(game 용도 고른 것)
"""
import argparse
import datetime
import json
import os
import re
import shutil
import sys

for _s in (sys.stdout, sys.stderr):  # Windows 콘솔(cp949)에서 한글이 깨지거나 멈추지 않게(-I는 PYTHONIOENCODING을 무시)
    try:
        _s.reconfigure(encoding="utf-8")
    except AttributeError:
        pass

ROOT = os.getcwd()  # 프로젝트 루트에서 실행한다(플러그인 캐시 위치와 무관)
PROFILE = os.path.join(ROOT, ".claude", "skill-profile.yaml")


def _value(v):
    """주석 · 따옴표를 뗀다."""
    out, quote = "", None
    for i, ch in enumerate(v):
        if quote:
            quote = None if ch == quote else quote
        elif ch in "\"'":
            quote = ch
        elif ch == "#" and (i == 0 or v[i - 1] == " "):
            break
        out += ch
    v = out.strip()
    if len(v) >= 2 and v[0] == v[-1] and v[0] in "\"'":
        return v[1:-1]
    return v


def read_profile():
    """skill-profile.yaml을 두 단계(최상위 · 들여쓴 키)까지만 읽는다(-I 실행이라 PyYAML을 기대하지 않는다)."""
    if not os.path.exists(PROFILE):
        sys.exit(f"{PROFILE}가 없다. 스킬 저장소 templates/skill-profile.yaml을 복사해 채운다.")
    prof, sect = {}, None
    for line in open(PROFILE, encoding="utf-8").read().splitlines():
        if not line.strip() or line.lstrip().startswith("#"):
            continue
        m = re.match(r"^(\s*)([A-Za-z_][\w-]*):\s?(.*)$", line)
        if not m:
            continue
        indent, key, v = len(m.group(1)), m.group(2), _value(m.group(3))
        if indent == 0:
            if v == "":
                sect = prof.setdefault(key, {})
            else:
                prof[key], sect = v, None
        elif sect is not None:
            sect[key] = v
    return prof


def log_dir(prof):
    wd = prof.get("work_dir")
    if not wd:
        sys.exit("프로필 work_dir가 비어 있다(git 무시 작업 폴더).")
    return os.path.join(ROOT, wd, "imagegen")


def style_version(prof):
    p = (prof.get("imagegen") or {}).get("style_pack")
    if not p:
        return None
    full = os.path.join(ROOT, p)
    if not os.path.exists(full):
        sys.exit(f"스타일 팩이 없다: {p}(프로필 imagegen.style_pack)")
    return json.load(open(full, encoding="utf-8")).get("version")


def rel(p):
    return os.path.relpath(os.path.abspath(p), ROOT).replace("\\", "/")


def append_log(base, entry):
    with open(os.path.join(base, "log.jsonl"), "a", encoding="utf-8") as f:
        f.write(json.dumps(entry, ensure_ascii=False) + "\n")


def cmd_record(a, prof):
    rule = (prof.get("imagegen") or {}).get("original_refs") or "never"
    if rule not in ("never", "draft_only", "allow"):
        sys.exit(f"프로필 imagegen.original_refs 값이 이상하다: {rule}(never | draft_only | allow)")
    if a.original_ref and (rule == "never" or (rule == "draft_only" and a.purpose != "draft")):
        sys.exit(f"원작 그림 참조는 규칙({rule})상 용도 {a.purpose}에 쓸 수 없다. 생성을 보내지 않는다.")
    for f in [a.prompt_file] + a.ref + a.original_ref:
        if not os.path.exists(f):
            sys.exit(f"파일이 없다: {f}")
    base = log_dir(prof)
    kdir = os.path.join(base, a.key)
    os.makedirs(kdir, exist_ok=True)
    ids = [int(n[:-5]) for n in os.listdir(kdir) if re.fullmatch(r"\d+\.json", n)]
    rid = max(ids, default=0) + 1
    entry = {
        "type": "record", "key": a.key, "id": rid,
        "time": datetime.datetime.now().isoformat(timespec="seconds"),
        "purpose": a.purpose, "model": a.model, "ratio": a.ratio, "count": a.count,
        "prompt": open(a.prompt_file, encoding="utf-8").read().strip(),
        "refs": [rel(f) for f in a.ref], "original_refs": [rel(f) for f in a.original_ref],
        "style_pack_version": style_version(prof), "library": a.library, "note": a.note, "picked": [],
    }
    json.dump(entry, open(os.path.join(kdir, f"{rid}.json"), "w", encoding="utf-8"), ensure_ascii=False, indent=2)
    append_log(base, entry)
    print(f"기록 {a.key} #{rid} → {rel(os.path.join(kdir, f'{rid}.json'))}")


def cmd_list(a, prof):
    base = log_dir(prof)
    keys = [a.key] if a.key else sorted(d for d in os.listdir(base) if os.path.isdir(os.path.join(base, d))) if os.path.isdir(base) else []
    for k in keys:
        kdir = os.path.join(base, k)
        for n in sorted((n for n in os.listdir(kdir) if re.fullmatch(r"\d+\.json", n)), key=lambda n: int(n[:-5])) if os.path.isdir(kdir) else []:
            e = json.load(open(os.path.join(kdir, n), encoding="utf-8"))
            picked = ", ".join(e.get("picked") or []) or "-"
            print(f"{k} #{e['id']}  {e['time']}  {e['model']}  {e['ratio']}  {e['purpose']}  팩 v{e.get('style_pack_version')}  고름: {picked}")


def cmd_pick(a, prof):
    base = log_dir(prof)
    path = os.path.join(base, a.key, f"{a.id}.json")
    if not os.path.exists(path):
        sys.exit(f"기록이 없다: {a.key} #{a.id}")
    if not os.path.exists(a.file):
        sys.exit(f"파일이 없다: {a.file}")
    e = json.load(open(path, encoding="utf-8"))
    dest_key = "out_dir" if e["purpose"] == "draft" else "draft_dir"
    dest = (prof.get("imagegen") or {}).get(dest_key)
    if not dest:
        sys.exit(f"프로필 imagegen.{dest_key}가 비어 있다(용도 {e['purpose']})")
    os.makedirs(os.path.join(ROOT, dest), exist_ok=True)
    ext = os.path.splitext(a.file)[1] or ".png"
    n = len(e.get("picked") or []) + 1
    name = f"{a.key}_{a.id}{'' if n == 1 else '_' + str(n)}{ext}"
    target = os.path.join(ROOT, dest, name)
    shutil.copyfile(a.file, target)
    e.setdefault("picked", []).append(rel(target))
    json.dump(e, open(path, "w", encoding="utf-8"), ensure_ascii=False, indent=2)
    append_log(base, {"type": "pick", "key": a.key, "id": a.id, "file": rel(target),
                      "time": datetime.datetime.now().isoformat(timespec="seconds")})
    print(f"고름 {a.key} #{a.id} → {rel(target)}")


def main():
    ap = argparse.ArgumentParser(description="이미지 생성 기록 · 고르기")
    sub = ap.add_subparsers(dest="cmd", required=True)
    r = sub.add_parser("record")
    r.add_argument("--key", required=True)
    r.add_argument("--purpose", required=True, choices=["draft", "game"])
    r.add_argument("--model", required=True)
    r.add_argument("--ratio", required=True)
    r.add_argument("--prompt-file", required=True)
    r.add_argument("--count", type=int, default=1)
    r.add_argument("--ref", action="append", default=[])
    r.add_argument("--original-ref", action="append", default=[])
    r.add_argument("--library", default="")
    r.add_argument("--note", default="")
    li = sub.add_parser("list")
    li.add_argument("--key")
    p = sub.add_parser("pick")
    p.add_argument("--key", required=True)
    p.add_argument("--id", type=int, required=True)
    p.add_argument("--file", required=True)
    a = ap.parse_args()
    if a.cmd == "record" and not re.fullmatch(r"[A-Za-z0-9_-]+", a.key):
        sys.exit("--key는 영문 · 숫자 · _ · -만 쓴다(폴더 이름이 된다)")
    prof = read_profile()
    {"record": cmd_record, "list": cmd_list, "pick": cmd_pick}[a.cmd](a, prof)


if __name__ == "__main__":
    main()
