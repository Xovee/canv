# CANV: Co-Authorship Network Visualization

![Example](asset/teaser.png)

CANV is an interactive co-authorship network visualization tool based on [webweb](https://github.com/dblarremore/webweb). See an example above (my network) or at [here](https://xovee.cn/html/canv/xovee-xu.html). You can use this tool to create a standalone webpage containing your co-authorship network. 

## Dependency

```shell
pip install -r requirements.txt
```

## Usage

You can create your co-authorship network with a few easy steps in no time.

1. Open your [dblp](https://dblp.org) author page, download your bibliographic data, e.g.,
`xovee-xu.xml`  
<img src="asset/download_data.png" alt="download data" width="250"/>

2. Change variable `name` in `args` in `canv.py` to match the name of your data file, e.g., `'name': 'xovee-xu'` 

3. Run [canv.py](./canv.py), then you have `xovee-xu.html`, that's all! 

## Option

There are several options you can customize your CANV page.

- `name`: your data file name
- `display_name`: name displayed in webpage
- `min_edge_weight`: filter out infrequent co-authors
- `link_length`: you know what
- `name_to_match`: show someone's name in default
- `radius`: node size
- `show_node_names`: show all co-author names in default or not
- `show_percentage_names`: show top frequented co-author names (%), preferably 5-15% if you have a large number of co-authors; if this variable is not `0`, `frequent_co_authors` must be `None`
- `frequent_co_authors`: a list contains co-author names, the webpage will display their names in default; if `frequent_co_authors` is not `None`, `show_percentage_names` must be `0`
- `canvas_height`
- `canvas_width`

Check [canv.py](./canv.py) for more. 

## Deep Customization

You can directly edit [template.html](./template.html) to deeply customize your page. Some examples:
- If you want to change node colormap, search `d3.interpolateReds(webweb.scales.colors.scalar(x))` in [template.html](./template.html) and replace it within the color you like.
- If you want to regularize node color/size values, modify the `getRawNodeValues()` function, e.g., `rawValues[i] = val;` to `rawValues[i] = Math.log(val)`

## Todos

- [ ] Support Google Scholar data
- [ ] Colormap selection
- [ ] Optimize mobile experience

## More Examples

- Prof. [Andrew Y. Ng](https://xovee.cn/html/canv/andrew-y-ng.html)
![](./asset/andrew-ng.png)

## Acknowledgment

Thanks to [webweb](https://github.com/dblarremore/webweb) and [dblp](https://dblp.org) team.

## LICENSE

GPL-3.0 License

## Contact

If you notice any bugs or have suggestions, please contact me at `xovee at ieee.org`
