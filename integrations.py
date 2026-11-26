import os, datetime, re
import httpx
from zoneinfo import ZoneInfo

TOOLS = {'time': 'Current time in Chennai', 'gmail': 'List recent Gmail message IDs and snippets', 'drive': 'List recent Google Drive files', 'calendar': 'List upcoming calendar events'}
async def google(path, params):
    required = ['GOOGLE_CLIENT_ID','GOOGLE_CLIENT_SECRET','GOOGLE_REFRESH_TOKEN']
    if not all(os.getenv(k) for k in required):
        raise ValueError('Google authorization not configured')
    async with httpx.AsyncClient(timeout=20) as c:
        r=await c.post('https://oauth2.googleapis.com/token',data={'client_id':os.environ[required[0]],'client_secret':os.environ[required[1]],'refresh_token':os.environ[required[2]],'grant_type':'refresh_token'}); r.raise_for_status()
        r=await c.get('https://www.googleapis.com/'+path,params=params,headers={'Authorization':'Bearer '+r.json()['access_token']}); r.raise_for_status(); return r.json()
async def execute(name):
    if name=='time': return datetime.datetime.now(ZoneInfo('Asia/Kolkata')).isoformat()
    if name=='drive': return await google('drive/v3/files',{'pageSize':10,'fields':'files(id,name,modifiedTime,webViewLink)','orderBy':'modifiedTime desc','q':'trashed = false'})
    if name=='calendar': return await google('calendar/v3/calendars/primary/events',{'maxResults':10,'singleEvents':'true','orderBy':'startTime','timeMin':datetime.datetime.now(datetime.timezone.utc).isoformat()})
    if name=='gmail': return await google('gmail/v1/users/me/messages',{'maxResults':10})
    raise ValueError('Unknown tool')
def select_tool(text):
    # Conservative deterministic routing, no arbitrary commands or writes.
    s=text.strip().lower().rstrip('?.!')
    patterns={'time':r'(what (is|s) the time|current time|time now|இப்போ என்ன நேரம்)', 'gmail':r'(show|list|check) (my )?(recent )?(emails|gmail)', 'drive':r'(show|list) (my )?(recent )?(drive files|google drive files)', 'calendar':r'(show|check|list) (my )?(upcoming )?(calendar|events|schedule)'}
    return next((k for k,p in patterns.items() if re.fullmatch(p,s)),None)
def retrieve(query, rows, limit=8):
    words=set(re.findall(r'\w+',query.lower()))
    return sorted(rows,key=lambda r:len(words & set(re.findall(r'\w+',r.lower()))),reverse=True)[:limit]
