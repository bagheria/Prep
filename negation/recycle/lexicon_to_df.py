# %%
import pandas as pd
from pathlib import Path
import yaml


# %%
def yaml_to_panda(filename):
    filepath = Path.cwd() / "negation" / "data" / filename
    with open(filepath) as file:
        yaml_file = yaml.load_all(file, Loader=yaml.SafeLoader)
        i = 0
        for doc in yaml_file:
            if i == 0:
                yaml_panda = pd.DataFrame(data=doc, index=[i])
            else:
                new_row = pd.DataFrame(data=doc, index=[i])
                yaml_panda = pd.concat([yaml_panda, new_row])
            i = i + 1
    return(yaml_panda)


# %%
