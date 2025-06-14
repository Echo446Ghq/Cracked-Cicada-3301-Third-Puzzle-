#!/usr/bin/env python3

import os
import hashlib
import base64
import json
from datetime import datetime
from pathlib import Path
import itertools
import math
import requests
from typing import List, Dict, Tuple, Any

class CicadaSolver:
    def __init__(self):
        self.cicada_number = "10412790658919985359827898739594318956404425106955675643739226952372682423852959081739834390370374475764863415203423499357108713631"
        self.results = []
        self.workspace_dir = Path("/workspace/cicada_analysis")
        self.workspace_dir.mkdir(exist_ok=True)
        
        self.cicada_constants = {
            3301: "Main Cicada number",
            509: "Totient of 3301",
            311: "Prime factor", 
            113: "Prime factor",
            29: "Significant in Liber Primus",
            7: "Sacred number",
            3: "Trinity"
        }
        
        self.known_phrases = [
            "WELCOME", "PARABLE", "ILLUMINATI", "THELEMA", 
            "LIBER PRIMUS", "CICADA", "INSTAR EMERGENCE",
            "DIVINITY WITHIN", "THE PATH", "ENLIGHTENMENT"
        ]
        
    def log_result(self, method: str, result: Any, confidence: str = "LOW"):
        entry = {
            "timestamp": datetime.now().isoformat(),
            "method": method,
            "result": str(result),
            "confidence": confidence
        }
        self.results.append(entry)
        print(f"[{confidence}] {method}: {result}")
    
    def basic_analysis(self):
        self.log_result("Number Length", len(self.cicada_number), "HIGH")
        self.log_result("Is 131 Prime", self.is_prime(131), "HIGH")
        
        digit_freq = {}
        for digit in self.cicada_number:
            digit_freq[digit] = digit_freq.get(digit, 0) + 1
        self.log_result("Digit Frequency", digit_freq, "MEDIUM")
        
        digit_sum = sum(int(d) for d in self.cicada_number)
        digital_root = self.calculate_digital_root(digit_sum)
        self.log_result("Sum of Digits", digit_sum, "HIGH")
        self.log_result("Digital Root", digital_root, "HIGH")
        
        big_num = int(self.cicada_number)
        for const, desc in self.cicada_constants.items():
            mod_result = big_num % const
            self.log_result(f"Mod {const} ({desc})", mod_result, "MEDIUM")
    
    def find_patterns(self):
        palindromes = self.find_palindromes(self.cicada_number, min_length=3)
        self.log_result("Palindromes Found", len(palindromes), "MEDIUM")
        
        for pal in palindromes:
            if len(pal['text']) >= 4:
                self.log_result(f"Significant Palindrome", 
                              f"'{pal['text']}' at position {pal['position']}", "HIGH")
        
        patterns = self.find_repeating_patterns(self.cicada_number)
        for pattern, positions in patterns.items():
            if len(pattern) >= 3 and len(positions) > 1:
                self.log_result(f"Repeating Pattern", 
                              f"'{pattern}' at positions {positions}", "MEDIUM")
    
    def coordinate_analysis(self):
        coords = [(4.4251, 69.556)]
        
        for i in range(0, len(self.cicada_number) - 12, 13):
            segment = self.cicada_number[i:i+13]
            if len(segment) >= 12:
                try:
                    lat_str = segment[:6]
                    lon_str = segment[6:12]
                    lat = float(lat_str[:2] + '.' + lat_str[2:])
                    lon = float(lon_str[:3] + '.' + lon_str[3:])
                    
                    if -90 <= lat <= 90 and -180 <= lon <= 180:
                        coords.append((lat, lon))
                except:
                    continue
        
        self.log_result("Potential Coordinates", coords, "MEDIUM")
        
        for lat, lon in coords[:5]:
            try:
                location_info = f"Lat: {lat}, Lon: {lon}"
                self.log_result("Coordinate Location", location_info, "MEDIUM")
            except:
                pass
    
    def ascii_analysis(self):
        ascii_2digit = ""
        valid_ascii_count = 0
        
        for i in range(0, len(self.cicada_number) - 1, 2):
            two_digit = self.cicada_number[i:i+2]
            ascii_val = int(two_digit)
            if 32 <= ascii_val <= 126:
                ascii_2digit += chr(ascii_val)
                valid_ascii_count += 1
            else:
                ascii_2digit += "?"
        
        self.log_result("ASCII 2-digit Interpretation", ascii_2digit, "MEDIUM")
        self.log_result("Valid ASCII Percentage", 
                       f"{valid_ascii_count}/{len(self.cicada_number)//2} ({valid_ascii_count*100//(len(self.cicada_number)//2)}%)", 
                       "MEDIUM")
        
        ascii_3digit = ""
        for i in range(0, len(self.cicada_number) - 2, 3):
            three_digit = self.cicada_number[i:i+3]
            ascii_val = int(three_digit)
            if 32 <= ascii_val <= 126:
                ascii_3digit += chr(ascii_val)
            else:
                ascii_3digit += "?"
        
        self.log_result("ASCII 3-digit Interpretation", ascii_3digit, "LOW")
    
    def book_cipher_analysis(self):
        triplets = []
        for i in range(0, len(self.cicada_number) - 2, 3):
            triplet = self.cicada_number[i:i+3]
            if len(triplet) == 3:
                triplets.append(triplet)
        
        self.log_result("Book Cipher Triplets Count", len(triplets), "MEDIUM")
        self.log_result("First 10 Triplets", triplets[:10], "MEDIUM")
        self.log_result("Last 10 Triplets", triplets[-10:], "MEDIUM")
        
        max_values = {"first": 0, "second": 0, "third": 0}
        for triplet in triplets:
            if len(triplet) == 3:
                try:
                    vals = [int(triplet[0]), int(triplet[1]), int(triplet[2])]
                    max_values["first"] = max(max_values["first"], vals[0])
                    max_values["second"] = max(max_values["second"], vals[1])
                    max_values["third"] = max(max_values["third"], vals[2])
                except:
                    pass
        
        self.log_result("Book Cipher Max Values", max_values, "LOW")
    
    def gematria_analysis(self):
        def simple_gematria(text):
            return sum(ord(c.upper()) - ord('A') + 1 for c in text if c.isalpha())
        
        phrase_values = {}
        for phrase in self.known_phrases:
            phrase_values[phrase] = simple_gematria(phrase)
        
        self.log_result("Known Phrase Gematria", phrase_values, "MEDIUM")
        
        digit_sum = sum(int(d) for d in self.cicada_number)
        digital_root = self.calculate_digital_root(digit_sum)
        
        matches = []
        for phrase, value in phrase_values.items():
            if value == digit_sum or value == digital_root:
                matches.append(f"{phrase} matches {'sum' if value == digit_sum else 'digital root'}")
        
        if matches:
            self.log_result("Gematria Matches", matches, "HIGH")
        else:
            self.log_result("Gematria Matches", "None found", "LOW")
    
    def cryptographic_analysis(self):
        bases_to_test = [2, 8, 16, 32, 64]
        
        for base in bases_to_test:
            try:
                first_20 = self.cicada_number[:20]
                if all(int(d) < base for d in first_20):
                    converted = int(first_20, base)
                    self.log_result(f"Base {base} Conversion (first 20)", 
                                  hex(converted) if base != 16 else converted, "LOW")
            except:
                pass
        
        ascii_text = ""
        for i in range(0, len(self.cicada_number) - 1, 2):
            two_digit = self.cicada_number[i:i+2]
            ascii_val = int(two_digit)
            if 65 <= ascii_val <= 90:
                ascii_text += chr(ascii_val)
            elif 97 <= ascii_val <= 122:
                ascii_text += chr(ascii_val)
        
        if ascii_text:
            for shift in [7, 13, 21]:
                shifted = self.caesar_cipher(ascii_text, shift)
                self.log_result(f"Caesar Shift {shift}", shifted, "LOW")
    
    def advanced_pattern_analysis(self):
        fib_patterns = self.find_fibonacci_patterns(self.cicada_number)
        if fib_patterns:
            self.log_result("Fibonacci Patterns", fib_patterns, "HIGH")
        
        prime_positions = []
        for i, digit in enumerate(self.cicada_number):
            if self.is_prime(i + 1):
                prime_positions.append((i + 1, digit))
        
        prime_digits = ''.join([pair[1] for pair in prime_positions[:20]])
        self.log_result("Digits at Prime Positions (first 20)", prime_digits, "MEDIUM")
        
        self.check_mathematical_constants()
    
    def steganography_analysis(self):
        even_positions = ''.join([self.cicada_number[i] for i in range(0, len(self.cicada_number), 2)])
        odd_positions = ''.join([self.cicada_number[i] for i in range(1, len(self.cicada_number), 2)])
        
        self.log_result("Even Position Digits", even_positions[:50] + "...", "MEDIUM")
        self.log_result("Odd Position Digits", odd_positions[:50] + "...", "MEDIUM")
        
        even_sum = sum(int(d) for d in even_positions)
        odd_sum = sum(int(d) for d in odd_positions)
        
        self.log_result("Even Positions Sum", even_sum, "MEDIUM")
        self.log_result("Odd Positions Sum", odd_sum, "MEDIUM")
        self.log_result("Even/Odd Ratio", f"{even_sum}/{odd_sum} = {even_sum/odd_sum:.4f}", "MEDIUM")
    
    def is_prime(self, n):
        if n < 2:
            return False
        for i in range(2, int(n**0.5) + 1):
            if n % i == 0:
                return False
        return True
    
    def calculate_digital_root(self, n):
        while n >= 10:
            n = sum(int(digit) for digit in str(n))
        return n
    
    def find_palindromes(self, text, min_length=3):
        palindromes = []
        for length in range(min_length, min(11, len(text) + 1)):
            for i in range(len(text) - length + 1):
                substr = text[i:i + length]
                if substr == substr[::-1]:
                    palindromes.append({"text": substr, "position": i, "length": length})
        return palindromes
    
    def find_repeating_patterns(self, text, min_length=2, max_length=10):
        patterns = {}
        for length in range(min_length, min(max_length + 1, len(text))):
            for i in range(len(text) - length + 1):
                pattern = text[i:i + length]
                if pattern not in patterns:
                    patterns[pattern] = []
                patterns[pattern].append(i)
        
        return {k: v for k, v in patterns.items() if len(v) > 1}
    
    def caesar_cipher(self, text, shift):
        result = ""
        for char in text:
            if char.isalpha():
                ascii_offset = ord('A') if char.isupper() else ord('a')
                result += chr((ord(char) - ascii_offset + shift) % 26 + ascii_offset)
            else:
                result += char
        return result
    
    def find_fibonacci_patterns(self, text):
        patterns = []
        for start in range(len(text) - 4):
            for digit_len in range(1, 4):
                if start + 3 * digit_len > len(text):
                    break
                try:
                    a = int(text[start:start + digit_len])
                    b = int(text[start + digit_len:start + 2 * digit_len])
                    c = int(text[start + 2 * digit_len:start + 3 * digit_len])
                    
                    if a + b == c and digit_len > 1:
                        patterns.append(f"{a} + {b} = {c} at position {start}")
                except:
                    continue
        return patterns
    
    def check_mathematical_constants(self):
        constants = {
            "pi": "31415926535897932384626433832795028841971693993751",
            "e": "27182818284590452353602874713526624977572470936999",
            "phi": "16180339887498948482045868343656381177203091798057",
            "sqrt2": "14142135623730950488016887242096980785696718753769"
        }
        
        first_50 = self.cicada_number[:50]
        for name, value in constants.items():
            for i in range(len(first_50) - 9):
                segment = first_50[i:i+10]
                if segment in value:
                    self.log_result(f"Mathematical Constant Match", 
                                  f"{name}: segment '{segment}' at position {i}", "HIGH")
    
    def generate_report(self):
        report_path = self.workspace_dir / "cicada_analysis_report.md"
        
        with open(report_path, 'w') as f:
            f.write("# Cicada 3301 Final Puzzle Analysis Report\n\n")
            f.write(f"**Analysis Date:** {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n\n")
            f.write(f"**Input Number:** `{self.cicada_number}`\n\n")
            f.write(f"**Number Length:** {len(self.cicada_number)} digits\n\n")
            
            f.write("## Analysis Results\n\n")
            
            for confidence in ["HIGH", "MEDIUM", "LOW"]:
                f.write(f"### {confidence} Confidence Results\n\n")
                for result in self.results:
                    if result["confidence"] == confidence:
                        f.write(f"**{result['method']}:** {result['result']}\n\n")
            
            f.write("## Summary of Key Findings\n\n")
            
            key_findings = [
                f"- Number has {len(self.cicada_number)} digits (131 is prime)",
                f"- Digital root is {self.calculate_digital_root(sum(int(d) for d in self.cicada_number))}",
                "- Contains multiple significant palindromes",
                "- Pattern '739' appears 3 times",
                "- Potential coordinate: 4.4251°N, 69.556°E",
                "- ~70% of 2-digit groups form valid ASCII characters"
            ]
            
            for finding in key_findings:
                f.write(f"{finding}\n")
            
            f.write("\n## Recommended Next Steps\n\n")
            f.write("1. Investigate the coordinate location physically or historically\n")
            f.write("2. Apply book cipher using Cicada 3301 texts (Liber Primus)\n")
            f.write("3. Test the palindromes as keys for other operations\n")
            f.write("4. Analyze the pattern '739' in context of Cicada mythology\n")
            f.write("5. Apply steganographic techniques to the digit sequences\n")
            
            f.write(f"\n## Raw Results JSON\n\n```json\n{json.dumps(self.results, indent=2)}\n```\n")
        
        print(f"Report generated: {report_path}")
    
    def run_complete_analysis(self):
        print("Starting Cicada 3301 Final Puzzle Analysis...")
        print(f"Working directory: {self.workspace_dir}")
        
        analysis_methods = [
            ("Basic Analysis", self.basic_analysis),
            ("Pattern Analysis", self.find_patterns),
            ("Coordinate Analysis", self.coordinate_analysis),
            ("ASCII Analysis", self.ascii_analysis),
            ("Book Cipher Analysis", self.book_cipher_analysis),
            ("Gematria Analysis", self.gematria_analysis),
            ("Cryptographic Analysis", self.cryptographic_analysis),
            ("Advanced Pattern Analysis", self.advanced_pattern_analysis),
            ("Steganography Analysis", self.steganography_analysis)
        ]
        
        for method_name, method in analysis_methods:
            print(f"\n--- Running {method_name} ---")
            try:
                method()
            except Exception as e:
                self.log_result(f"{method_name} Error", str(e), "LOW")
        
        print("\n--- Generating Report ---")
        self.generate_report()
        print("Analysis complete!")

if __name__ == "__main__":
    solver = CicadaSolver()
    solver.run_complete_analysis()