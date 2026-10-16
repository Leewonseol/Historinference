#!/usr/bin/env python3
"""Fetch historical CLASSICAL CHINESE primary text from official sites only.

No modern Korean translation or webpage HTML is published by this script.
Extraction is provisional until article-boundary and completeness QA.
"""
import csv,hashlib,json,pathlib,re,time,urllib.parse,datetime,sys
import requests
from bs4 import BeautifulSoup

ROOT=pathlib.Path(__file__).resolve().parents[1]
INPUT=ROOT/"research/source_register.csv"
DEST=ROOT/"research/primary_originals"
DEST.mkdir(parents=True,exist_ok=True)
ALLOWED={"sillok.history.go.kr","db.history.go.kr","sjw.history.go.kr"}
CH=re.compile(r"[\u3400-\u9fff]")
KR=re.compile(r"[\uac00-\ud7af]")
BREAK_TAGS={"p","blockquote","td","dd","li","section","div","article"}
def clean(x):
    return "\n".join(z.strip() for z in x.replace("\xa0"," ").splitlines() if z.strip())
def asian_counts(t):
    return len(CH.findall(t)),len(KR.findall(t))
def likely_chinese(t):
    han,hang=asian_counts(t)
    return han>=45 and han >= 4*(hang+1) and han/max(1,len(t)) > .32
def extract(html):
    soup=BeautifulSoup(html,"html.parser")
    for x in soup(["script","style","noscript","header","footer","nav","form"]):x.decompose()
    # Find original-text sections, not published Korean translation.
    candidates=[]
    rx=re.compile(r"(?:hanmun|hanja|original|classical|view_han|hanja_txt|org_content|original_text)",re.I)
    for t in soup.find_all(True):
        attr=" ".join(map(str,[t.get("id") or "", " ".join(t.get("class") or [])]))
        if rx.search(attr):
            val=clean(t.get_text("\n",strip=True))
            if likely_chinese(val) and len(val)>180:
                candidates.append(val)
    candidates.sort(key=len,reverse=True)
    # If named container exists, keep the longest, since it may wrap the full article.
    if candidates:
        chosen=candidates[0]
        return chosen, "CSS_ORIGINAL_CONTAINER_CANDIDATE"
    # Fallback individual substantial paragraphs, excluding nested duplicates.
    paragraphs=[]
    for t in soup.find_all(["p","blockquote","td","dd"]):
        txt=clean(t.get_text(" ",strip=True))
        if likely_chinese(txt) and len(txt)>60:
            paragraphs.append(txt)
    if not paragraphs:
        for t in soup.find_all(["div","article","section"]):
            if t.find(["div","article","section","p","blockquote","td","dd"]): continue
            txt=clean(t.get_text(" ",strip=True))
            if likely_chinese(txt) and len(txt)>80:paragraphs.append(txt)
    uniq=[];seen=set()
    for p in paragraphs:
        if p not in seen:seen.add(p);uniq.append(p)
    return "\n\n".join(uniq),"HANJA_PARAGRAPH_HEURISTIC_UNVERIFIED"
sess=requests.Session()
sess.headers.update({"User-Agent":"Historinference-source-verification/1.0 (research, rate-limited; github.com/Leewonseol/Historinference)","Accept-Language":"ko-KR,ko;q=0.9"})
records=[]
with INPUT.open(encoding="utf-8-sig",newline="") as f: rows=list(csv.DictReader(f))
for idx,row in enumerate(rows):
    sid=row["source_id"];url=row["url"]
    host=urllib.parse.urlparse(url).hostname
    rec={"source_id":sid,"case_id":row["case_id"],"url":url,"status":"NOT_ATTEMPTED","mode":None,"http_status":None,"original_han_characters":0,"source_sha256":None,"filename":None}
    if host not in ALLOWED or not url.startswith("https://"):
        rec["status"]="REJECTED_NON_OFFICIAL"
    else:
        try:
            res=sess.get(url,timeout=22)
            rec["http_status"]=res.status_code
            res.raise_for_status()
            raw,mode=extract(res.text)
            rec["mode"]=mode;rec["html_received_bytes"]=len(res.content)
            rec["original_han_characters"]=len(CH.findall(raw))
            if rec["original_han_characters"]>=250:
                fname=re.sub(r"[^A-Za-z0-9_-]","_",sid)+".txt"
                text="# SOURCE "+sid+"\n# URL "+url+"\n# METHOD "+mode+"\n# STATUS PROVISIONAL_NOT_COMPLETE_VERIFIED\n# Caution: automatically extracted Chinese-only candidates; boundaries/editions not verified.\n\n"+raw+"\n"
                (DEST/fname).write_text(text,encoding="utf-8")
                rec["source_sha256"]=hashlib.sha256(text.encode("utf-8")).hexdigest()
                rec["filename"]=fname
                rec["status"]="EXTRACTED_NEEDS_COMPLETE_TEXT_QA"
            else:
                rec["status"]="NO_RELIABLE_HANJA_EXTRACT"
        except Exception as e:
            rec["status"]="FETCH_ERROR"
            rec["error"]=str(e)[:300]
    records.append(rec)
    print(f"{idx+1}/{len(rows)} {sid}: {rec['status']} han={rec['original_han_characters']}",flush=True)
    if idx<len(rows)-1:time.sleep(1.5)
out={"generated_at_utc":datetime.datetime.now(datetime.timezone.utc).isoformat(),"source_count":len(rows),"record_status":"AUTOMATED_FETCH_NOT_FINAL_VERIFICATION","records":records}
(DEST/"manifest.json").write_text(json.dumps(out,ensure_ascii=False,indent=2)+"\n",encoding="utf-8")
print("SUCCESS",sum(r["status"]=="EXTRACTED_NEEDS_COMPLETE_TEXT_QA" for r in records),"/",len(records))
