import os
from dash.dependencies import Input, Output

from app import app, asset_url


def get_ikernel_img_url(assets_dir):
    imgUrl = ""
    if assets_dir is not None:
        imgUrl = "figures/" + assets_dir + "interaction_kernel.png"
        style = {'display': 'list-item'}
    if not os.path.isfile("assets/" + imgUrl): 
        imgUrl = "placeholders/plot_not_found.png"
        style = {'display': 'none'}
    imgUrl = asset_url + imgUrl
    return imgUrl, imgUrl, style


# Update ikernel tabs
for side in ['left', 'right']:    
    app.callback(
        [Output(f"ikernel_tab_{side}_img", 'src'),
         Output(f"ikernel_tab_{side}_modal_img", 'src'),
         Output(f"ikernel_tab_{side}", 'tab_style')],
        Input(f"date_picker_{side}_output_container", 'children')
    )(get_ikernel_img_url)