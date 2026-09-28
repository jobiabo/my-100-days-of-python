def add_tag(profile, tag):
  updated = profile.copy()
  updated["tag"] = profile["tag"].copy()
  updated["tag"].append(tag)
  return updated

a = {"name": "jane", "tag": ["python"]}
changed = add_tag(a, "go")
print(a)
print(changed)

assert a["tag"] == ["python"]
assert changed["tag"] == ["python", "go"]