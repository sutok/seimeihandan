#!/usr/bin/env python3
"""
姓名判断アプリ - JSON読込パフォーマンステスト（簡易版）
"""

import time
import json
import os
import tracemalloc

def test_json_performance():
    """JSONファイル読込パフォーマンステスト"""
    print("🔍 JSON読込テスト開始...")
    
    # JSONファイルパス
    json_path = '../data/kanji_strokes.json'
    
    if not os.path.exists(json_path):
        print(f"❌ JSONファイルが見つかりません: {json_path}")
        return
    
    # メモリ追跡開始
    tracemalloc.start()
    
    # 初期化時間測定
    start_time = time.perf_counter()
    with open(json_path, 'r', encoding='utf-8') as f:
        kanji_data = json.load(f)
    init_time = time.perf_counter() - start_time
    
    # メモリ使用量測定
    current, peak = tracemalloc.get_traced_memory()
    tracemalloc.stop()
    
    # 検索速度テスト（1000回実行）
    test_chars = ['愛', '美', '田', '中', '太', '郎', '花', '子', '山', '川']
    search_times = []
    
    print("🔍 検索性能テスト実行中...")
    for i in range(1000):
        start_search = time.perf_counter()
        for char in test_chars:
            if char in kanji_data.get('kanji_dictionary', {}):
                stroke = kanji_data['kanji_dictionary'][char]['stroke']
            else:
                stroke = None  # 未登録文字
        search_times.append(time.perf_counter() - start_search)
        
        if (i + 1) % 100 == 0:
            print(f"   {i + 1}/1000 完了")
    
    avg_search_time = sum(search_times) / len(search_times)
    file_size = os.path.getsize(json_path)
    char_count = len(kanji_data.get('kanji_dictionary', {}))
    
    # 結果表示
    print("\n📊 JSON読込テスト結果")
    print("=" * 50)
    print(f"初期化時間: {init_time * 1000:.2f}ms")
    print(f"平均検索時間: {avg_search_time * 1000:.4f}ms (10文字)")
    print(f"1文字あたり検索時間: {avg_search_time * 1000 / len(test_chars):.4f}ms")
    print(f"メモリ使用量: {current / 1024 / 1024:.2f}MB")
    print(f"ピークメモリ: {peak / 1024 / 1024:.2f}MB")
    print(f"ファイルサイズ: {file_size / 1024:.2f}KB")
    print(f"登録文字数: {char_count}文字")
    
    # GCP Functions制約との比較
    print(f"\n🎯 GCP Functions制約との比較")
    print(f"目標応答時間: 500ms以下")
    print(f"現在の処理時間: {init_time * 1000 + avg_search_time * 1000:.2f}ms")
    
    if init_time * 1000 + avg_search_time * 1000 < 500:
        print("✅ 制約内に収まっています")
    else:
        print("❌ 制約を超えています")
    
    # 未登録文字のテスト
    print(f"\n❓ 未登録文字テスト")
    missing_chars = ['龍', '麗', '憂', '鬱', '薔', '薇']
    missing_count = 0
    
    for char in missing_chars:
        if char not in kanji_data.get('kanji_dictionary', {}):
            missing_count += 1
            print(f"   ❌ 未登録: {char}")
    
    print(f"未登録文字: {missing_count}/{len(missing_chars)} 文字")
    
    # 拡張予測
    print(f"\n📈 全JIS漢字対応予測")
    target_chars = 6300  # 全JIS漢字数
    current_chars = char_count
    scale_factor = target_chars / current_chars
    
    predicted_size = file_size * scale_factor / 1024  # KB
    predicted_memory = peak * scale_factor / 1024 / 1024  # MB
    predicted_init_time = init_time * scale_factor * 1000  # ms
    
    print(f"予測ファイルサイズ: {predicted_size:.0f}KB")
    print(f"予測メモリ使用量: {predicted_memory:.1f}MB")
    print(f"予測初期化時間: {predicted_init_time:.0f}ms")
    
    if predicted_init_time < 400:
        print("✅ 拡張しても制約内に収まる見込み")
    else:
        print("⚠️ 拡張すると制約を超える可能性あり")
    
    return {
        'init_time_ms': init_time * 1000,
        'avg_search_time_ms': avg_search_time * 1000,
        'memory_mb': peak / 1024 / 1024,
        'file_size_kb': file_size / 1024,
        'char_count': char_count,
        'missing_chars': missing_count,
        'predicted_size_kb': predicted_size,
        'predicted_memory_mb': predicted_memory,
        'predicted_init_time_ms': predicted_init_time
    }

if __name__ == "__main__":
    results = test_json_performance()
    
    # 結果をJSONで保存
    if results:
        output_path = '../test/json_performance_results.json'
        with open(output_path, 'w', encoding='utf-8') as f:
            json.dump(results, f, ensure_ascii=False, indent=2)
        print(f"\n💾 結果を {output_path} に保存しました")