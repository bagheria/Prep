# %%
import yaml
import urllib.request


yaml_object = yaml.load_all(urllib.request.urlopen(target_path, data=None))
for doc in yaml_object:
    print(doc["Direction"])

# %%