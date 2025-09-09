#!/usr/bin/env python3
"""
姓名判断アプリ - 辞書パフォーマンス比較テスト
SQLite vs JSON読込速度の比較
"""

import time
import json
import os
import sqlite3
from typing import Dict, List, Tuple
import memory_profiler
import tracemalloc

class PerformanceTest:
    def __init__(self):
        self.results = {
            'json': {},
            'sqlite': {},
            'jamdict': {}
        }
        
    def test_json_performance(self, json_file_path: str) -> Dict:
        """JSONファイル読込パフォーマンステスト"""
        print("🔍 JSON読込テスト開始...")
        
        # メモリ追跡開始
        tracemalloc.start()
        
        # 初期化時間測定
        start_time = time.perf_counter()
        try:
            with open(json_file_path, 'r', encoding='utf-8') as f:
                kanji_data = json.load(f)
        except FileNotFoundError:
            print(f"❌ JSONファイルが見つかりません: {json_file_path}")
            return {}
            
        init_time = time.perf_counter() - start_time
        
        # メモリ使用量測定
        current, peak = tracemalloc.get_traced_memory()
        tracemalloc.stop()
        
        # 検索速度テスト（100回実行）
        test_chars = ['愛', '美', '龍', '田', '中', '太', '郎', '花', '子', '山']
        search_times = []
        
        for _ in range(100):
            start_search = time.perf_counter()
            for char in test_chars:
                if char in kanji_data.get('kanji_dictionary', {}):
                    stroke = kanji_data['kanji_dictionary'][char]['stroke']
                else:
                    stroke = None
            search_times.append(time.perf_counter() - start_search)
        
        avg_search_time = sum(search_times) / len(search_times)
        
        return {
            'init_time_ms': init_time * 1000,
            'avg_search_time_ms': avg_search_time * 1000,
            'memory_current_mb': current / 1024 / 1024,
            'memory_peak_mb': peak / 1024 / 1024,
            'file_size_kb': os.path.getsize(json_file_path) / 1024 if os.path.exists(json_file_path) else 0,
            'total_characters': len(kanji_data.get('kanji_dictionary', {}))
        }
    
    def test_jamdict_performance(self) -> Dict:
        """jamdictライブラリパフォーマンステスト"""
        print("🔍 jamdict SQLiteテスト開始...")
        
        # メモリ追跡開始
        tracemalloc.start()
        
        # 初期化時間測定
        start_time = time.perf_counter()
        try:
            from jamdict import Jamdict
            jam = Jamdict()
        except ImportError:
            print("❌ jamdictライブラリがインストールされていません")
            return {'error': 'jamdict_not_installed'}
        except Exception as e:
            print(f"❌ jamdict初期化エラー: {e}")
            return {'error': f'jamdict_init_error: {str(e)}'}
            
        init_time = time.perf_counter() - start_time
        
        # メモリ使用量測定
        current, peak = tracemalloc.get_traced_memory()
        tracemalloc.stop()
        
        # 検索速度テスト（100回実行）
        test_chars = ['愛', '美', '龍', '田', '中', '太', '郎', '花', '子', '山']
        search_times = []
        
        for _ in range(100):
            start_search = time.perf_counter()
            for char in test_chars:
                try:
                    result = jam.lookup(char)
                    if result.chars:
                        stroke = result.chars[0].stroke_count
                    else:
                        stroke = None
                except:
                    stroke = None
            search_times.append(time.perf_counter() - start_search)
        
        avg_search_time = sum(search_times) / len(search_times)
        
        # データベースサイズ取得（概算）
        try:
            db_size = jam.db_file_size() if hasattr(jam, 'db_file_size') else 0
        except:
            db_size = 0
        
        return {
            'init_time_ms': init_time * 1000,
            'avg_search_time_ms': avg_search_time * 1000,
            'memory_current_mb': current / 1024 / 1024,
            'memory_peak_mb': peak / 1024 / 1024,
            'db_size_mb': db_size / 1024 / 1024 if db_size else 0,
            'total_characters': 13108  # KanjiDic2の総文字数
        }
    
    def test_kotobase_performance(self) -> Dict:
        """kotobaseライブラリパフォーマンステスト"""
        print("🔍 kotobase SQLiteテスト開始...")
        
        # メモリ追跡開始
        tracemalloc.start()
        
        # 初期化時間測定
        start_time = time.perf_counter()
        try:
            from kotobase import Kotobase
            kb = Kotobase()
        except ImportError:
            print("❌ kotobaseライブラリがインストールされていません")
            return {'error': 'kotobase_not_installed'}
        except Exception as e:
            print(f"❌ kotobase初期化エラー: {e}")
            return {'error': f'kotobase_init_error: {str(e)}'}
            
        init_time = time.perf_counter() - start_time
        
        # メモリ使用量測定
        current, peak = tracemalloc.get_traced_memory()
        tracemalloc.stop()
        
        # 検索速度テスト（100回実行）
        test_chars = ['愛', '美', '龍', '田', '中', '太', '郎', '花', '子', '山']
        search_times = []
        
        for _ in range(100):
            start_search = time.perf_counter()
            for char in test_chars:
                try:
                    kanji_info = kb.kanji(char)
                    if hasattr(kanji_info, 'stroke_count'):
                        stroke = kanji_info.stroke_count
                    else:
                        stroke = None
                except:
                    stroke = None
            search_times.append(time.perf_counter() - start_search)
        
        avg_search_time = sum(search_times) / len(search_times)
        
        return {
            'init_time_ms': init_time * 1000,
            'avg_search_time_ms': avg_search_time * 1000,
            'memory_current_mb': current / 1024 / 1024,
            'memory_peak_mb': peak / 1024 / 1024,
            'db_size_mb': 0,  # サイズ不明
            'total_characters': 'unknown'
        }

    def run_comprehensive_test(self):
        """包括的パフォーマンステスト実行"""
        print("🚀 姓名判断辞書パフォーマンス比較テスト開始")
        print("=" * 60)
        
        # 1. JSON読込テスト
        json_path = '../data/kanji_strokes.json'
        self.results['json'] = self.test_json_performance(json_path)
        
        # 2. jamdict SQLiteテスト
        self.results['jamdict'] = self.test_jamdict_performance()
        
        # 3. kotobase SQLiteテスト  
        self.results['sqlite'] = self.test_kotobase_performance()
        
        # 結果表示
        self.display_results()
        
        # 推奨案の決定
        self.recommend_solution()
        
    def display_results(self):
        """テスト結果表示"""
        print("\n📊 パフォーマンステスト結果")
        print("=" * 60)
        
        methods = ['JSON', 'jamdict', 'kotobase']
        keys = ['json', 'jamdict', 'sqlite']
        
        for method, key in zip(methods, keys):
            result = self.results[key]
            if 'error' in result:
                print(f"\n❌ {method}: {result['error']}")
                continue
                
            print(f"\n✅ {method}:")
            print(f"   初期化時間: {result.get('init_time_ms', 0):.2f}ms")
            print(f"   検索時間: {result.get('avg_search_time_ms', 0):.4f}ms")
            print(f"   メモリ使用量: {result.get('memory_peak_mb', 0):.2f}MB")
            print(f"   データサイズ: {result.get('file_size_kb', result.get('db_size_mb', 0)):.2f}KB/MB")
            print(f"   文字数: {result.get('total_characters', 'unknown')}")
    
    def recommend_solution(self):
        """最適解の推奨"""
        print("\n🎯 推奨案")
        print("=" * 60)
        
        # GCP Functions制約
        target_init_time = 200  # ms
        target_search_time = 50  # ms
        target_memory = 100     # MB
        
        recommendations = []
        
        for method, key in [('JSON', 'json'), ('jamdict', 'jamdict'), ('kotobase', 'sqlite')]:
            result = self.results[key]
            if 'error' in result:
                continue
                
            score = 0
            reasons = []
            
            # 初期化時間評価
            init_time = result.get('init_time_ms', float('inf'))
            if init_time < target_init_time:
                score += 3
                reasons.append("✅ 初期化高速")
            elif init_time < target_init_time * 2:
                score += 1
                reasons.append("⚠️ 初期化やや遅い")
            else:
                reasons.append("❌ 初期化が遅い")
            
            # 検索時間評価
            search_time = result.get('avg_search_time_ms', float('inf'))
            if search_time < target_search_time:
                score += 3
                reasons.append("✅ 検索高速")
            elif search_time < target_search_time * 2:
                score += 1
                reasons.append("⚠️ 検索やや遅い")
            else:
                reasons.append("❌ 検索が遅い")
            
            # メモリ使用量評価
            memory = result.get('memory_peak_mb', float('inf'))
            if memory < target_memory:
                score += 2
                reasons.append("✅ 省メモリ")
            elif memory < target_memory * 2:
                score += 1
                reasons.append("⚠️ メモリやや多い")
            else:
                reasons.append("❌ メモリ消費大")
            
            # データ完全性評価
            char_count = result.get('total_characters', 0)
            if char_count > 6000:
                score += 3
                reasons.append("✅ 完全なデータ")
            elif char_count > 1000:
                score += 1
                reasons.append("⚠️ 限定的なデータ")
            else:
                reasons.append("❌ データ不足")
            
            recommendations.append({
                'method': method,
                'score': score,
                'reasons': reasons,
                'result': result
            })
        
        # スコア順にソート
        recommendations.sort(key=lambda x: x['score'], reverse=True)
        
        print(f"🏆 最優秀: {recommendations[0]['method']} (スコア: {recommendations[0]['score']}/11)")
        for reason in recommendations[0]['reasons']:
            print(f"   {reason}")
        
        if len(recommendations) > 1:
            print(f"\n🥈 次点: {recommendations[1]['method']} (スコア: {recommendations[1]['score']}/11)")
            for reason in recommendations[1]['reasons']:
                print(f"   {reason}")

if __name__ == "__main__":
    # パフォーマンステスト実行
    test = PerformanceTest()
    test.run_comprehensive_test()
    
    # 結果をJSONで保存
    with open('../test/performance_results.json', 'w', encoding='utf-8') as f:
        json.dump(test.results, f, ensure_ascii=False, indent=2)
    
    print(f"\n💾 結果を performance_results.json に保存しました")