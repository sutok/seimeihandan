#!/usr/bin/env python3
"""
姓名判断アプリ - APIテストケース
jamdict統合版の動作検証
"""

import json
import requests
import time
from typing import Dict, List

class SeimeiHandanAPITest:
    def __init__(self, base_url: str = 'http://localhost:8080'):
        self.base_url = base_url
        self.test_cases = []
        self.load_test_cases()
    
    def load_test_cases(self):
        """テストケースデータ読込"""
        try:
            with open('data_validation.json', 'r', encoding='utf-8') as f:
                validation_data = json.load(f)
                self.test_cases = validation_data.get('test_cases', {})
        except FileNotFoundError:
            # 埋め込みテストケース使用
            self.test_cases = self.get_embedded_test_cases()
    
    def test_basic_functionality(self):
        """基本機能テスト"""
        print("🧪 基本機能テスト開始")
        print("=" * 50)
        
        # テストケース1: 田中太郎
        test_case = {
            'lastName': '田中',
            'firstName': '太郎',
            'expected_chars': [
                {'char': '田', 'stroke': 5},
                {'char': '中', 'stroke': 4},
                {'char': '太', 'stroke': 4},
                {'char': '郎', 'stroke': 9}
            ]
        }
        
        result = self.call_api(test_case['lastName'], test_case['firstName'])
        
        if result and result.get('success'):
            print(f"✅ {test_case['lastName']}{test_case['firstName']} - 成功")
            
            # 画数検証
            chars = result.get('data', {}).get('characters', [])
            for i, expected_char in enumerate(test_case['expected_chars']):
                if i < len(chars):
                    actual_char = chars[i]
                    if actual_char['char'] == expected_char['char']:
                        if actual_char['stroke'] == expected_char['stroke']:
                            print(f"   ✅ {expected_char['char']}: {expected_char['stroke']}画 - 正確")
                        else:
                            print(f"   ❌ {expected_char['char']}: 期待{expected_char['stroke']}画, 実際{actual_char['stroke']}画")
                    else:
                        print(f"   ❌ 文字不一致: 期待{expected_char['char']}, 実際{actual_char.get('char', 'なし')}")
            
            # 五格検証
            gogaku = result.get('data', {}).get('gogaku', {})
            print(f"   天格: {gogaku.get('tenkaku', {}).get('value')} - {gogaku.get('tenkaku', {}).get('result')}")
            print(f"   人格: {gogaku.get('jinkaku', {}).get('value')} - {gogaku.get('jinkaku', {}).get('result')}")
            print(f"   地格: {gogaku.get('chikaku', {}).get('value')} - {gogaku.get('chikaku', {}).get('result')}")
            print(f"   外格: {gogaku.get('gaikaku', {}).get('value')} - {gogaku.get('gaikaku', {}).get('result')}")
            print(f"   総格: {gogaku.get('sokaku', {}).get('value')} - {gogaku.get('sokaku', {}).get('result')}")
            print(f"   総合: {result.get('data', {}).get('overall')}")
            
        else:
            print(f"❌ {test_case['lastName']}{test_case['firstName']} - 失敗")
            if result:
                print(f"   エラー: {result.get('error', {}).get('message')}")
    
    def test_hiragana_mixed(self):
        """ひらがな混在テスト"""
        print("\n🔤 ひらがな混在テスト")
        print("=" * 50)
        
        test_cases = [
            {'lastName': '田中', 'firstName': 'あい'},
            {'lastName': 'さとう', 'firstName': '美香'},
            {'lastName': 'やまだ', 'firstName': 'ひろし'}
        ]
        
        for test_case in test_cases:
            result = self.call_api(test_case['lastName'], test_case['firstName'])
            
            if result and result.get('success'):
                print(f"✅ {test_case['lastName']}{test_case['firstName']} - 成功")
                overall = result.get('data', {}).get('overall')
                print(f"   総合判定: {overall}")
            else:
                print(f"❌ {test_case['lastName']}{test_case['firstName']} - 失敗")
                if result:
                    print(f"   エラー: {result.get('error', {}).get('message')}")
    
    def test_edge_cases(self):
        """エッジケーステスト"""
        print("\n⚠️ エッジケーステスト")
        print("=" * 50)
        
        # 一文字姓名
        result = self.call_api('森', '薫')
        if result and result.get('success'):
            print("✅ 一文字姓名 - 成功（霊数処理）")
            gogaku = result.get('data', {}).get('gogaku', {})
            print(f"   天格: {gogaku.get('tenkaku', {}).get('value')} (霊数+1)")
            print(f"   地格: {gogaku.get('chikaku', {}).get('value')} (霊数+1)")
        else:
            print("❌ 一文字姓名 - 失敗")
        
        # 長い名前
        result = self.call_api('高橋', '太郎次郎')
        if result and result.get('success'):
            print("✅ 長い名前 - 成功")
        else:
            print("❌ 長い名前 - 失敗")
        
        # 無効な文字（絵文字等）
        result = self.call_api('田中', '🌸')
        if result and not result.get('success'):
            print("✅ 無効文字エラー処理 - 成功")
            print(f"   エラー: {result.get('error', {}).get('message')}")
        else:
            print("❌ 無効文字エラー処理 - 失敗")
    
    def test_performance(self):
        """パフォーマンステスト"""
        print("\n⚡ パフォーマンステスト")
        print("=" * 50)
        
        test_names = [
            ('田中', '太郎'), ('山田', '花子'), ('佐藤', '美香'),
            ('高橋', 'ひろし'), ('渡辺', 'ゆうき'), ('森', '薫'),
            ('あいだ', 'みどり'), ('いとう', 'まさき'), ('おかだ', 'けんじ')
        ]
        
        response_times = []
        
        print("10回連続実行テスト...")
        for i in range(10):
            for last_name, first_name in test_names:
                start_time = time.time()
                result = self.call_api(last_name, first_name)
                end_time = time.time()
                
                response_time = (end_time - start_time) * 1000  # ms
                response_times.append(response_time)
                
                if result and result.get('success'):
                    status = "✅"
                else:
                    status = "❌"
                
                print(f"   {status} {last_name}{first_name}: {response_time:.2f}ms")
        
        # 統計計算
        avg_time = sum(response_times) / len(response_times)
        max_time = max(response_times)
        min_time = min(response_times)
        
        print(f"\n📊 パフォーマンス統計:")
        print(f"   平均応答時間: {avg_time:.2f}ms")
        print(f"   最大応答時間: {max_time:.2f}ms")
        print(f"   最小応答時間: {min_time:.2f}ms")
        print(f"   総実行回数: {len(response_times)}回")
        
        # 500ms制約チェック
        over_limit = [t for t in response_times if t > 500]
        if len(over_limit) == 0:
            print(f"✅ 全て500ms以内に完了 - 制約クリア")
        else:
            print(f"⚠️ {len(over_limit)}回が500ms超過 - 要最適化")
    
    def call_api(self, last_name: str, first_name: str) -> Dict:
        """API呼び出し"""
        try:
            response = requests.post(
                f"{self.base_url}/api/v1/analyze",
                json={'lastName': last_name, 'firstName': first_name},
                headers={'Content-Type': 'application/json'},
                timeout=10
            )
            return response.json()
        except requests.exceptions.RequestException as e:
            print(f"❌ API呼び出しエラー: {str(e)}")
            return None
        except json.JSONDecodeError as e:
            print(f"❌ JSON解析エラー: {str(e)}")
            return None
    
    def get_embedded_test_cases(self) -> Dict:
        """埋め込みテストケース"""
        return {
            'basic_calculation': [
                {
                    'name': '田中太郎',
                    'lastName': '田中',
                    'firstName': '太郎',
                    'expected_chars': [
                        {'char': '田', 'stroke': 5},
                        {'char': '中', 'stroke': 4},
                        {'char': '太', 'stroke': 4},
                        {'char': '郎', 'stroke': 9}
                    ]
                }
            ]
        }
    
    def run_all_tests(self):
        """全テスト実行"""
        print("🚀 姓名判断API総合テスト開始")
        print("=" * 60)
        
        self.test_basic_functionality()
        self.test_hiragana_mixed()
        self.test_edge_cases()
        self.test_performance()
        
        print("\n🎉 全テスト完了")

if __name__ == "__main__":
    # APIテスト実行
    tester = SeimeiHandanAPITest()
    
    print("⚠️ 注意: API実行前にローカルサーバーを起動してください")
    print("   コマンド: python functions/main.py")
    input("\nサーバー起動後、Enterキーを押してテストを開始...")
    
    tester.run_all_tests()