from pathlib import Path
import sys
import json
import urllib.request
import urllib.parse
import webbrowser
import threading
import re


class TwitchBridge:
    """Small bridge for Twitch device authorization from the desktop UI."""
    def open_url(self, url: str) -> None:
        parsed = urllib.parse.urlparse(url)
        if parsed.scheme == "https" and parsed.hostname in ("twitch.tv", "www.twitch.tv") and parsed.path.rstrip("/") == "/activate":
            # Launch off the pywebview bridge thread so Windows ShellExecute
            # cannot block the JavaScript callback while starting the browser.
            threading.Thread(target=webbrowser.open, args=(url,), daemon=True).start()

    def request(self, url: str, data=None, user_agent=None):
        body = urllib.parse.urlencode(data).encode() if data else None
        headers = {"Content-Type": "application/x-www-form-urlencoded"}
        if user_agent:
            headers["User-Agent"] = user_agent
        req = urllib.request.Request(url, data=body, headers=headers)
        try:
            with urllib.request.urlopen(req, timeout=15) as response:
                return json.loads(response.read())
        except Exception as exc:
            try:
                return json.loads(exc.read())
            except Exception:
                return {"error": str(exc)}

    # Twitch TV client used by the reference TDM project for device login.
    CLIENT_ID = "ue6666qo983tsx6so1t0vnawi233wa"
    TV_USER_AGENT = "Mozilla/5.0 (Linux; Android 9; SHIELD Android TV) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/138.0 Safari/537.36"
    DEVICE_SCOPES = "channel_read chat:read user_blocks_edit user_blocks_read user_follows_edit user_read"
    ANDROID_CLIENT_ID = "kd1unb4b3q4t58fwlpcbzcbnm76a8fp"
    sessions = {}

    def start_device_flow(self):
        result = self.request("https://id.twitch.tv/oauth2/device", {"client_id": self.CLIENT_ID, "scopes": self.DEVICE_SCOPES}, user_agent=self.TV_USER_AGENT)
        return result

    def poll_token(self, device_code: str):
        return self.request("https://id.twitch.tv/oauth2/token", {
            "client_id": self.CLIENT_ID, "device_code": device_code,
            "scopes": self.DEVICE_SCOPES,
            "grant_type": "urn:ietf:params:oauth:grant-type:device_code"}, user_agent=self.TV_USER_AGENT)

    def get_user(self, token: str):
        req = urllib.request.Request("https://api.twitch.tv/helix/users", headers={"Client-Id": self.CLIENT_ID, "Authorization": "Bearer " + token})
        with urllib.request.urlopen(req, timeout=15) as response:
            users = json.loads(response.read()).get("data", [])
        return users[0] if users else {}

    def import_token(self, token: str):
        """Validate an imported OAuth token and return only public profile fields."""
        req = urllib.request.Request("https://id.twitch.tv/oauth2/validate", headers={"Authorization": "OAuth " + token.strip()})
        try:
            with urllib.request.urlopen(req, timeout=15) as response:
                profile = json.loads(response.read())
            if profile.get("client_id") not in (self.CLIENT_ID, self.ANDROID_CLIENT_ID):
                return {"error": "wrong_client"}
            login = profile.get("login", "")
            self.sessions[login.lower()] = (token.strip(), profile["client_id"])
            return {"login": login, "user_id": profile.get("user_id", ""), "drops": self.get_drops(token.strip(), profile["client_id"])}
        except Exception:
            return {"error": "invalid_token"}

    def recheck_account(self, login: str):
        session = self.sessions.get(login.lower())
        if not session:
            return {"error": "session_missing", "login": login}
        token, client_id = session
        return {"login": login, "drops": self.get_drops(token, client_id)}

    def get_drops(self, token, client_id):
        op = {"operationName":"Inventory","variables":{},"extensions":{"persistedQuery":{"version":1,"sha256Hash":"d86775d0ef16a63a33ad52e80eaff963b2d5b72fada7c991504a57496e1d8e4b"}}}
        req=urllib.request.Request("https://gql.twitch.tv/gql", data=json.dumps(op).encode(), headers={"Content-Type":"application/json","Client-Id":client_id,"Authorization":"OAuth "+token})
        try:
            with urllib.request.urlopen(req,timeout=20) as response: body=json.loads(response.read())
            camps=body.get("data",{}).get("currentUser",{}).get("inventory",{}).get("dropCampaignsInProgress",[])
            game_map={}
            dashboard={"operationName":"ViewerDropsDashboard","variables":{"fetchRewardCampaigns":False},"extensions":{"persistedQuery":{"version":1,"sha256Hash":"5a4da2ab3d5b47c9f9ce864e727b2cb346af1e3ea8b897fe8f704a97ff017619"}}}
            try:
                gql=urllib.request.Request("https://gql.twitch.tv/gql",data=json.dumps(dashboard).encode(),headers={"Content-Type":"application/json","Client-Id":client_id,"Authorization":"OAuth "+token})
                with urllib.request.urlopen(gql,timeout=15) as response: dash=json.loads(response.read())
                for c in dash.get("data",{}).get("currentUser",{}).get("dropCampaigns",[]):
                    game=c.get("game") or {}; art=game.get("boxArtURL","").replace("{width}","80").replace("{height}","110")
                    game_map[c.get("id")]=(game.get("displayName","Twitch Drops"),art)
            except Exception: pass
            out=[]
            for camp in camps:
                camp_drops=[]
                for drop in camp.get("timeBasedDrops",[]):
                    state=drop.get("self") or {}; reqmin=drop.get("requiredMinutesWatched",0); mins=state.get("currentMinutesWatched",0)
                    camp_drops.append({"name":drop.get("name","Награда"),"pct":min(100,round(mins*100/reqmin)) if reqmin else (100 if state.get("isClaimed") else 0),"claimed":state.get("isClaimed",False),"minutes":mins,"required":reqmin})
                if camp_drops:
                    pct=sum(d["pct"] for d in camp_drops)/len(camp_drops)
                    game,art=game_map.get(camp.get("id"),("Twitch Drops",""))
                    out.append({"campaign":camp.get("name") or camp.get("id","Twitch Drops"),"game":game,"art":art,"drops":camp_drops,"pct":pct,"claimed":all(d["claimed"] for d in camp_drops)})
            return out
        except Exception: return []

import webview


def resource_root() -> Path:
    if getattr(sys, "frozen", False):
        return Path(sys._MEIPASS)
    return Path(__file__).resolve().parents[1]


def main() -> None:
    index_file = resource_root() / "index.html"
    if not index_file.is_file():
        raise FileNotFoundError(f"Не найден интерфейс приложения: {index_file}")

    bridge = TwitchBridge()
    webview.create_window(
        title="Drops Monitor",
        url=index_file.as_uri(),
        width=1440,
        height=940,
        min_size=(1024, 680),
        maximized=True,
        background_color="#0c0a10",
        js_api=bridge,
    )
    webview.start(gui="edgechromium", debug=False)


if __name__ == "__main__":
    main()
