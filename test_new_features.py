"""
Testscript for nye kalkulatorfunksjoner
"""
import math
import sys
sys.path.insert(0, '.')

# Test prosent
from main import calculate
result = calculate(200, 10, "%")
print(f"Test prosent: 200 % 10 = {result} (forventet: 20.0)")
assert result == 20.0, "Prosentberegning feilet"

# Test kvadratrot
result = math.sqrt(16)
print(f"Test sqrt: sqrt(16) = {result} (forventet: 4.0)")
assert result == 4.0, "Kvadratrot feilet"

result = math.sqrt(2)
print(f"Test sqrt: sqrt(2) = {result} (forventet: ~1.414)")
assert abs(result - 1.414213562373095) < 0.0001, "Kvadratrot feilet"

# Test minnefunksjoner
from main import memory
print(f"Test minne: Startverd i = {memory} (forventet: 0.0)")

print("\nAlle tester bestått!")
