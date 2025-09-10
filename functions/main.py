"""
姓名判断アプリ - GCP Functions メインハンドラー
jamdict + KanjiDic2を使用した康熙字典準拠の姓名判断API
"""

import json
import logging
import threading
import time
from collections import defaultdict
from typing import Dict, List, Optional, Tuple
from flask import Flask, request, jsonify
from flask_cors import CORS
import functions_framework
from jamdict import Jamdict

# ロギング設定
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# グローバル変数（Functions起動時に1度だけ初期化）
jam = None
gogaku_rules = None
hiragana_strokes = None

# スレッドローカルストレージ
thread_local = threading.local()

# セキュリティ関連変数
request_tracker = defaultdict(list)

def initialize_dictionaries():
    """辞書データの初期化（Functions起動時に1度だけ実行）"""
    global jam, gogaku_rules, hiragana_strokes
    
    if jam is None:
        logger.info("📚 jamdict辞書を初期化中...")
        jam = Jamdict()
        logger.info("✅ jamdict辞書初期化完了")
    
    if gogaku_rules is None:
        logger.info("📊 五格説判定ルールを読込中...")
        # 既存の五格説ルールファイルを読込
        try:
            with open('gogaku_judgment.json', 'r', encoding='utf-8') as f:
                gogaku_rules = json.load(f)
            logger.info("✅ 五格説ルール読込完了")
        except FileNotFoundError:
            # ファイルが見つからない場合はコード内に埋め込み
            gogaku_rules = get_embedded_gogaku_rules()
            logger.info("✅ 埋め込み五格説ルール使用")
    
    if hiragana_strokes is None:
        logger.info("🔤 ひらがな画数データを読込中...")
        try:
            with open('hiragana_strokes.json', 'r', encoding='utf-8') as f:
                hiragana_data = json.load(f)
                hiragana_strokes = hiragana_data.get('hiragana_dictionary', {})
            logger.info("✅ ひらがな画数データ読込完了")
        except FileNotFoundError:
            # ファイルが見つからない場合はコード内に埋め込み
            hiragana_strokes = get_embedded_hiragana_strokes()
            logger.info("✅ 埋め込みひらがな画数データ使用")

def basic_security_check(request):
    """基本的なセキュリティチェック（Phase A対策）"""
    client_ip = request.environ.get('HTTP_X_FORWARDED_FOR', 
                                   request.environ.get('REMOTE_ADDR', 'unknown'))
    
    # 1. リファラー/オリジンチェック
    origin = request.headers.get('Origin', '')
    referer = request.headers.get('Referer', '')
    allowed_origins = [
        'https://storage.googleapis.com',
        'http://localhost:3000',  # 開発環境用
        'http://localhost:8080'   # ローカルテスト用
    ]
    
    # オリジンまたはリファラーが存在する場合のみチェック
    if origin:
        if not any(allowed_origin in origin for allowed_origin in allowed_origins):
            logger.warning(f"🚨 不正なオリジン: {origin} from IP: {client_ip}")
            return False, "アクセスが拒否されました"
    
    if referer and not origin:  # オリジンがない場合はリファラーをチェック
        if not any(allowed_origin in referer for allowed_origin in allowed_origins):
            logger.warning(f"🚨 不正なリファラー: {referer} from IP: {client_ip}")
            return False, "アクセスが拒否されました"
    
    # 2. シンプルレート制限（1分間に10リクエスト）
    now = time.time()
    request_tracker[client_ip] = [
        timestamp for timestamp in request_tracker[client_ip]
        if timestamp > now - 60  # 1分以内のリクエストのみ保持
    ]
    
    if len(request_tracker[client_ip]) >= 10:
        logger.warning(f"🚨 レート制限超過: IP {client_ip} ({len(request_tracker[client_ip])} requests)")
        return False, "リクエスト頻度が高すぎます。しばらく待ってから再試行してください"
    
    request_tracker[client_ip].append(now)
    
    # 3. User-Agent基本チェック
    user_agent = request.headers.get('User-Agent', '')
    blocked_agents = ['bot', 'curl', 'wget', 'scraper', 'spider', 'crawler']
    
    for agent in blocked_agents:
        if agent.lower() in user_agent.lower():
            logger.warning(f"🚨 ブロックされたUser-Agent: {user_agent} from IP: {client_ip}")
            return False, "自動化されたアクセスは許可されていません"
    
    return True, None

def get_thread_local_jamdict():
    """スレッドローカルなjamdict インスタンスを取得"""
    if not hasattr(thread_local, 'jam'):
        thread_local.jam = Jamdict()
    return thread_local.jam

def get_character_stroke_count(char: str) -> Optional[int]:
    """文字の画数を取得（jamdict + ひらがな辞書）"""
    # ひらがなチェック
    if char in hiragana_strokes:
        return hiragana_strokes[char]['stroke']
    
    # 漢字チェック（スレッドローカルjamdict）
    try:
        local_jam = get_thread_local_jamdict()
        result = local_jam.lookup(char)
        if result.chars and len(result.chars) > 0:
            return result.chars[0].stroke_count
    except Exception as e:
        logger.warning(f"⚠️ jamdict検索エラー: {char} - {str(e)}")
    
    return None

def calculate_gogaku(last_name: str, first_name: str) -> Dict:
    """五格説による姓名判断計算"""
    # 文字ごとの画数取得
    last_name_chars = []
    first_name_chars = []
    
    # 姓の画数取得
    for char in last_name:
        stroke = get_character_stroke_count(char)
        if stroke is None:
            raise ValueError(f"対応していない文字があります: {char}")
        last_name_chars.append({'char': char, 'stroke': stroke})
    
    # 名の画数取得
    for char in first_name:
        stroke = get_character_stroke_count(char)
        if stroke is None:
            raise ValueError(f"対応していない文字があります: {char}")
        first_name_chars.append({'char': char, 'stroke': stroke})
    
    # 五格計算
    gogaku = {}
    
    # 天格（姓の合計）
    tenkaku = sum(char['stroke'] for char in last_name_chars)
    if len(last_name_chars) == 1:  # 一文字姓の場合、霊数+1
        tenkaku += 1
    
    # 地格（名の合計）
    chikaku = sum(char['stroke'] for char in first_name_chars)
    if len(first_name_chars) == 1:  # 一文字名の場合、霊数+1
        chikaku += 1
    
    # 人格（姓の最後 + 名の最初）
    jinkaku = last_name_chars[-1]['stroke'] + first_name_chars[0]['stroke']
    
    # 総格（姓名の合計）
    sokaku = sum(char['stroke'] for char in last_name_chars) + sum(char['stroke'] for char in first_name_chars)
    
    # 外格（総格 - 人格）
    gaikaku = sokaku - jinkaku
    if gaikaku <= 0:  # 外格が0以下の場合は霊数として1
        gaikaku = 1
    
    # 各格の判定結果取得
    judgment_table = gogaku_rules.get('judgment_table', {})
    
    gogaku['tenkaku'] = {
        'value': tenkaku,
        'result': judgment_table.get(str(tenkaku), {}).get('result', '不明'),
        'description': judgment_table.get(str(tenkaku), {}).get('description', '詳細不明')
    }
    
    gogaku['jinkaku'] = {
        'value': jinkaku,
        'result': judgment_table.get(str(jinkaku), {}).get('result', '不明'),
        'description': judgment_table.get(str(jinkaku), {}).get('description', '詳細不明')
    }
    
    gogaku['chikaku'] = {
        'value': chikaku,
        'result': judgment_table.get(str(chikaku), {}).get('result', '不明'),
        'description': judgment_table.get(str(chikaku), {}).get('description', '詳細不明')
    }
    
    gogaku['gaikaku'] = {
        'value': gaikaku,
        'result': judgment_table.get(str(gaikaku), {}).get('result', '不明'),
        'description': judgment_table.get(str(gaikaku), {}).get('description', '詳細不明')
    }
    
    gogaku['sokaku'] = {
        'value': sokaku,
        'result': judgment_table.get(str(sokaku), {}).get('result', '不明'),
        'description': judgment_table.get(str(sokaku), {}).get('description', '詳細不明')
    }
    
    return {
        'characters': last_name_chars + first_name_chars,
        'gogaku': gogaku
    }

def get_overall_judgment(gogaku_results: Dict) -> str:
    """総合判定の算出"""
    # 各格の結果を点数化
    score_map = {
        '大吉': 5,
        '吉': 4,
        '中吉': 3,
        '小吉': 2,
        '凶': 1,
        '大凶': 0
    }
    
    total_score = 0
    count = 0
    
    # 人格と総格を重視（2倍重み）
    important_kaku = ['jinkaku', 'sokaku']
    normal_kaku = ['tenkaku', 'chikaku', 'gaikaku']
    
    for kaku in important_kaku:
        result = gogaku_results.get(kaku, {}).get('result', '不明')
        if result in score_map:
            total_score += score_map[result] * 2
            count += 2
    
    for kaku in normal_kaku:
        result = gogaku_results.get(kaku, {}).get('result', '不明')
        if result in score_map:
            total_score += score_map[result]
            count += 1
    
    if count == 0:
        return '不明'
    
    avg_score = total_score / count
    
    # 平均点数から総合判定
    if avg_score >= 4.5:
        return '大吉'
    elif avg_score >= 3.5:
        return '吉'
    elif avg_score >= 2.5:
        return '中吉'
    elif avg_score >= 1.5:
        return '小吉'
    elif avg_score >= 0.5:
        return '凶'
    else:
        return '大凶'

@functions_framework.http
def seimei_handan(request):
    """姓名判断API メインエンドポイント - /api/v1/analyze"""
    
    # 辞書初期化
    initialize_dictionaries()
    
    # セキュリティチェック
    is_valid, error_msg = basic_security_check(request)
    if not is_valid:
        headers = {
            'Access-Control-Allow-Origin': '*',
            'Content-Type': 'application/json; charset=utf-8'
        }
        return jsonify({
            'success': False,
            'error': {'code': 'SECURITY_VIOLATION', 'message': error_msg}
        }), 403, headers
    
    # CORS対応
    if request.method == 'OPTIONS':
        headers = {
            'Access-Control-Allow-Origin': '*',
            'Access-Control-Allow-Methods': 'POST',
            'Access-Control-Allow-Headers': 'Content-Type',
            'Access-Control-Max-Age': '3600'
        }
        return ('', 204, headers)
    
    headers = {
        'Access-Control-Allow-Origin': '*',
        'Content-Type': 'application/json; charset=utf-8'
    }
    
    try:
        # リクエスト解析
        if not request.is_json:
            return jsonify({
                'success': False,
                'error': {
                    'code': 'INVALID_REQUEST_FORMAT',
                    'message': 'リクエストはJSON形式である必要があります'
                }
            }), 400, headers
        
        data = request.get_json()
        last_name = data.get('lastName', '').strip()
        first_name = data.get('firstName', '').strip()
        
        # バリデーション
        if not last_name or not first_name:
            return jsonify({
                'success': False,
                'error': {
                    'code': 'MISSING_REQUIRED_FIELDS',
                    'message': '姓と名の両方を入力してください'
                }
            }), 400, headers
        
        if len(last_name) > 10 or len(first_name) > 10:
            return jsonify({
                'success': False,
                'error': {
                    'code': 'NAME_TOO_LONG',
                    'message': '姓名は各10文字以内で入力してください'
                }
            }), 400, headers
        
        # 五格計算実行
        result = calculate_gogaku(last_name, first_name)
        
        # 総合判定追加
        overall = get_overall_judgment(result['gogaku'])
        
        # レスポンス返却
        return jsonify({
            'success': True,
            'data': {
                'characters': result['characters'],
                'gogaku': result['gogaku'],
                'overall': overall
            }
        }), 200, headers
        
    except ValueError as e:
        return jsonify({
            'success': False,
            'error': {
                'code': 'UNSUPPORTED_CHARACTER',
                'message': str(e)
            }
        }), 400, headers
        
    except Exception as e:
        logger.error(f"❌ 予期しないエラー: {str(e)}")
        return jsonify({
            'success': False,
            'error': {
                'code': 'INTERNAL_SERVER_ERROR',
                'message': 'サーバー内部エラーが発生しました'
            }
        }), 500, headers

def get_embedded_gogaku_rules() -> Dict:
    """埋め込み五格説ルール（ファイル読込失敗時のフォールバック）"""
    return {
        'judgment_table': {
            '1': {'result': '大吉', 'description': '独立心旺盛で指導力に優れる'},
            '2': {'result': '凶', 'description': '協調性はあるが意志薄弱'},
            '3': {'result': '大吉', 'description': '明朗快活で人気運あり'},
            '4': {'result': '凶', 'description': '几帳面だが消極的'},
            '5': {'result': '大吉', 'description': '温厚で人望を集める'},
            '6': {'result': '大吉', 'description': '責任感強く信頼される'},
            '7': {'result': '吉', 'description': '意志強固で独立心旺盛'},
            '8': {'result': '吉', 'description': '忍耐力があり努力家'},
            '9': {'result': '凶', 'description': '才能はあるが苦労多し'},
            '10': {'result': '凶', 'description': '空虚で挫折しやすい'}
            # 実際には81個すべてのルールが必要
        }
    }

def get_embedded_hiragana_strokes() -> Dict:
    """埋め込みひらがな画数（ファイル読込失敗時のフォールバック）"""
    return {
        'あ': {'stroke': 3}, 'い': {'stroke': 2}, 'う': {'stroke': 2}, 'え': {'stroke': 2}, 'お': {'stroke': 3},
        'か': {'stroke': 3}, 'き': {'stroke': 3}, 'く': {'stroke': 2}, 'け': {'stroke': 3}, 'こ': {'stroke': 2},
        'さ': {'stroke': 3}, 'し': {'stroke': 3}, 'す': {'stroke': 2}, 'せ': {'stroke': 3}, 'そ': {'stroke': 2},
        'た': {'stroke': 4}, 'ち': {'stroke': 3}, 'つ': {'stroke': 1}, 'て': {'stroke': 3}, 'と': {'stroke': 2},
        'な': {'stroke': 4}, 'に': {'stroke': 3}, 'ぬ': {'stroke': 2}, 'ね': {'stroke': 4}, 'の': {'stroke': 1},
        'は': {'stroke': 3}, 'ひ': {'stroke': 1}, 'ふ': {'stroke': 4}, 'へ': {'stroke': 1}, 'ほ': {'stroke': 4},
        'ま': {'stroke': 3}, 'み': {'stroke': 3}, 'む': {'stroke': 3}, 'め': {'stroke': 2}, 'も': {'stroke': 3},
        'や': {'stroke': 3}, 'ゆ': {'stroke': 2}, 'よ': {'stroke': 3},
        'ら': {'stroke': 2}, 'り': {'stroke': 2}, 'る': {'stroke': 1}, 'れ': {'stroke': 1}, 'ろ': {'stroke': 1},
        'わ': {'stroke': 3}, 'ん': {'stroke': 1}
    }

# Flask アプリケーション（ローカルテスト用）
app = Flask(__name__)
CORS(app)

@app.route('/api/v1/analyze', methods=['POST'])
def analyze():
    """ローカルテスト用エンドポイント"""
    return seimei_handan(request)

if __name__ == '__main__':
    # ローカルテスト実行
    app.run(debug=True, port=8080)