import time
from time import time
from flask import Flask, request, jsonify, url_for, Response, stream_with_context
from playwright.sync_api import sync_playwright
from playwright_stealth import stealth_sync
import logging
import random
from random import choices
from string import ascii_letters, digits
import re
from playwright.async_api import async_playwright
import json
import codecs
import base64
import binascii
import requests
from Crypto.Cipher import AES
from Crypto.Util.Padding import unpad
from urllib.parse import urljoin, quote, unquote, urlsplit
import urllib3
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = Flask(__name__)

BASE_API = "http://localhost:8888"
USER_AGENTS = [
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
]

@app.after_request
def add_cors_headers(response):
    response.headers["Access-Control-Allow-Origin"] = "*"
    response.headers["Access-Control-Allow-Methods"] = "GET, POST, OPTIONS"
    response.headers["Access-Control-Allow-Headers"] = "*"
    return response

@app.route('/', methods=['GET'])
def get_html():
    raw_url = request.args.get('raw')
    if not raw_url:
        return jsonify({
            "message": "Api is ready !",
            "documentation": {
                "version": "1.0",
                "base_url": f"{BASE_API}"
            },
            'endpoints' : {
                '/vidmoly' : {
                    'description': 'Extraction HLS pour Vidmoly via Playwright.',
                    'parameter' : [{
                        'name' : 'url',
                        'type' : 'string',
                        'required' : True
                    }],
                    'methods' : [
                    'GET'
                    ],
                    'embed_url' : 'https://vidmoly.net/embed-v7ad0oiawrdv.html',
                    'example' : f'{BASE_API}/vidmoly?url=https://vidmoly.net/embed-v7ad0oiawrdv.html',
                    'example_return' : {
                        'source': f'{BASE_API}/vidmoly-proxy?url=https%3A//prx-1351-ant-20.vmwesa.online/hls2/01/02135/v7ad0oiawrdv_%2Cl%2Cn%2C.urlset/master.m3u8%3Ft%3DUl5yp3W6T68EVKi6ubYC8WqwvOAPeqnw5V0mJ2016iU%26s%3D1768757400%26e%3D43200%26v%3D%26srv%3Dres-v3i-s4%26i%3D0.4%26sp%3D0%26asn%3D47377',
                        'status': 'success'
                    },
                },
                '/callistanise' : {
                    'description': 'Extraction HLS pour Callistanise (Dingtezuni).',
                    'parameter' : [{
                        'name' : 'url',
                        'type' : 'string',
                        'required' : True
                    }],
                    'methods' : [
                    'GET'
                    ],
                    'embed_url' : 'https://dingtezuni.com/embed/fdbfypeipkyc',
                    'allowed_url' : [
                        'https://callistanise.com',
                        'https://Smoothpre.com',
                        'https://dingtezuni.com',
                        'https://movearnpre.com',
                        'https://minochinos.com',
                    ],
                    'example' : f'{BASE_API}/callistanise?url=https://dingtezuni.com/embed/fdbfypeipkyc',
                    'example_return' : {
                        'source': f'{BASE_API}/callistanise-proxy?url=https%3A//RNzT2t4XVKU08.marineridgemediaworks.cyou/Z8VeXJnplmoxw/hls3/01/07116/fdbfypeipkyc_%2Cl%2Cn%2Ch%2C.urlset/master.txt',
                        'status': 'success'
                    },
                },
                '/embed4me' : {
                    'description': 'Extraction pour Embed4me / Lplayer via ID.',
                    'parameter' : [{
                        'name' : 'id',
                        'type' : 'string',
                        'required' : True
                    }],
                    'methods' : [
                    'GET'
                    ],
                    'embed_url' : 'https://lpayer.embed4me.com/#xv8jw',
                    'example' : f'{BASE_API}/embed4me?id=xv8jw',
                    'example_return' : {
                        'ip_source': f'{BASE_API}/embed4me-proxy?url=https%3A//185.237.106.184/v4/_R-ZYkSpoB8Z3LbO1WJ5Iw/1768767781/ck/xv8jw/master.m3u8%3Fv%3D1768734497',
                        'source': f'{BASE_API}/embed4me-proxy?url=https%3A//s6d.servicecatalog.site/v4/ck/xv8jw/cf-master.1768734497.txt',
                        'status': 'success'
                    },
                },
                '/vk' : {
                    'description': 'Extraction pour vk / vk-video-player via id et oid.',
                    'parameter' : [{
                        'name' : 'url',
                        'type' : 'string',
                        'required' : True
                    }],
                    'methods' : [
                    'GET'
                    ],
                    'embed_url' : 'https://vk.com/video_ext.php?oid=755747641&id=456240670',
                    'example' : f'{BASE_API}/vk?url=https://vk.com/video_ext.php?oid=755747641&id=456240670',
                    'example_return' : {
                        'source': f'{BASE_API}/vk-proxy?url=https%3A//vkvd423.okcdn.ru/%3FsrcIp%3D94.106.215.122%26pr%3D40%26expires%3D1769306933789%26srcAg%3DCHROME%26fromCache%3D1%26ms%3D45.136.21.154%26type%3D3%26sig%3DFz-c09UdgPM%26ct%3D0%26urls%3D185.226.52.132%26clientType%3D13%26appId%3D512000384397%26zs%3D65%26id%3D5804617632313',
                        'status': 'success'
                    },
                },
                '/vidoza' : {
                    'description': 'Extraction pour vidoza / via url.',
                    'parameter' : [{
                        'name' : 'url',
                        'type' : 'string',
                        'required' : True
                    }],
                    'methods' : [
                    'GET'
                    ],
                    'embed_url' : 'https://videzz.net/embed-9b6zbu7135u0.html',
                    'example' : f'{BASE_API}/vidoza?url=https://videzz.net/embed-9b6zbu7135u0.html',
                    'example_return' : {
                        'source': f'{BASE_API}/vidoza-proxy?url=https%3A//str41.vidoza.net/vod/v2/nvl4h6wfjefeieno3xqdxbx5phjpc6c3ol75c7arjbwthfys3hidlod5y6adtypjuy/v.mp4',
                        'status': 'success'
                    },
                },
                '/doodstream' : {
                    'description': 'Extraction pour doodstream / via url et d0000d.',
                    'parameter' : [{
                        'name' : 'url',
                        'type' : 'string',
                        'required' : True
                    }],
                    'methods' : [
                    'GET'
                    ],
                    'embed_url' : 'https://d0000d.com/e/x84gtg15zdr0',
                    'example' : f'{BASE_API}/doodstream?url=https://d0000d.com/e/x84gtg15zdr0',
                    'example_return' : {
                        'source': f'{BASE_API}/doodstream-proxy?url=https%3A//ior159p.cloudatacdn.com/u5kjwffw4tb3sdgge6ankjaods6tjmytb2n4lpmrrjw4jd3q5l6d6owxopmq/3tkh59jgio~a1fSlE38xB%3Ftoken%3Dp0okvsj2ildu0xxz4ubvd7rn%26expiry%3D1768868131723',
                        'status': 'success'
                    },
                },
                '/voe' : {
                    'description': 'Extraction pour vode / via url.',
                    'parameter' : [{
                        'name' : 'url',
                        'type' : 'string',
                        'required' : True
                    }],
                    'methods' : [
                    'GET'
                    ],
                    'embed_url' : 'https://voe.sx/e/llwq1wy1qfye',
                    'example' : f'{BASE_API}/voe?url=https://voe.sx/e/llwq1wy1qfye',
                    'example_return' : {
                        'source': f'{BASE_API}/voe-proxy?url=https%3A//cdn-e4srqqyuolvqfr5r.edgeon-bandwidth.com/engine/download/01/15930/sghn1bhjll5t_n.mp4%3Ft%3DoyQSr8hA7IN4pmPA7k_GBfxF5y5wcnX2qFmLf-5rbiQ%26s%3D1768869723%26e%3D14400%26f%3D79671350%26node%3DY0KHGfl9QQsG/hnJQy4YMlg5PipBN8Q9%2B7i/ywA/hFo%3D%26i%3D94.106%26sp%3D380%26asn%3D47377%26n%3DMaxton.Hall.The.World.Between.Us.S02E06.FINAL.MULTI.1080p.WEB.H264-HiggsBoson-1_.mp4%26d%3D1',
                        'status': 'success'
                    },
                },
                'proxies_info' : {
                'description': 'Tous les proxies (/voe-proxy, /vidoza-proxy, /doodstream-proxy, /vidmoly-proxy, /vk-proxy, /callistanise-proxy, /embed4me-proxy) acceptent un paramètre \'url\' encodé et retournent le flux vidéo ou le fichier m3u8 réécrit.',
                    'parameter' : [{
                        'name' : 'url',
                        'type' : 'string',
                        'required' : True
                    }],
                    'methods' : [
                    'GET'
                    ],
                    'example' : f'{BASE_API}/embed4me-proxy?url=https%3A//s6d.servicecatalog.site/v4/ck/xv8jw/cf-master.1768734497.txt',
                    'example_return' : 'Binary data (video/mp2t), Text (application/vnd.apple.mpegurl) or video file',
                },
            }
        }), 200

# vidmoly START
@app.route('/vidmoly', methods=['GET'])
def get_vidmoly_m3u8():
    url = request.args.get('url')
    if not url:
        return jsonify({"error": "URL manquante"}), 400

    try:
        with sync_playwright() as p:
            browser = p.chromium.launch(headless=True)
            context = browser.new_context(user_agent=random.choice(USER_AGENTS))
            page = context.new_page()
            stealth_sync(page)

            adblock_msg = page.locator("#adsblock")
            # Fermer les popups de pub automatiquement
            context.on("page", lambda p: p.close())

            # 1. Charger l'embed initial
            page.goto(url, wait_until='networkidle')
            page.wait_for_timeout(1500) # Sécurité anti-bot

            if not adblock_msg:
                try:
                    # 2. Cliquer sur le bouton Play
                    selector = 'div.play-button'
                    page.wait_for_selector(selector)

                    # On clique et on attend que l'URL change (redirection vers ?g=...)
                    with page.expect_navigation(timeout=10000):
                        page.click(selector, force=True)

                except Exception as e:
                        logger.error(f"Error: {e}")

            # 3. Extraire le lien .m3u8 du code source de la NOUVELLE page
            html_content = page.content()
            # Regex identique à ton PHP pour trouver le fichier .m3u8
            pattern = r'file\s*:\s*["\'](https?://[^"\']+\.m3u8[^"\']*)["\']'
            match = re.search(pattern, html_content)

            if match:
                m3u8_url = match.group(1)
                browser.close()
                proxy_base = f"{BASE_API}/vidmoly-proxy?url="
                return jsonify({
                    "status": "success",
                    "source": f"{proxy_base}{quote(m3u8_url)}"
                })
            else:
                browser.close()
                return jsonify({"error": "Fichier .m3u8 non trouvé dans le code source"}), 404

    except Exception as e:
        return jsonify({"error": str(e)}), 500

# vidmoly
@app.route('/vidmoly-proxy')
def vidmoly_proxy():
    target_url = request.args.get('url')
    if not target_url:
        return "URL manquante", 400

    # Décodage de l'URL cible (car elle arrive encodée par quote)
    target_url = unquote(target_url)

    try:
        # Headers identiques à votre extractM3U8Vidmoly PHP
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/130.0.0.0 Safari/537.36',
            'Accept': '*/*',
            'Accept-Language': 'fr-BE,fr-FR;q=0.9,fr;q=0.8,en-US;q=0.7,en;q=0.6,ru;q=0.5',
            'Referer': 'https://vidmoly.net/',
            'Origin': 'https://vidmoly.net',
            'Connection': 'keep-alive',
            'DNT': '1'
        }

        # Gestion du Range header envoyé par le lecteur vidéo
        range_header = request.headers.get('Range', None)
        if range_header:
            headers['Range'] = range_header

        # Requête vers Vidmoly
        resp = requests.get(target_url, headers=headers, timeout=20, stream=True, verify=False)

        # CAS 1 : C'est un Manifest M3U8
        if ".m3u8" in target_url or "mpegurl" in resp.headers.get('Content-Type', '').lower():
            content = resp.text
            new_lines = []
            # On utilise l'URL actuelle du proxy pour le préfixage
            proxy_base = f"{BASE_API}/vidmoly-proxy?url="

            for line in content.splitlines():
                line = line.strip()
                if not line: continue

                # Remplacement des URI dans les tags (ex: #EXT-X-KEY:URI="...")
                if 'URI=' in line:
                    line = re.sub(r'URI=(["\'])(.+?)\1',
                         lambda m: f'URI={m.group(1)}{proxy_base}{quote(urljoin(target_url, m.group(2)))}{m.group(1)}',
                         line)
                    new_lines.append(line)
                elif line.startswith('#'):
                    new_lines.append(line)
                else:
                    # Remplacement des URLs de segments ou sous-playlists
                    abs_url = urljoin(target_url, line)
                    new_lines.append(f"{proxy_base}{quote(abs_url)}")

            return Response(
                "\n".join(new_lines),
                mimetype='application/vnd.apple.mpegurl',
                headers={
                    "Access-Control-Allow-Origin": "*",
                    "Content-Disposition": 'inline; filename="playlist.m3u8"'
                }
            )

        # CAS 2 : C'est un segment binaire (.ts)
        # On utilise un générateur pour supporter les Range Requests et le streaming
        def generate():
            for chunk in resp.iter_content(chunk_size=8192):
                yield chunk

        # On recopie les headers importants du serveur original (Content-Range, Content-Length)
        excluded_headers = ['content-encoding', 'content-length', 'transfer-encoding', 'connection']
        proxy_headers = [(name, value) for (name, value) in resp.raw.headers.items()
                         if name.lower() not in excluded_headers]
        proxy_headers.append(("Access-Control-Allow-Origin", "*"))
        proxy_headers.append(("X-Content-Type-Options", "nosniff"))

        return Response(
            generate(),
            status=resp.status_code,
            mimetype='video/mp2t',
            headers=proxy_headers
        )

    except Exception as e:
        return f"Erreur Proxy Vidmoly: {str(e)}", 500
# vidmoly END

# callistanise START
def unpack_js_for_ts_file(packed_code, base, count, words):
    def to_base(num, base):
        if num == 0:
            return '0'
        digits = []
        while num:
            digits.append(str(num % base) if num % base < 10 else chr(ord('a') + num % base - 10))
            num //= base
        return ''.join(reversed(digits))

    replacements = {to_base(i, base): words[i] for i in range(count) if i < len(words) and words[i]}
    unpacked = packed_code
    for key, value in replacements.items():
        pattern = r'\b' + re.escape(key) + r'\b'
        unpacked = re.sub(pattern, value, unpacked)

    return unpacked

# callistanise
def extract_hls_url(unpacked_code):
    # 1. Tentative d'extraction depuis la variable JS 'links' (hls2, hls3 ou hls4)
    # On cherche hls4 d'abord, puis hls3, puis hls2 (ordre de qualité/priorité souvent utilisé)
    for key in ['hls4', 'hls3', 'hls2']:
        pattern = r'["\']' + key + r'["\']\s*:\s*["\'](https?://[^"\']+)["\']'
        match = re.search(pattern, unpacked_code)
        if match:
            return match.group(1)

    # 2. Fallback : Ancien pattern si le premier a échoué
    pattern_fallback = r'["\'](/stream/[^"\']*/master\.m3u8[^"\']*)["\']'
    match_fallback = re.search(pattern_fallback, unpacked_code)
    if match_fallback:
        return match_fallback.group(1)

    print("No matching HLS URL found in unpacked code.")
    return None

# callistanise
@app.route('/callistanise', methods=['GET'])
def get_callistanise_m3u8():
    url = request.args.get('url')

    if not url:
        return jsonify({"error": "URL manquante"}), 400

    try:
        # Determine base URL for relative paths
        url_parts = url.split('/')
        url_start = f"{url_parts[0]}//{url_parts[2]}" # e.g., https://domain.com

        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/129.0.0.0 Safari/537.36',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
            'Referer': url.split('/embed/')[0] if '/embed/' in url else url,
        }

        response = requests.get(url, headers=headers, timeout=10)
        response.raise_for_status()
        html_content = response.text

        # 1. Look for Dean Edwards Packer code
        pattern = r"eval\(function\(p,a,c,k,e,d\)\{.*?\}\('(.*?)',(\d+),(\d+),'(.*?)'\.split\('\|'\)\)\)"
        match = re.search(pattern, html_content, re.DOTALL)

        if match:
            packed_code, base, count, words = match.group(1), int(match.group(2)), int(match.group(3)), match.group(4).split('|')
            unpacked_code = unpack_js_for_ts_file(packed_code, base, count, words)

            #return jsonify({
            #    "status": "success",
            #    "unpacked_code": unpacked_code
            #})

            # 2. Extract HLS URL from the unpacked script (Corrected Indentation)
            hls_url = extract_hls_url(unpacked_code)

            if hls_url:
                if hls_url.startswith('http'):
                    final_source = hls_url
                else:
                    final_source = url_start + hls_url

                proxy_base = f"{BASE_API}/callistanise-proxy?url="
                return jsonify({
                    "status": "success",
                    "source": f"{proxy_base}{quote(final_source)}"
                })

            return jsonify({"error": "HLS URL not found in unpacked code"}), 404

        return jsonify({"error": "No packed JavaScript code found"}), 404

    except requests.exceptions.RequestException as e:
        return jsonify({"error": str(e)}), 500

# callistanise
@app.route('/callistanise-proxy')
def callistanise_proxy():
    target_url = request.args.get('url')
    if not target_url:
        return "URL manquante", 400

    try:
        # Headers nécessaires pour que le serveur de stream accepte la requête
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36',
            'Referer': 'https://callistanise.com/',
            'Origin': 'https://callistanise.com'
        }

        resp = requests.get(target_url, headers=headers, timeout=15)
        resp.raise_for_status()

        # Si c'est une playlist M3U8, on réécrit les liens
        if "#EXTM3U" in resp.text:
            content = resp.text
            new_lines = []
            proxy_base = f"{BASE_API}/callistanise-proxy?url="

            for line in content.splitlines():
                line = line.strip()
                if not line: continue

                # Si la ligne commence par #, c'est un tag (sauf cas particulier comme EXT-X-MAP)
                if line.startswith('#'):
                    # Gestion du fichier d'initialisation si présent
                    if line.startswith('#EXT-X-MAP:URI='):
                        match = re.search(r'URI="([^"]+)"', line)
                        if match:
                            abs_uri = urljoin(target_url, match.group(1))
                            line = f'#EXT-X-MAP:URI="{proxy_base}{quote(abs_uri)}"'
                    new_lines.append(line)
                else:
                    # C'est un segment (.ts) ou une sous-playlist (.m3u8)
                    # urljoin gère automatiquement les chemins relatifs ou absolus
                    abs_url = urljoin(target_url, line)
                    new_lines.append(f"{proxy_base}{quote(abs_url)}")

            return Response(
                "\n".join(new_lines),
                mimetype='application/vnd.apple.mpegurl',
                headers={"Access-Control-Allow-Origin": "*"}
            )

        # Si c'est un segment binaire (TS), on renvoie le contenu brut
        return Response(
            resp.content,
            mimetype=resp.headers.get('Content-Type'),
            headers={"Access-Control-Allow-Origin": "*"}
        )

    except Exception as e:
        return f"Erreur Proxy: {str(e)}", 500
# callistanise END

# embed4me START
KEY = b"kiemtienmua911ca"
IV = b"1234567890oiuytr"

def _decrypt_data(hex_str):
    try:
        hex_str = hex_str.strip().replace('"', '')
        data = binascii.unhexlify(hex_str)
        cipher = AES.new(KEY, AES.MODE_CBC, IV)
        decrypted = unpad(cipher.decrypt(data), AES.block_size)
        return decrypted.decode('utf-8')
    except Exception as e:
        print(f"Erreur de déchiffrement : {e}")
        return None

# embed4me
@app.route('/embed4me', methods=['GET'])
def extract_embed4me_video_source():
    # On récupère l'ID depuis la requête

    video_id = request.args.get('id')
    api_url = f"https://lpayer.embed4me.com/api/v1/video?id={video_id}&w=1920&h=1080&r="
    headers = get_headers() # Utilise ta fonction de headers déjà définie

    try:
        r = requests.get(api_url, headers=headers, timeout=10)
        if r.status_code != 200:
            return jsonify({"status": "error", "message": f"Erreur API: {r.status_code}"}), 400

        decrypted_raw = _decrypt_data(r.text)

        if decrypted_raw:
            data = json.loads(decrypted_raw)

            # --- Extraction et construction des URLs proxy ---
            # On récupère les URLs brutes
            raw_cf = data.get('cf', '')
            raw_source = data.get('source', '')

            # On prépare le préfixe du proxy (encodé pour la sécurité)
            proxy_base = f"{BASE_API}/embed4me-proxy?url="

            # On assemble le tout
            return jsonify({
                "status": "success",
                "source": f"{proxy_base}{quote(raw_cf)}",
                "ip_source": f"{proxy_base}{quote(raw_source)}",
            })
        else:
            return jsonify({"status": "error", "message": "Échec du déchiffrement AES"}), 500

    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 500

# embed4me
def get_headers():
    return {
        'User-Agent': USER_AGENTS[0],
        'Accept': '*/*',
        'Accept-Language': 'en-US,en;q=0.5',
        'Referer': 'https://lpayer.embed4me.com/',
        'Origin': 'https://lpayer.embed4me.com',
    }

# embed4me
@app.route('/embed4me-proxy')
def proxy():
    target_url = request.args.get('url')
    if not target_url:
        return "URL manquante", 400

    try:
        resp = requests.get(target_url, headers=get_headers(), timeout=15, verify=False)
        resp.raise_for_status()

        if "#EXTM3U" in resp.text:
            content = resp.text
            new_lines = []
            proxy_base = f"{BASE_API}/embed4me-proxy?url="

            for line in content.splitlines():
                line = line.strip()
                if not line: continue

                # 1. Traitement de la balise EXT-X-MAP (Fichier d'initialisation)
                if line.startswith('#EXT-X-MAP:URI='):
                    # On extrait l'URL entre les guillemets
                    match = re.search(r'URI="([^"]+)"', line)
                    if match:
                        raw_uri = match.group(1)
                        abs_uri = urljoin(target_url, raw_uri)
                        proxified_uri = f'{proxy_base}{quote(abs_uri)}'
                        # On reconstruit la ligne avec l'URL proxyfiée
                        line = f'#EXT-X-MAP:URI="{proxified_uri}"'
                    new_lines.append(line)

                # 2. Traitement des segments standards (lignes sans #)
                elif not line.startswith('#'):
                    abs_url = urljoin(target_url, line)
                    proxified_url = f"{proxy_base}{quote(abs_url)}"
                    new_lines.append(proxified_url)

                # 3. On garde les autres tags (#EXTINF, etc.) tels quels
                else:
                    new_lines.append(line)

            return Response(
                "\n".join(new_lines),
                mimetype='application/vnd.apple.mpegurl',
                headers={"Access-Control-Allow-Origin": "*"}
            )

        return Response(
            resp.content,
            mimetype=resp.headers.get('Content-Type'),
            headers={"Access-Control-Allow-Origin": "*"}
        )

    except Exception as e:
        return f"Erreur Proxy: {str(e)}", 500
# embed4me END

# vk START
@app.route('/vk', methods=['GET'])
def extract_vk_video_source():
    url = request.url.split('?url=')[1]

    if not url:
        return jsonify({"error": "URL manquante"}), 400

    try:
        with sync_playwright() as p:
            browser = p.chromium.launch(headless=True)
            context = browser.new_context(user_agent=random.choice(USER_AGENTS))
            page = context.new_page()

            page.goto(url)
            html_content = page.content()
            browser.close()

            # --- ETAPE 1 : Isoler uniquement le bloc "files" ---
            # On cherche ce qui est entre "files":{ et },"trailer"
            files_block_match = re.search(r'"files":\{(.*?)\},"trailer"', html_content)

            if not files_block_match:
                return jsonify({"error": "Bloc de fichiers introuvable"}), 404

            files_content = files_block_match.group(1)

            # --- ETAPE 2 : Extraire les MP4 depuis ce bloc uniquement ---
            pattern = r'"mp4_(\d+)":"([^"]+)"'
            matches = re.findall(pattern, files_content)

            if not matches:
                return jsonify({"error": "Aucun flux MP4 complet trouvé"}), 404

            # 3. Création du dictionnaire {720: "url", 1080: "url"}
            video_sources = {}
            for quality, raw_url in matches:
                clean_url = raw_url.replace(r'\/', '/')
                # On utilise ton proxy pour contourner les restrictions d'IP
                video_sources[int(quality)] = f"{BASE_API}/vk-proxy?url={quote(clean_url)}"

            # 4. Filtrage : On ne garde que ce qui est <= 720
            qualities_under_720 = [q for q in video_sources.keys() if q <= 720]

            if not qualities_under_720:
                # Au cas où seule la 1080p existerait (rare sur VK)
                # on prend la plus basse disponible par sécurité
                selected_quality = min(video_sources.keys())
            else:
                # On prend la plus haute parmi celles qui respectent la limite
                selected_quality = max(qualities_under_720)

            final_url = video_sources[selected_quality]

            return jsonify({
                "status": "success",
                "source": final_url
            }), 200

    except Exception as e:
        return jsonify({"error": str(e)}), 500

# vk

@app.route('/vk-proxy')
def vk_proxy():
    # Récupération de l'URL cible (doit être encodée dans l'appel)
    target_url = request.args.get('url')
    if not target_url:
        return "URL manquante", 400

    # On prépare les headers à envoyer à VK
    # On imite un navigateur et on transmet le header 'Range' si présent
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
        'Referer': 'https://vk.com/',
    }

    # Très important pour le streaming : on transmet le 'Range' du lecteur vidéo
    if 'Range' in request.headers:
        headers['Range'] = request.headers['Range']

    try:
        # On fait la requête avec stream=True pour ne pas charger le fichier en RAM
        req = requests.get(target_url, headers=headers, stream=True, timeout=15)

        # On définit une fonction génératrice pour envoyer les chunks
        def generate():
            for chunk in req.iter_content(chunk_size=8192):
                yield chunk

        # On renvoie la réponse avec le bon code (200 ou 206) et les bons headers
        response = Response(
            stream_with_context(generate()),
            status=req.status_code,
            content_type=req.headers.get('content-type')
        )

        # On transmet les headers critiques pour la vidéo
        critical_headers = ['Content-Range', 'Content-Length', 'Accept-Ranges']
        for header in critical_headers:
            if header in req.headers:
                response.headers[header] = req.headers[header]

        # CORS headers pour éviter les blocages navigateurs
        response.headers['Access-Control-Allow-Origin'] = '*'

        return response

    except Exception as e:
        return f"Erreur Proxy: {str(e)}", 500
# vk END

# vidoza START
VIDOZA_PATTERN = re.compile(r'<source\s+src="(?P<url>[^"]+)"')

def extract_vidoza(html_content):
    """Extrait le lien direct MP4 de Vidoza via Regex."""
    match = VIDOZA_PATTERN.search(html_content)
    return match.group("url") if match else None
# vidoza
@app.route('/vidoza')
async def vidoza_scraper():
    url = request.args.get('url')
    if not url: return jsonify({"error": "URL manquante"}), 400

    try:
        # Pour Vidoza, une simple requête GET suffit souvent
        resp = requests.get(url, timeout=10)
        video_url = extract_vidoza(resp.text)

        if video_url:
            # Proxying automatique
            proxy_url = f"{request.host_url}vidoza-proxy?url={quote(video_url)}"
            return jsonify({"source": proxy_url, "status": "success"})
        return jsonify({"error": "Vidéo non trouvée"}), 404
    except Exception as e:
        return jsonify({"error": str(e)}), 500

# vidoza
@app.route('/vidoza-proxy')
def vidoza_proxy():
    video_url = unquote(request.args.get('url'))
    if not video_url:
        return "URL manquante", 400

    # On récupère le header Range envoyé par le navigateur (ex: bytes=0-1024)
    range_header = request.headers.get('Range', None)

    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36',
        'Referer': 'https://vidoza.net/'
    }
    if range_header:
        headers['Range'] = range_header

    try:
        # stream=True est indispensable pour ne pas charger le MP4 en RAM
        resp = requests.get(video_url, headers=headers, stream=True, timeout=15)

        # On prépare la réponse Flask en transmettant les headers importants
        excluded_headers = ['content-encoding', 'content-length', 'transfer-encoding', 'connection']
        proxy_headers = [
            (name, value) for (name, value) in resp.raw.headers.items()
            if name.lower() not in excluded_headers
        ]

        def generate():
            for chunk in resp.iter_content(chunk_size=128 * 1024): # Segments de 128kb
                yield chunk

        return Response(
            generate(),
            status=resp.status_code,
            headers=proxy_headers,
            content_type=resp.headers.get('Content-Type')
        )

    except Exception as e:
        return str(e), 500
# vidoza END

# doodstream START
DOODSTREAM_PATTERN = re.compile(r"/pass_md5/[\w-]+/(?P<token>[\w-]+)")
def extract_doodstream(html_content, original_url):
    """Logique robuste pour Doodstream."""
    # Extraire le domaine (ex: doodstream.com ou d0000d.com)
    parsed_url = urlsplit(original_url)
    domain = f"{parsed_url.scheme}://{parsed_url.netloc}"

    pattern_match = DOODSTREAM_PATTERN.search(html_content)
    if not pattern_match:
        return None

    pass_md5_url = pattern_match.group(0)
    token = pattern_match.group("token")

    headers = {
        'Referer': domain,
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
    }

    # Appel avec verify=False pour éviter l'erreur SSL
    response = requests.get(f"{domain}{pass_md5_url}", headers=headers, verify=False)
    base_url = response.text

    random_str = ''.join(choices(ascii_letters + digits, k=10))
    expiry = int(time() * 1000)

    return f"{base_url}{random_str}?token={token}&expiry={expiry}"

# doodstream
@app.route('/doodstream')
async def doodstream_scraper():
    url = request.args.get('url')
    if not url: return jsonify({"error": "URL manquante"}), 400

    try:
        # Ajout de verify=False ici aussi
        resp = requests.get(url, headers={'Referer': 'https://d0000d.com/'}, verify=False)
        video_url = extract_doodstream(resp.text, url) # On passe 'url' ici

        if video_url:
            proxy_url = f"{request.host_url}doodstream-proxy?url={quote(video_url)}"
            return jsonify({"source": proxy_url, "status": "success"})
        return jsonify({"error": "Extraction échouée"}), 404
    except Exception as e:
        return jsonify({"error": str(e)}), 500
# doodstream

@app.route('/doodstream-proxy')
def video_proxy():
    # 1. Récupération et décodage de l'URL cible
    video_url = unquote(request.args.get('url'))
    if not video_url:
        return jsonify({"error": "URL manquante"}), 400

    # 2. Préparation des Headers pour l'hébergeur
    # On récupère le header 'Range' du navigateur s'il existe
    range_header = request.headers.get('Range', None)

    referer = "https://d0000d.com/"

    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
        'Referer': referer,
        'Connection': 'keep-alive'
    }

    if range_header:
        headers['Range'] = range_header

    try:
        # 3. Requête vers l'hébergeur avec stream=True (très important pour le MP4)
        # verify=False car Doodstream a souvent des soucis de certificats sur ses CDNs
        resp = requests.get(video_url, headers=headers, stream=True, timeout=15, verify=False)

        # 4. Transmission des headers de réponse (Content-Type, Content-Range, etc.)
        excluded_headers = ['content-encoding', 'content-length', 'transfer-encoding', 'connection']
        proxy_headers = [
            (name, value) for (name, value) in resp.raw.headers.items()
            if name.lower() not in excluded_headers
        ]

        # 5. Générateur pour streamer le contenu par morceaux (chunks)
        def generate():
            for chunk in resp.iter_content(chunk_size=256 * 1024): # Morceaux de 256 Ko
                yield chunk

        return Response(
            generate(),
            status=resp.status_code,
            headers=proxy_headers,
            content_type=resp.headers.get('Content-Type', 'video/mp4')
        )

    except Exception as e:
        return jsonify({"error": str(e)}), 500
# doodstream END

# voe START

def voe_rot13(text):
    return codecs.encode(text, 'rot_13')

# voe
def voe_replace_patterns(text):
    patterns = ['@$', '^^', '~@', '%?', '*~', '!!', '#&']
    for p in patterns:
        text = text.replace(p, '')
    return text

# voe
def voe_safe_base64_decode(encoded_str):
    # Ajout du padding automatique si nécessaire
    missing_padding = len(encoded_str) % 4
    if missing_padding:
        encoded_str += '=' * (4 - missing_padding)
    return base64.b64decode(encoded_str).decode('utf-8', errors='ignore')

# voe
def voe_shift_chars(text, shift):
    return ''.join(chr(ord(c) - shift) for c in text)

# voe
def deobfuscate_voe_json(raw_json_text):
    try:
        data = json.loads(raw_json_text)
        if not data or not isinstance(data, list) or not data[0]:
            return None

        obfuscated = data[0]

        # Le processus en 6 étapes (ton PHP adapté)
        step1 = voe_rot13(obfuscated)
        step2 = voe_replace_patterns(step1)
        step3 = voe_safe_base64_decode(step2)
        step4 = voe_shift_chars(step3, 3)
        step5 = step4[::-1]  # Reverse string
        step6 = voe_safe_base64_decode(step5)

        try:
            return json.loads(step6)
        except:
            return step6 # Si c'est une string brute
    except Exception as e:
        return None

# voe
@app.route('/voe')
async def voe_scraper():
    url = request.args.get('url')
    if not url:
        return jsonify({"error": "missing url"}), 400

    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36',
        'Referer': 'https://voe.sx/'
    }

    try:
        # 1. Récupération HTML
        response = requests.get(url, headers=headers, timeout=15)
        html = response.text

        # 2. Détection redirection JS (Regex pour remplacer detectJsRedirect)
        js_redir_pattern = re.compile(r'window\.location\.href\s*=\s*["\']([^"\']+)', re.I)
        match_redir = js_redir_pattern.search(html)
        if match_redir:
            new_url = match_redir.group(1)
            # Appel récursif (simple redirection HTTP ici)
            response = requests.get(new_url, headers=headers, timeout=15)
            html = response.text

        # 3. Extraction Method 8 (JSON obfusqué)
        # On cherche tous les <script type="application/json">
        json_scripts = re.findall(r'<script type="application/json">(.*?)</script>', html, re.S)

        source_found = None
        for script_content in json_scripts:
            result = deobfuscate_voe_json(script_content.strip())

            if result and isinstance(result, dict):
                source_url = result.get('direct_access_url') or result.get('source')
                if source_url:
                    source_found = source_url
                    break

        if not source_found:
            return jsonify({"error": "source_not_found"}), 404

        # 4. Retourner le résultat (Pas besoin de proxy pour VOE en général, mais optionnel)
        proxy_url = f"{request.host_url}voe-proxy?url={quote(source_found)}"
        return jsonify({
            "source": proxy_url,
            "status": "success"
        })

    except Exception as e:
        return jsonify({"error": str(e)}), 500

# voe
@app.route('/voe-proxy')
def voe_proxy():
    video_url = unquote(request.args.get('url', ''))
    if not video_url:
        return "URL manquante", 400

    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36',
        'Referer': 'https://voe.sx/'
    }

    range_header = request.headers.get('Range')
    if range_header:
        headers['Range'] = range_header

    try:
        resp = requests.get(video_url, headers=headers, stream=True, timeout=15, verify=False)

        # CAS 1 : HLS (.m3u8)
        if ".m3u8" in video_url:
            content = resp.text
            base_url = video_url.rsplit('/', 1)[0]
            lines = content.split('\n')
            new_lines = []
            for line in lines:
                line = line.strip()
                if not line: continue
                if line.endswith('.ts') or '.ts?' in line:
                    segment_url = line if line.startswith('http') else f"{base_url}/{line}"
                    new_lines.append(f"{request.host_url}voe-proxy?url={quote(segment_url)}")
                else:
                    new_lines.append(line)

            # Forcer le type MIME pour HLS
            return Response('\n'.join(new_lines), content_type='application/vnd.apple.mpegurl')

        # CAS 2 : MP4 ou Segment TS
        excluded_headers = ['content-encoding', 'content-length', 'transfer-encoding', 'connection', 'content-disposition']
        proxy_headers = [(n, v) for (n, v) in resp.raw.headers.items() if n.lower() not in excluded_headers]

        # On force le Content-Type si c'est un MP4 pour éviter le téléchargement
        final_content_type = resp.headers.get('Content-Type')
        if ".mp4" in video_url:
            final_content_type = 'video/mp4'
        elif ".ts" in video_url:
            final_content_type = 'video/mp2t'

        # CRUCIAL : On s'assure que 'inline' est utilisé et non 'attachment'
        proxy_headers.append(('Content-Disposition', 'inline'))
        # Autoriser le CORS pour que les lecteurs web (JWPlayer, Video.js) puissent lire
        proxy_headers.append(('Access-Control-Allow-Origin', '*'))

        return Response(
            resp.iter_content(chunk_size=512 * 1024),
            status=resp.status_code,
            headers=proxy_headers,
            content_type=final_content_type
        )

    except Exception as e:
        return str(e), 500
# voe END
if __name__ == '__main__':
    app.run(host='127.0.0.1', port=8888, debug=True)
