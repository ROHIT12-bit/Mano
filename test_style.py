from helper.utils import big_and_nice

test_text = "Hello World 123 {placeholder} <tag>http://url.com</tag> (bracket)"
result = big_and_nice(test_text)
print(f"Original: {test_text}")
print(f"Result: {result}")

# Expected:
# H -> 𝗛
# e -> 𝗲
# ...
# {placeholder} -> {placeholder} (skipped)
# <tag> -> <tag> (skipped)
