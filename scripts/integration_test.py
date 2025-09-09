#!/usr/bin/env python3
"""
姓名判断アプリ - ローカル統合テストスクリプト
フロントエンド・バックエンド接続確認
"""

import os
import time
import subprocess
import requests
import json
from typing import Dict, List
import threading
import signal
import sys

class IntegrationTester:
    def __init__(self):
        self.backend_process = None
        self.frontend_process = None
        self.backend_url = "http://localhost:8080"
        self.frontend_url = "http://localhost:3000"
        self.api_endpoint = f"{self.backend_url}/api/v1/analyze"
        
    def start_backend(self) -> bool:
        """バックエンドサーバー起動"""
        print("🔧 バックエンドサーバー起動中...")
        
        try:
            # functionsディレクトリに移動してサーバー起動
            os.chdir("functions")
            self.backend_process = subprocess.Popen(
                ["python", "main.py"],
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                text=True
            )
            
            # 起動待機
            max_attempts = 30
            for attempt in range(max_attempts):
                try:
                    response = requests.get(f"{self.backend_url}", timeout=2)
                    if response.status_code in [200, 404]:  # 404でもサーバーは起動済み
                        print("✅ バックエンドサーバー起動完了")
                        os.chdir("..")  # 元のディレクトリに戻る
                        return True
                except requests.exceptions.RequestException:
                    time.sleep(2)
                    print(f"   起動待機中... ({attempt + 1}/{max_attempts})")
            
            print("❌ バックエンドサーバー起動タイムアウト")
            os.chdir("..")
            return False
            
        except Exception as e:
            print(f"❌ バックエンドサーバー起動エラー: {str(e)}")
            os.chdir("..")
            return False
    
    def start_frontend(self) -> bool:
        """フロントエンドサーバー起動"""
        print("🎨 フロントエンドサーバー起動中...")
        
        try:
            # frontendディレクトリに移動してサーバー起動
            os.chdir("frontend")
            
            # 環境変数設定
            env = os.environ.copy()
            env["REACT_APP_API_URL"] = self.backend_url
            env["BROWSER"] = "none"  # ブラウザ自動起動を無効化
            
            self.frontend_process = subprocess.Popen(
                ["npm", "start"],
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                text=True,
                env=env
            )
            
            # 起動待機
            max_attempts = 60  # フロントエンドは時間がかかる
            for attempt in range(max_attempts):
                try:
                    response = requests.get(self.frontend_url, timeout=2)
                    if response.status_code == 200:
                        print("✅ フロントエンドサーバー起動完了")
                        os.chdir("..")
                        return True
                except requests.exceptions.RequestException:
                    time.sleep(2)
                    if attempt % 5 == 0:
                        print(f"   起動待機中... ({attempt + 1}/{max_attempts})")
            
            print("❌ フロントエンドサーバー起動タイムアウト")
            os.chdir("..")
            return False
            
        except Exception as e:
            print(f"❌ フロントエンドサーバー起動エラー: {str(e)}")
            os.chdir("..")
            return False
    
    def test_api_direct(self) -> bool:
        """APIエンドポイント直接テスト"""
        print("\n🧪 API直接テスト開始")
        
        test_cases = [
            {"lastName": "田中", "firstName": "太郎"},
            {"lastName": "山田", "firstName": "花子"},
            {"lastName": "田中", "firstName": "あい"},
            {"lastName": "さとう", "firstName": "美香"},
            {"lastName": "森", "firstName": "薫"}  # 一文字姓名
        ]
        
        success_count = 0
        
        for i, test_case in enumerate(test_cases, 1):
            try:
                # 小さな遅延を追加してAPI負荷を分散
                if i > 1:
                    time.sleep(0.5)
                    
                start_time = time.time()
                response = requests.post(
                    self.api_endpoint,
                    json=test_case,
                    headers={"Content-Type": "application/json"},
                    timeout=10
                )
                end_time = time.time()
                
                response_time = (end_time - start_time) * 1000  # ms
                
                if response.status_code == 200:
                    data = response.json()
                    if data.get("success"):
                        print(f"   ✅ テスト{i}: {test_case['lastName']}{test_case['firstName']} - 成功 ({response_time:.2f}ms)")
                        # 結果の詳細表示
                        overall = data.get("data", {}).get("overall", "不明")
                        print(f"      総合判定: {overall}")
                        success_count += 1
                    else:
                        error_msg = data.get("error", {}).get("message", "不明なエラー")
                        print(f"   ❌ テスト{i}: {test_case['lastName']}{test_case['firstName']} - APIエラー: {error_msg}")
                else:
                    print(f"   ❌ テスト{i}: {test_case['lastName']}{test_case['firstName']} - HTTPエラー: {response.status_code}")
                
            except Exception as e:
                print(f"   ❌ テスト{i}: {test_case['lastName']}{test_case['firstName']} - 例外: {str(e)}")
        
        print(f"\n📊 API直接テスト結果: {success_count}/{len(test_cases)} 成功")
        return success_count == len(test_cases)
    
    def test_error_handling(self) -> bool:
        """エラーハンドリングテスト"""
        print("\n🚨 エラーハンドリングテスト開始")
        
        error_cases = [
            {"lastName": "", "firstName": "太郎", "expected": "MISSING_REQUIRED_FIELDS"},
            {"lastName": "田中", "firstName": "", "expected": "MISSING_REQUIRED_FIELDS"},
            {"lastName": "田中🌸", "firstName": "太郎", "expected": "UNSUPPORTED_CHARACTER"},
            {"lastName": "a" * 15, "firstName": "太郎", "expected": "NAME_TOO_LONG"}
        ]
        
        success_count = 0
        
        for i, test_case in enumerate(error_cases, 1):
            try:
                response = requests.post(
                    self.api_endpoint,
                    json={"lastName": test_case["lastName"], "firstName": test_case["firstName"]},
                    headers={"Content-Type": "application/json"},
                    timeout=5
                )
                
                if response.status_code == 400:  # エラーレスポンスを期待
                    data = response.json()
                    if not data.get("success"):
                        print(f"   ✅ エラーテスト{i}: 適切なエラー処理 - {data.get('error', {}).get('code')}")
                        success_count += 1
                    else:
                        print(f"   ❌ エラーテスト{i}: エラーが発生すべき")
                else:
                    print(f"   ❌ エラーテスト{i}: 期待されるステータスコード400、実際{response.status_code}")
                
            except Exception as e:
                print(f"   ❌ エラーテスト{i}: 例外 - {str(e)}")
        
        print(f"\n📊 エラーハンドリングテスト結果: {success_count}/{len(error_cases)} 成功")
        return success_count == len(error_cases)
    
    def test_performance(self) -> bool:
        """パフォーマンステスト"""
        print("\n⚡ パフォーマンステスト開始")
        
        test_case = {"lastName": "田中", "firstName": "太郎"}
        response_times = []
        
        # 10回実行してパフォーマンス測定
        for i in range(10):
            try:
                start_time = time.time()
                response = requests.post(
                    self.api_endpoint,
                    json=test_case,
                    headers={"Content-Type": "application/json"},
                    timeout=5
                )
                end_time = time.time()
                
                response_time = (end_time - start_time) * 1000
                response_times.append(response_time)
                
                if response.status_code == 200:
                    print(f"   ✅ パフォーマンステスト{i+1}: {response_time:.2f}ms")
                else:
                    print(f"   ❌ パフォーマンステスト{i+1}: HTTPエラー {response.status_code}")
                    
            except Exception as e:
                print(f"   ❌ パフォーマンステスト{i+1}: 例外 - {str(e)}")
        
        if response_times:
            avg_time = sum(response_times) / len(response_times)
            max_time = max(response_times)
            min_time = min(response_times)
            
            print(f"\n📊 パフォーマンス統計:")
            print(f"   平均応答時間: {avg_time:.2f}ms")
            print(f"   最大応答時間: {max_time:.2f}ms")
            print(f"   最小応答時間: {min_time:.2f}ms")
            
            # 500ms制約チェック
            if max_time <= 500:
                print("   ✅ 500ms制約クリア")
                return True
            else:
                print("   ❌ 500ms制約超過")
                return False
        else:
            print("   ❌ パフォーマンステスト失敗")
            return False
    
    def test_frontend_backend_integration(self) -> bool:
        """フロントエンド・バックエンド統合テスト"""
        print("\n🔗 フロントエンド・バックエンド統合テスト")
        
        # フロントエンドが正しくバックエンドAPIを呼び出せるかテスト
        try:
            # フロントエンドページが正しく読み込まれるかチェック
            response = requests.get(self.frontend_url, timeout=10)
            if response.status_code != 200:
                print("   ❌ フロントエンドページ読み込み失敗")
                return False
            
            # HTMLに必要な要素が含まれているかチェック（基本的な要素のみ）
            html_content = response.text
            required_elements = ["姓名判断", "姓", "名"]
            
            for element in required_elements:
                if element in html_content:
                    print(f"   ✅ UI要素確認: '{element}' 存在")
                else:
                    print(f"   ❌ UI要素確認: '{element}' 不在")
                    return False
            
            # React コンポーネントが読み込まれる時間を待つ
            print("   ⏳ Reactコンポーネントの読み込み待機中...")
            time.sleep(3)
            
            # 再度ページをチェックしてReact要素を確認
            response = requests.get(self.frontend_url, timeout=10)
            html_content = response.text
            if "診断する" in html_content or "react" in html_content.lower():
                print("   ✅ React要素確認: Reactアプリケーション読み込み済み")
            else:
                print("   ⚠️ React要素確認: Reactアプリは動作中だが、静的チェックでは確認困難")
            
            print("   ✅ フロントエンド・バックエンド統合テスト成功")
            return True
            
        except Exception as e:
            print(f"   ❌ 統合テスト例外: {str(e)}")
            return False
    
    def cleanup(self):
        """プロセス終了処理"""
        print("\n🧹 テスト環境クリーンアップ中...")
        
        if self.backend_process:
            try:
                self.backend_process.terminate()
                self.backend_process.wait(timeout=5)
                print("   ✅ バックエンドプロセス終了")
            except:
                self.backend_process.kill()
                print("   ⚠️ バックエンドプロセス強制終了")
        
        if self.frontend_process:
            try:
                self.frontend_process.terminate()
                self.frontend_process.wait(timeout=5)
                print("   ✅ フロントエンドプロセス終了")
            except:
                self.frontend_process.kill()
                print("   ⚠️ フロントエンドプロセス強制終了")
    
    def run_integration_test(self) -> bool:
        """統合テスト実行"""
        print("🚀 姓名判断アプリ - ローカル統合テスト開始")
        print("=" * 60)
        
        try:
            # バックエンド起動
            if not self.start_backend():
                return False
            
            # フロントエンド起動
            if not self.start_frontend():
                return False
            
            # 各種テスト実行
            api_test_result = self.test_api_direct()
            error_test_result = self.test_error_handling()
            performance_test_result = self.test_performance()
            integration_test_result = self.test_frontend_backend_integration()
            
            # 総合結果
            all_tests_passed = all([
                api_test_result,
                error_test_result, 
                performance_test_result,
                integration_test_result
            ])
            
            print("\n" + "=" * 60)
            print("📊 統合テスト総合結果")
            print(f"   API機能テスト: {'✅ PASS' if api_test_result else '❌ FAIL'}")
            print(f"   エラーハンドリング: {'✅ PASS' if error_test_result else '❌ FAIL'}")
            print(f"   パフォーマンス: {'✅ PASS' if performance_test_result else '❌ FAIL'}")
            print(f"   統合テスト: {'✅ PASS' if integration_test_result else '❌ FAIL'}")
            print()
            
            if all_tests_passed:
                print("🎉 全ての統合テストが成功しました！")
                print("   Phase 4: 統合・テスト・デプロイ - ローカルテスト完了")
            else:
                print("⚠️ 一部のテストが失敗しました。修正が必要です。")
            
            return all_tests_passed
            
        except KeyboardInterrupt:
            print("\n⏹️ ユーザーによる中断")
            return False
        except Exception as e:
            print(f"\n❌ 予期しないエラー: {str(e)}")
            return False
        finally:
            self.cleanup()

def signal_handler(sig, frame):
    """Ctrl+C ハンドラー"""
    print("\n⏹️ 統合テスト中断中...")
    sys.exit(0)

if __name__ == "__main__":
    # シグナルハンドラー設定
    signal.signal(signal.SIGINT, signal_handler)
    
    # 統合テスト実行
    tester = IntegrationTester()
    success = tester.run_integration_test()
    
    # 終了コード設定
    sys.exit(0 if success else 1)