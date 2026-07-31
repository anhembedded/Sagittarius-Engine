import timeit
import io
import sys

setup = """
import io
import sys

components = {f"comp_{i}": f"state_{i}" for i in range(1000)}

def orig():
    old_stdout = sys.stdout
    sys.stdout = io.StringIO()
    try:
        for comp, state in components.items():
            print(f" - {comp.capitalize()}: {state}")
    finally:
        sys.stdout = old_stdout

def optimized():
    old_stdout = sys.stdout
    sys.stdout = io.StringIO()
    try:
        if components:
            print("\\n".join(f" - {comp.capitalize()}: {state}" for comp, state in components.items()))
    finally:
        sys.stdout = old_stdout
"""

orig_time = timeit.timeit("orig()", setup=setup, number=1000)
opt_time = timeit.timeit("optimized()", setup=setup, number=1000)

print(f"Original: {orig_time:.4f}s")
print(f"Optimized: {opt_time:.4f}s")
print(f"Speedup: {orig_time / opt_time:.2f}x")
