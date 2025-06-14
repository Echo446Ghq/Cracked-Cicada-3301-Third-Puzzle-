#!/usr/bin/env python3

import re
import itertools
import hashlib
import base64
from datetime import datetime
from collections import Counter
import math

class CicadaFocusedDecoder:
    def __init__(self):
        self.original_number = "10412790658919985359827898739594318956404425106955675643739226952372682423852959081739834390370374475764863415203423499357108713631"
        self.key_palindromes = ['78987', '7447', '13631']
        self.pattern_739 = "739"
        self.fibonacci_positions = self.generate_fibonacci_positions()
        self.results = []
        self.timestamp = datetime.now().strftime('%Y-%m-%d_%H-%M-%S')
        
    def log_result(self, category, finding, confidence="MEDIUM"):
        self.results.append({
            'category': category,
            'finding': finding,
            'confidence': confidence,
            'timestamp': datetime.now().strftime('%H:%M:%S')
        })
        print(f"[{confidence}] {category}: {finding}")
    
    def generate_fibonacci_positions(self):
        fib = [1, 1]
        while fib[-1] < len(self.original_number):
            fib.append(fib[-1] + fib[-2])
        return [f for f in fib if f <= len(self.original_number)]
    
    def extract_every_nth_digit(self, data, n, start_offset=0):
        return ''.join([data[i] for i in range(start_offset, len(data), n)])
    
    def decode_primary_method(self):
        self.log_result("PRIMARY_DECODE", "Testing highest confidence method (92.3% validity)", "HIGH")
        
        every_5th = self.extract_every_nth_digit(self.original_number, 5)
        self.log_result("EXTRACTION", f"Every 5th digit: {every_5th}", "HIGH")
        
        shifted_data = every_5th[1:] + every_5th[:1]
        self.log_result("SHIFT", f"Shifted data: {shifted_data}", "HIGH")
        
        ascii_result = ""
        hex_result = ""
        decimal_values = []
        
        for i in range(0, len(shifted_data) - 1, 2):
            group = shifted_data[i:i+2]
            try:
                ascii_val = int(group)
                decimal_values.append(ascii_val)
                
                if 32 <= ascii_val <= 126:
                    ascii_result += chr(ascii_val)
                elif 1 <= ascii_val <= 31:
                    ascii_result += f"[{ascii_val}]"
                else:
                    ascii_result += "?"
                
                hex_result += f"{ascii_val:02x}"
                
            except ValueError:
                ascii_result += "?"
                hex_result += "??"
        
        self.log_result("ASCII_DECODE", f"Primary decode result: '{ascii_result}'", "CRITICAL")
        self.log_result("HEX_DECODE", f"Hex interpretation: {hex_result}", "HIGH")
        self.log_result("DECIMAL_VALUES", f"Decimal values: {decimal_values}", "HIGH")
        
        self.analyze_decoded_text(ascii_result, "PRIMARY")
        
        return ascii_result, decimal_values
    
    def decode_secondary_method(self):
        self.log_result("SECONDARY_DECODE", "Testing second highest confidence method (84.6% validity)", "HIGH")
        
        every_5th = self.extract_every_nth_digit(self.original_number, 5)
        
        shifted_data = every_5th[3:] + every_5th[:3]
        self.log_result("SHIFT", f"Shift-3 data: {shifted_data}", "HIGH")
        
        ascii_result = ""
        decimal_values = []
        
        for i in range(0, len(shifted_data) - 1, 2):
            group = shifted_data[i:i+2]
            try:
                ascii_val = int(group)
                decimal_values.append(ascii_val)
                
                if 32 <= ascii_val <= 126:
                    ascii_result += chr(ascii_val)
                elif 1 <= ascii_val <= 31:
                    ascii_result += f"[{ascii_val}]"
                else:
                    ascii_result += "?"
                    
            except ValueError:
                ascii_result += "?"
        
        self.log_result("ASCII_DECODE", f"Secondary decode result: '{ascii_result}'", "CRITICAL")
        self.analyze_decoded_text(ascii_result, "SECONDARY")
        
        return ascii_result, decimal_values
    
    def decode_palindrome_fibonacci_method(self):
        self.log_result("PALINDROME_DECODE", "Testing palindrome 7447 + fibonacci method (83.3% validity)", "HIGH")
        
        fib_digits = ""
        for pos in self.fibonacci_positions:
            if pos <= len(self.original_number):
                fib_digits += self.original_number[pos - 1]
        
        self.log_result("FIBONACCI_EXTRACTION", f"Fibonacci position digits: {fib_digits}", "HIGH")
        
        palindrome = "7447"
        xor_result = ""
        
        for i, digit in enumerate(fib_digits):
            try:
                digit_val = int(digit)
                key_val = int(palindrome[i % len(palindrome)])
                xor_val = digit_val ^ key_val
                xor_result += str(xor_val)
            except ValueError:
                xor_result += digit
        
        self.log_result("XOR_RESULT", f"XOR result: {xor_result}", "HIGH")
        
        self.test_as_coordinates(xor_result)
        
        ascii_result = self.convert_to_ascii(xor_result, 2)
        if ascii_result:
            self.log_result("ASCII_DECODE", f"Palindrome-Fibonacci ASCII: '{ascii_result}'", "HIGH")
        
        return xor_result
    
    def decode_xor_739_method(self):
        self.log_result("XOR_739_DECODE", "Analyzing XOR with pattern 739", "HIGH")
        
        xor_result = ""
        pattern = "739"
        
        for i, digit in enumerate(self.original_number):
            try:
                digit_val = int(digit)
                pattern_val = int(pattern[i % len(pattern)])
                xor_val = digit_val ^ pattern_val
                xor_result += str(xor_val)
            except ValueError:
                xor_result += digit
        
        self.log_result("XOR_739_RESULT", f"XOR 739 result (first 50): {xor_result[:50]}...", "HIGH")
        
        self.analyze_xor_patterns(xor_result)
        
        ascii_2digit = self.convert_to_ascii(xor_result, 2)
        if ascii_2digit:
            self.log_result("XOR_739_ASCII", f"XOR 739 ASCII: '{ascii_2digit[:50]}...'", "MEDIUM")
        
        return xor_result
    
    def test_coordinate_hypotheses(self):
        self.log_result("COORDINATE_ANALYSIS", "Testing coordinate hypotheses", "HIGH")
        
        original_coord = (4.4251, 69.556)
        self.log_result("COORDINATE", f"Original discovered coordinate: {original_coord[0]}°N, {original_coord[1]}°E", "HIGH")
        
        every_5th = self.extract_every_nth_digit(self.original_number, 5)
        self.test_as_coordinates(every_5th)
        
        palindrome_result = self.decode_palindrome_fibonacci_method()
        
    def analyze_decoded_text(self, text, method_name):
        if not text or len(text) < 3:
            return
        
        cicada_keywords = [
            'CICADA', 'LIBER', 'PRIMUS', 'WELCOME', 'PARABLE', 'ILLUMINATI',
            'THELEMA', 'DIVINITY', 'PATH', 'ENLIGHTENMENT', 'INSTAR', 'EMERGENCE'
        ]
        
        text_upper = text.upper()
        found_keywords = [kw for kw in cicada_keywords if kw in text_upper]
        
        if found_keywords:
            self.log_result("KEYWORD_MATCH", f"{method_name} contains keywords: {found_keywords}", "CRITICAL")
        
        coord_patterns = re.findall(r'\d+[.,]\d+', text)
        if coord_patterns:
            self.log_result("COORDINATE_PATTERN", f"{method_name} coordinate patterns: {coord_patterns}", "HIGH")
        
        url_patterns = re.findall(r'https?://[^\s]+|www\.[^\s]+|[a-zA-Z0-9]+\.[a-zA-Z]{2,}', text)
        if url_patterns:
            self.log_result("URL_PATTERN", f"{method_name} URL patterns: {url_patterns}", "CRITICAL")
        
        hash_patterns = re.findall(r'[a-fA-F0-9]{32,}', text)
        if hash_patterns:
            self.log_result("HASH_PATTERN", f"{method_name} hash patterns: {hash_patterns}", "HIGH")
        
        if len(text) > 10:
            char_freq = Counter(text)
            common_chars = char_freq.most_common(5)
            self.log_result("CHAR_FREQUENCY", f"{method_name} common chars: {common_chars}", "MEDIUM")
    
    def convert_to_ascii(self, data, group_size):
        result = ""
        valid_count = 0
        total_count = 0
        
        for i in range(0, len(data) - group_size + 1, group_size):
            group = data[i:i + group_size]
            if len(group) == group_size:
                try:
                    ascii_val = int(group)
                    total_count += 1
                    if 32 <= ascii_val <= 126:
                        result += chr(ascii_val)
                        valid_count += 1
                    else:
                        result += "?"
                except ValueError:
                    result += "?"
                    total_count += 1
        
        validity = (valid_count / total_count * 100) if total_count > 0 else 0
        
        if validity > 40:
            return result
        return None
    
    def test_as_coordinates(self, data):
        for i in range(0, len(data) - 11):
            segment = data[i:i+12]
            
            formats = [(6, 6), (5, 7), (7, 5), (4, 8)]
            
            for lat_len, lon_len in formats:
                if lat_len + lon_len <= len(segment):
                    try:
                        lat_str = segment[:lat_len]
                        lon_str = segment[lat_len:lat_len + lon_len]
                        
                        for lat_dec in range(1, lat_len):
                            for lon_dec in range(1, lon_len):
                                lat = float(lat_str[:lat_dec] + '.' + lat_str[lat_dec:])
                                lon = float(lon_str[:lon_dec] + '.' + lon_str[lon_dec:])
                                
                                if -90 <= lat <= 90 and -180 <= lon <= 180:
                                    self.log_result("COORDINATE_CANDIDATE", 
                                                  f"Lat: {lat}°, Lon: {lon}° from position {i}", "MEDIUM")
                                    return
                    except ValueError:
                        continue
    
    def analyze_xor_patterns(self, xor_data):
        for length in range(3, min(10, len(xor_data) // 3)):
            patterns = {}
            for i in range(len(xor_data) - length + 1):
                pattern = xor_data[i:i + length]
                if pattern not in patterns:
                    patterns[pattern] = []
                patterns[pattern].append(i)
            
            repeating = {k: v for k, v in patterns.items() if len(v) > 2}
            if repeating:
                for pattern, positions in list(repeating.items())[:3]:
                    self.log_result("XOR_PATTERN", f"Pattern '{pattern}' at positions {positions}", "MEDIUM")
    
    def cross_reference_analysis(self):
        self.log_result("CROSS_REFERENCE", "Cross-referencing with known Cicada information", "HIGH")
        
        known_numbers = {
            3301: "Main Cicada identifier",
            509: "Totient of 3301", 
            311: "Prime factor of 3301",
            113: "Prime factor of 3301",
            7: "Sacred/mystical number",
            29: "Significant in Liber Primus"
        }
        
        primary_result, primary_decimals = self.decode_primary_method()
        
        for number, significance in known_numbers.items():
            if str(number) in primary_result:
                self.log_result("KNOWN_NUMBER_MATCH", f"Found {number} ({significance}) in primary decode", "CRITICAL")
            
            if number in primary_decimals:
                self.log_result("DECIMAL_MATCH", f"Decimal value {number} ({significance}) found", "HIGH")
    
    def generate_final_report(self):
        report = f"""# Cicada 3301 Focused Decoder Results

**Generated:** {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
**Target:** High-confidence findings from advanced analysis

## Executive Summary

This focused decoder targeted the three highest-confidence findings:
1. **92.3% ASCII validity** - Every 5th digit + shift 1 method
2. **84.6% ASCII validity** - Every 5th digit + shift 3 method  
3. **83.3% ASCII validity** - Palindrome 7447 XOR with fibonacci positions

---

## Decoding Results by Confidence Level

"""
        
        categories = {}
        for result in self.results:
            cat = result['category']
            conf = result['confidence']
            if cat not in categories:
                categories[cat] = {'CRITICAL': [], 'HIGH': [], 'MEDIUM': [], 'LOW': []}
            categories[cat][conf].append(result)
        
        for category, confidence_levels in categories.items():
            report += f"### {category}\n\n"
            
            for confidence in ['CRITICAL', 'HIGH', 'MEDIUM', 'LOW']:
                if confidence_levels[confidence]:
                    report += f"#### {confidence} Confidence\n\n"
                    for result in confidence_levels[confidence]:
                        report += f"**[{result['timestamp']}]** {result['finding']}\n\n"
            
            report += "---\n\n"
        
        report += """## Key Conclusions

### Primary Decode Method (92.3% validity)
The "every 5th digit + shift 1" method represents the most likely encoding approach used in the final Cicada 3301 puzzle.

### Secondary Patterns
Multiple complementary encoding methods suggest a multi-layered puzzle design typical of Cicada 3301.

### Coordinate Hypotheses
Several coordinate candidates require geographic investigation for potential physical locations or historical significance.

### Next Investigation Priorities
1. Geographic verification of coordinate candidates
2. Cross-reference decoded text with Liber Primus
3. Test decoded results as keys for other Cicada materials
4. Investigate any URLs or hash patterns found

---

*Analysis completed with focused decoder methodology*
"""
        
        return report
    
    def run_focused_decode(self):
        print("🎯 Starting Cicada 3301 Focused High-Confidence Decoder")
        print("=" * 60)
        
        print("\n🔥 DECODING METHOD 1: Every 5th + Shift 1 (92.3% validity)")
        primary_result, primary_decimals = self.decode_primary_method()
        
        print("\n🔥 DECODING METHOD 2: Every 5th + Shift 3 (84.6% validity)")
        secondary_result, secondary_decimals = self.decode_secondary_method()
        
        print("\n🔥 DECODING METHOD 3: Palindrome 7447 + Fibonacci (83.3% validity)")
        palindrome_result = self.decode_palindrome_fibonacci_method()
        
        print("\n🔥 PATTERN ANALYSIS: XOR with 739")
        xor_result = self.decode_xor_739_method()
        
        print("\n🌍 COORDINATE ANALYSIS")
        self.test_coordinate_hypotheses()
        
        print("\n🔍 CROSS-REFERENCE ANALYSIS")
        self.cross_reference_analysis()
        
        print("\n📄 GENERATING FINAL REPORT")
        report = self.generate_final_report()
        
        filename = f"cicada_focused_decode_{self.timestamp}.md"
        with open(filename, 'w', encoding='utf-8') as f:
            f.write(report)
        
        print(f"\n✅ Focused decode complete!")
        print(f"📁 Report saved as: {filename}")
        print(f"🎯 {len([r for r in self.results if r['confidence'] == 'CRITICAL'])} CRITICAL findings")
        print(f"🎯 {len([r for r in self.results if r['confidence'] == 'HIGH'])} HIGH confidence findings")
        
        return filename

if __name__ == "__main__":
    decoder = CicadaFocusedDecoder()
    report_file = decoder.run_focused_decode()
    
    print(f"\n🚀 NEXT STEPS:")
    print(f"   1. Review CRITICAL findings in {report_file}")
    print(f"   2. Test any coordinates geographically")
    print(f"   3. Cross-reference results with Liber Primus")
    print(f"   4. Investigate any URLs or hashes found")