import json, csv, os
from functools import lru_cache
from typing import Dict, Tuple
from pydantic import BaseModel, ValidationError
from google.cloud import storage
from flask import Request, make_response

BUCKET = os.getenv("GCS_BUCKET", "")
NEW_PATH = os.getenv("NEW_CSV_PATH", "kanji/kanji_strokes_new.csv")
OLD_PATH = os.getenv("OLD_CSV_PATH", "kanji/kanji_strokes_old.csv")
DEFAULT_VARIANT = os.getenv("DEFAULT_VARIANT", "new")
SINGLE_CHAR_PLUS_ONE = os.getenv("SINGLE_CHAR_PLUS_ONE", "false").lower() == "true"
ALLOWED_ORIGIN = os.getenv("ALLOWED_ORIGIN", "*")

class JudgeReq(BaseModel):
    sei: str
    mei: str
    variant: str | None = None

GOOD_SET = {1,3,5,6,7,8,11,13,15,16,17,18,21,23,24,25,29,31,32,33,35,37,39,41,45,47}
def _luck(n: int) -> str: return "吉" if n in GOOD_SET else "凶"

def _load_csv_from_gcs(path: str) -> Dict[str, int]:
    if not BUCKET:
        raise RuntimeError("GCS_BUCKET is not set")
    client = storage.Client()
    blob = client.bucket(BUCKET).blob(path)
    data = blob.download_as_text(encoding="utf-8")
    d: Dict[str, int] = {}
    for row in csv.DictReader(data.splitlines()):
        ch, st = row.get("char"), row.get("strokes")
        if ch and st: d[ch] = int(st)
    return d

@lru_cache(maxsize=2)
def get_dicts() -> Tuple[Dict[str,int], Dict[str,int]]:
    new_d = _load_csv_from_gcs(NEW_PATH)
    old_d = _load_csv_from_gcs(OLD_PATH) if OLD_PATH else {}
    return new_d, old_d

def _sum_strokes(s: str, d: Dict[str,int]) -> int:
    return sum(d.get(ch, 0) for ch in s)

def _calc(req: JudgeReq) -> dict:
    new_d, old_d = get_dicts()
    variant = (req.variant or DEFAULT_VARIANT).lower()
    dic = new_d if variant == "new" else old_d or new_d

    sei_sum = _sum_strokes(req.sei, dic)
    mei_sum = _sum_strokes(req.mei, dic)

    tenkaku = sei_sum
    chikaku = mei_sum
    if SINGLE_CHAR_PLUS_ONE:
        if len(req.sei) == 1: tenkaku += 1
        if len(req.mei) == 1: chikaku += 1

    jinkaku = dic.get(req.sei[-1], 0) + dic.get(req.mei[0], 0)
    soukaku = tenkaku + chikaku
    gaikaku = soukaku - jinkaku

    def pack(v: int): return {"value": v, "luck": _luck(v), "comment": ""}

    return {
        "tenkaku": pack(tenkaku),
        "jinkaku": pack(jinkaku),
        "chikaku": pack(chikaku),
        "gaikaku": pack(gaikaku),
        "soukaku": pack(soukaku),
        "summary": "簡易鑑定（新旧や単字+1は設定で切替）。"
    }

def _cors(resp):
    resp.headers["Access-Control-Allow-Origin"] = ALLOWED_ORIGIN
    resp.headers["Access-Control-Allow-Headers"] = "Content-Type"
    resp.headers["Access-Control-Allow-Methods"] = "POST, OPTIONS"
    return resp

def judge(request: Request):
    if request.method == "OPTIONS":
        return _cors(make_response("", 204))
    try:
        body = request.get_json(silent=True) or {}
        req = JudgeReq(**body)
        result = _calc(req)
        resp = make_response(json.dumps(result, ensure_ascii=False), 200)
        resp.headers["Content-Type"] = "application/json; charset=utf-8"
        return _cors(resp)
    except ValidationError as ve:
        resp = make_response(ve.json(), 400)
        resp.headers["Content-Type"] = "application/json; charset=utf-8"
        return _cors(resp)
    except Exception:
        resp = make_response(json.dumps({"error":"internal_error"}), 500)
        resp.headers["Content-Type"] = "application/json; charset=utf-8"
        return _cors(resp)
