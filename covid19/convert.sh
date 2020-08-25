#!/bin/bash
# Convert Dashboard Notebook to runable python Flask script
# Todo: Replace min_date to actual min date, once all figures are downloaded
jupyter-nbconvert covid19dynstat-dash.ipynb --to script 
cp covid19dynstat-dash.py covid19dynstat-dash_bup.py
#cp covid19dynstat-dash_v1.3.py covid19dynstat-dash.py
sed -i -e "s/from jupyter_dash import JupyterDash/#from jupyter_dash import JupyterDash/g" covid19dynstat-dash.py
sed -i -e "s/JupyterDash.infer_jupyter_proxy_config()/#JupyterDash.infer_jupyter_proxy_config()/g" covid19dynstat-dash.py
sed -i -e "s/get_ipython().system(/#get_ipython().system(/g" covid19dynstat-dash.py
sed -i -e "s/app.run_server(mode=\"external\")/if __name__ == \"__main__\":\n    app.run_server(debug=True)/g" covid19dynstat-dash.py
sed -i -e "s/app = JupyterDash(__name__, external_stylesheets=\[dbc.themes.BOOTSTRAP\])/import os\nbase_url=os.getenv(\"BASE_URL\")\nprefix_path=os.getenv(\"PREFIX_PATH\")\napp = dash.Dash(__name__, external_stylesheets=\[dbc.themes.BOOTSTRAP\])/g" covid19dynstat-dash.py
sed -i -e "s|^asset_url=app.get_asset_url('assets')|asset_url=\"{}{}assets/\".format(base_url, prefix_path)\n#asset_url=app.get_asset_url('assets')|g" covid19dynstat-dash.py
sed -i -e "s|^metadata = pd.read_csv(\"assets/metadata.csv\")|metadata = pd.read_csv(\"/app/assets/metadata.csv\")|g" covid19dynstat-dash.py
sed -i -e "s|^cache_dir = \"./cache\"|cache_dir = \"/app/cache\"|g" covid19dynstat-dash.py
sed -i -e "s|^min_date=dt(2020, 1, 29).date()|min_date=dt(2020, 4, 27).date()#|g" covid19dynstat-dash.py
#sed -i -e "s|^max_date=dt(|max_date=dt.today().date()#|g" covid19dynstat-dash.py
sed -i -e "s|^max_date=|if os.environ.get('MAX_DATE', '<no_max_date>') != '<no_max_date>':\n    max_date=dt.strptime(os.environ.get('MAX_DATE'), '%Y-%m-%d')\nelse:\n    max_date=dt.today().date()\n#max_date=dt.today().date()#|g" covid19dynstat-dash.py
#sed -i -e "s|^init_date=dt(|init_date=dt.today().date()#|g" covid19dynstat-dash.py
sed -i -e "s|^init_date=|if os.environ.get('INIT_DATE', '<no_init_date>') != '<no_init_date>':\n    init_date=dt.strptime(os.environ.get('INIT_DATE'), '%Y-%m-%d')\nelse:\n    init_date=dt.today().date()\n#init_date=dt.today().date()#|g" covid19dynstat-dash.py
sed -i -e "20s|.*|#    app.run_server(debug=True)|g" covid19dynstat-dash.py
#sed -i -e "s|import pandas as pd|#import pandas as pd|g" covid19dynstat-dash.py
cp covid19dynstat-dash.py /etc/j4j/jupyter-jsc-dashboads/covid19/build/app/app.py
