"""소리 현황 · 필요한 느낌 페이지(웹 소리 찾기 스킬 0단계).

실행(프로젝트 루트에서): <python> <skill_dir>/scripts/build_status.py [needs.json] [out.html]
  needs.json을 빼면 <work_dir>/sound_needs.json(있으면), out을 빼면 <work_dir>/sound_status.html.
  게임 소리 파일을 같이 틀어야 해서 sound.preview_server(저장소 루트를 여는 로컬 서버)로 연다.

경로는 모두 .claude/skill-profile.yaml에서 읽는다(손으로 옮겨 적지 않는다).
  - sound.slots: 소리 순간 enum이 있는 C# 파일(순서 = 에셋의 id 번호). enum 이름은 sound.enum(기본 SoundId)
  - sound.tuning_asset: 순간별 소리 SO(.asset). 아래 형식을 줄 단위로 읽는다(형식이 다르면 parse_asset을 고친다)
      useOriginal · useTempTones · volume · musicVolume(맨 위)
      entries: - id: N / clip: <원작 클립 이름> / volume / pitchJitter / pickOne / single / layers: - clip: {guid} · volume · pitch · delay
  - sound.audio_dir: .meta의 guid로 파일을 찾을 폴더(기본: sound.sfx_dir의 부모)
  - sound.labels: 순간 이름표 JSON(선택, 아래 형식). 없으면 id 그대로 "기타"에 나온다
  - sound.original_game_dir · sound.original_listen_dir: 원작 소리 <clip>.ogg 폴더(선택, 원작 비교를 하는 프로젝트만)
      game_dir = 게임이 읽는 곳(스위치가 켜 있고 여기 있으면 "원작 소리"), listen_dir = 듣기만
  - docs.original_sounds: 원작 길이 표 md(선택, "| `clip` | … | 길이 |" 줄)
  - docs.credits_sound: 출처 표 md(선택, "## BY — …" 같은 절 아래 "| … | `Sfx/…` | [제목](주소) |" 줄)

labels JSON 형식(프로젝트에 두고 커밋한다):
{
  "groups": ["플레이어", "아이템", ...],              # 페이지 묶음 순서("기타"는 끝에 자동)
  "labels": {"Dash": ["대시 출발", "플레이어"], ...},  # 새 순간이 생기면 여기에 더한다
  "tempTones": ["Dot", ...]                           # 우리 소리 · 원작이 없을 때 코드로 만든 임시 삐가 나는 순간
}

needs.json 형식(Claude가 GDD · CONCEPT · 사용자 말에서 초안을 쓴다. 빠진 순간은 비워 둔다):
{
  "updated": "2026-10-24",
  "note": "페이지 머리에 보일 한 줄(선택)",
  "items": {
    "ReviveNo": {"want": "new|replace|check|keep", "feel": "느낌 · 소리 모양(사용자 말 그대로)",
                 "length": "0.3 s 안팎", "with": "같이 나는 소리", "why": "근거(GDD 소리 장 등)"}, ...
  }
}
  want: new = 우리 소리 없음 · 새로 필요, replace = 있지만 바꾸고 싶음, check = 귀로 확인 대기, keep = 그대로.
"""
import json
import os
import re
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.getcwd()  # 프로젝트 루트에서 실행한다(플러그인 캐시 위치와 무관)
TEMPLATE = os.path.join(HERE, "..", "assets", "status_template.html")
PROFILE = os.path.join(ROOT, ".claude", "skill-profile.yaml")


def read(p):
    return open(p, encoding="utf-8").read()


def _value(v):
    """주석 · 따옴표를 떼고, { a: 1, b: x } 한 줄 묶음은 dict로."""
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
    if v.startswith("{") and v.endswith("}"):
        return {k.strip(): _value(x) for k, x in (p.split(":", 1) for p in v[1:-1].split(",") if ":" in p)}
    if len(v) >= 2 and v[0] == v[-1] and v[0] in "\"'":
        return v[1:-1]
    return v


def read_profile(path):
    """skill-profile.yaml을 두 단계(최상위 · 두 칸 들여쓴 키)까지만 읽는다(-I 실행이라 PyYAML을 기대하지 않는다)."""
    prof, sect = {}, None
    for line in read(path).splitlines():
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


def path_of(prof, sect, key, default=None):
    v = (prof.get(sect) or {}).get(key) or default
    return os.path.join(ROOT, v) if v else None


def sound_ids(enum_cs, enum_name):
    src = read(enum_cs)
    m = re.search(r"enum\s+" + re.escape(enum_name) + r"\s*\{(.*?)\}", src, re.S)
    if not m:
        sys.exit(f"{enum_cs}: enum {enum_name}를 찾지 못함(프로필 sound.enum)")
    body = re.sub(r"//[^\n]*", "", m.group(1))
    return [s.split("=")[0].strip() for s in body.split(",") if s.strip()]


def parse_asset(asset):
    """소리 SO(Unity YAML)을 필요한 만큼만 읽는다. Unity YAML 태그 때문에 yaml 모듈 대신 줄 단위로."""
    flags, entries, cur, layer = {}, [], None, None
    for line in read(asset).splitlines():
        m = re.match(r"^  (useOriginal|useTempTones|volume|musicVolume): (\S+)", line)
        if m and cur is None:
            flags[m.group(1)] = float(m.group(2))
            continue
        m = re.match(r"^  - id: (\d+)", line)
        if m:
            cur = {"id": int(m.group(1)), "layers": []}
            entries.append(cur)
            layer = None
            continue
        if cur is None:
            continue
        m = re.match(r"^    - clip: \{fileID: (\d+)(?:, guid: (\w+))?", line)
        if m:
            layer = {"guid": m.group(2) if m.group(1) != "0" else None, "volume": 1.0, "pitch": 1.0, "delay": 0.0}
            cur["layers"].append(layer)
            continue
        m = re.match(r"^      (volume|pitch|delay): (\S+)", line)
        if m and layer is not None:
            layer[m.group(1)] = float(m.group(2))
            continue
        m = re.match(r"^    (clip|volume|pitchJitter|pickOne|single|layers): ?(.*)", line)
        if m:
            k, v = m.group(1), m.group(2).strip()
            if k == "layers":
                layer = None
            elif k == "clip":
                cur["clip"] = v
            else:
                cur[k] = float(v) if v else 0.0
    return flags, entries


def guid_files(audio):
    out = {}
    for d, _, files in os.walk(audio):
        for f in files:
            if not f.endswith(".meta") or os.path.isdir(os.path.join(d, f[:-5])):
                continue
            m = re.search(r"^guid: (\w+)", read(os.path.join(d, f)), re.M)
            if m:
                out[m.group(1)] = os.path.relpath(os.path.join(d, f[:-5]), audio).replace("\\", "/")
    return out


def original_lengths(md):
    out = {}
    if not md or not os.path.exists(md):
        return out
    for line in read(md).splitlines():
        m = re.match(r"^\| `([^`]+)` \|.*\| ([\d.]+) \|\s*$", line)
        if m:
            out[m.group(1)] = float(m.group(2))
    return out


def credits(md, audio_rel_prefixes):
    """출처 표 줄: 파일(audio_dir 기준 경로) → 라이선스 묶음 · 원본 링크. 절 제목(## BY …)이 묶음이다."""
    out, section = {}, ""
    if not md or not os.path.exists(md):
        return out
    pat = re.compile(r"`((?:" + "|".join(map(re.escape, audio_rel_prefixes)) + r")/[^`]+)`") if audio_rel_prefixes else None
    for line in read(md).splitlines():
        if line.startswith("## "):
            section = line[3:].strip()
            continue
        if not line.startswith("|") or not pat:
            continue
        cols = [c.strip() for c in line.strip().strip("|").split("|")]
        if len(cols) < 3:
            continue
        link = re.search(r"\[([^\]]+)\]\((https?://[^)]+)\)", cols[2])
        lic = "BY" if section.startswith("BY —") else "BY-NC" if section.startswith("BY-NC") else "free" if "필요 없음" in section else "?"
        for f in pat.findall(cols[1]):
            out[f] = {"lic": lic, "title": link.group(1) if link else cols[2][:60], "url": link.group(2) if link else ""}
    return out


def main():
    for s in (sys.stdout, sys.stderr):
        try:
            s.reconfigure(encoding="utf-8")
        except AttributeError:
            pass
    if not os.path.exists(PROFILE):
        sys.exit(f"{PROFILE} 없음: 프로젝트 루트에서 실행하고, 스킬 저장소 templates/skill-profile.yaml을 복사해 채운다")
    prof = read_profile(PROFILE)
    snd = prof.get("sound") or {}
    work = os.path.join(ROOT, prof.get("work_dir") or "references/web")
    enum_cs, asset = path_of(prof, "sound", "slots"), path_of(prof, "sound", "tuning_asset")
    if not enum_cs or not asset:
        sys.exit("프로필에 sound.slots · sound.tuning_asset이 없음")
    sfx = path_of(prof, "sound", "sfx_dir")
    audio = path_of(prof, "sound", "audio_dir") or (os.path.dirname(sfx.rstrip("/\\")) if sfx else None)
    if not audio:
        sys.exit("프로필에 sound.audio_dir(또는 sound.sfx_dir)이 없음")
    labels_path = path_of(prof, "sound", "labels")
    lab = json.load(open(labels_path, encoding="utf-8")) if labels_path and os.path.exists(labels_path) else {}
    labels = {k: tuple(v) for k, v in (lab.get("labels") or {}).items()}
    groups = [g for g in (lab.get("groups") or []) if g != "기타"] + ["기타"]
    temp_tone = set(lab.get("tempTones") or [])
    orig_game = path_of(prof, "sound", "original_game_dir")
    orig_listen = path_of(prof, "sound", "original_listen_dir")

    needs_path = sys.argv[1] if len(sys.argv) > 1 else os.path.join(work, "sound_needs.json")
    out = sys.argv[2] if len(sys.argv) > 2 else os.path.join(work, "sound_status.html")
    needs = json.load(open(needs_path, encoding="utf-8")) if os.path.exists(needs_path) else {"items": {}}
    out_dir = os.path.dirname(os.path.abspath(out))
    rel = lambda p: os.path.relpath(p, out_dir).replace("\\", "/")  # 페이지 기준 경로

    ids = sound_ids(enum_cs, snd.get("enum") or "SoundId")
    flags, entries = parse_asset(asset)
    files = guid_files(audio)
    prefixes = sorted({f.split("/")[0] for f in files.values() if "/" in f})
    lens = original_lengths(path_of(prof, "docs", "original_sounds"))
    creds = credits(path_of(prof, "docs", "credits_sound"), prefixes)
    use_orig, use_temp = flags.get("useOriginal", 1) > 0, flags.get("useTempTones", 1) > 0
    problems, rows = [], []
    if labels_path and not lab:
        problems.append(f"sound.labels 파일 없음: {os.path.relpath(labels_path, ROOT)}")
    for e in entries:
        if e["id"] >= len(ids):
            problems.append(f"에셋 id {e['id']}가 enum에 없음")
            continue
        sid = ids[e["id"]]
        label, group = labels.get(sid, (sid, "기타"))
        if group not in groups:
            groups.insert(-1, group)
        layers = []
        for l in e["layers"]:
            if not l["guid"]:
                continue
            f = files.get(l["guid"])
            if not f:
                problems.append(f"{sid}: guid {l['guid']} 파일 없음")
                continue
            layers.append({"file": f, "src": rel(os.path.join(audio, f)), "volume": l["volume"], "pitch": l["pitch"],
                           "delay": l["delay"], "credit": creds.get(f)})
        clip = e.get("clip") or ""
        in_game = bool(clip and orig_game) and os.path.exists(os.path.join(orig_game, clip + ".ogg"))
        orig_any = None
        for folder in (orig_game, orig_listen):
            if clip and folder and os.path.exists(os.path.join(folder, clip + ".ogg")):
                orig_any = rel(os.path.join(folder, clip + ".ogg"))
                break
        if layers:
            state = "own"
        elif use_orig and in_game:
            state = "original"
        elif use_temp and sid in temp_tone:
            state = "temp"
        else:
            state = "silent"
        rows.append({"id": sid, "label": label, "group": group, "state": state, "volume": e.get("volume", 1),
                     "pitchJitter": e.get("pitchJitter", 0), "pickOne": bool(e.get("pickOne")), "single": bool(e.get("single")),
                     "layers": layers, "orig": {"clip": clip, "len": lens.get(clip), "src": orig_any},
                     "need": needs.get("items", {}).get(sid)})
    for s in ids:
        if s not in {r["id"] for r in rows}:
            problems.append(f"{s}: 에셋에 항목 없음(조용)")
    for s in needs.get("items", {}):
        if s not in ids:
            problems.append(f"needs.json의 {s}가 enum에 없음")
    rows.sort(key=lambda r: (groups.index(r["group"]), ids.index(r["id"])))

    data = {"flags": {"useOriginal": use_orig, "useTempTones": use_temp, "musicVolume": flags.get("musicVolume")},
            "hasOriginal": bool(orig_game or orig_listen), "updated": needs.get("updated"), "note": needs.get("note"),
            "sources": [os.path.relpath(p, ROOT).replace("\\", "/") for p in (asset, path_of(prof, "docs", "original_sounds"),
                                                                              path_of(prof, "docs", "credits_sound")) if p],
            "groups": groups, "rows": rows}
    html = read(TEMPLATE).replace("/*DATA*/null", json.dumps(data, ensure_ascii=False))
    os.makedirs(out_dir, exist_ok=True)
    open(out, "w", encoding="utf-8").write(html)
    count = {k: sum(r["state"] == k for r in rows) for k in ("own", "original", "temp", "silent")}
    for p in problems:
        print("확인:", p, file=sys.stderr)
    print(f"{out}: 순간 {len(rows)}개 — 우리 소리 {count['own']} · 원작 {count['original']} · 임시 삐 {count['temp']} · 조용 {count['silent']}, "
          f"필요한 느낌 {len(needs.get('items', {}))}개, 확인 {len(problems)}건")
    page = os.path.relpath(out, ROOT).replace("\\", "/")
    server = snd.get("preview_server")
    if isinstance(server, dict) and server.get("port") and not page.startswith(".."):
        print(f"열기: http://localhost:{server['port']}/{page} (.claude/launch.json의 {server.get('name', '')} 서버)")


if __name__ == "__main__":
    main()
