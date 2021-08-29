import xmltodict
import networkx as nx

from webweb import Web
import webweb


def load_bib(path):
    """
    Load bibliography from .bib file.
    You can create the .bib file yourself or download it from Google Scholar.
    Download from Google Scholar:
        1. open your google scholar profile
        2. click the box in the left of `TITLE` (below your avatar)
        3. click 'EXPORT' -> 'BibTeX'
    """
    with open(path) as f:
        data = f.read()

        co_author_lst = list()

        def traverse(ipt):
            author_lst = list()
            try:
                s_idx = ipt.index('author={')
            except ValueError:
                return
            e_idx = ipt.index('},', s_idx)
            authors = ipt[s_idx+8:e_idx].split(' and ')
            for author in authors:
                last_name, first_name = author.split(', ')
                author_lst.append(first_name + ' ' + last_name)
            co_author_lst.append(author_lst)
            print(co_author_lst)
            traverse(ipt[e_idx:])

        traverse(data)

        return co_author_lst


def load_dblp_xml(path):
    """
    Load DBLP author metadata.
    First, load author publication xml file. 
    Download:
        1. open your DBLP author page
        2. the third icon right next your Name, hover and click the `XML` in the dropdown box
        3. save your XML file
    Then this function read your co-authorship records. 
    """
    with open(path) as f:
        data = xmltodict.parse(f.read())

    co_author_lst = list()

    for paper in data['dblpperson']['r']:
        author_lst = list()
        # assumption: the first element of Ordered Dict 'paper' is paper type
        paper_type = list(paper.keys())
        if paper_type[0] in ['article', 'inproceedings']:
            authors = paper[list(paper.keys())[0]]['author']
        else:
            continue

        if len(authors) > 2:
            for author in authors:
                try:
                    name = author['#text']
                except TypeError:
                    continue
                if name[-4:].isnumeric():
                    name = name[:-5]
                if '(-)' in name:
                    name = name.replace('(-)', '')
                author_lst.append(name)
        else:
            continue
        co_author_lst.append(author_lst)

    # len(co-author_lst): number of paper
    # each of 'co-author_lst): list of co-authors of one paper
    return co_author_lst


def build_graph(co_author_lst, min_weight, frequent_co_authors=None, show_percentage_names=0):
    # build graph
    g = nx.Graph()

    # add edges
    for paper_author in co_author_lst:
        for author in paper_author:
            for another_author in paper_author:
                if author != another_author:
                    try:
                        g[author][another_author]['weight'] += .5
                    except KeyError:
                        g.add_weighted_edges_from([[author, another_author, .5]])
                    else:
                        pass

    # for an edge, if its weight (co-author times between two authors) less than 'min_weight', filter it out
    edge_list = [[u, v, w['weight']] for (u, v, w) in g.edges(data=True) if w['weight'] >= min_weight]

    nodes = set([u for (u, v, w) in edge_list]).union(set([v for (u, v, w) in edge_list]))

    degrees = [d for (u, d) in g.degree(nbunch=list(nodes), weight='weight')]

    # 
    percentage_names = None 
    if frequent_co_authors != None and show_percentage_names == 0:
        percentage_names = frequent_co_authors
    elif frequent_co_authors == None and show_percentage_names != 0:
        min_percentage_weight = sorted(degrees, reverse=True)[:int(len(degrees) * (show_percentage_names / 100))][-1]
        percentage_names = [u for (u, d) in g.degree(nbunch=list(nodes), weight='weight') if d >= min_percentage_weight]
        print('The webpage will show following {} names in default:'.format(len(percentage_names)))
        print('\t' + ', '.join(sorted(percentage_names, key=lambda name: name.split(' ')[-1])))
    elif frequent_co_authors == None and show_percentage_names == 0:
        percentage_names = None
    else:
        print("Whether 'frequent_co_authors' should be 'None' or 'show_percentage_names' should be zero.")
        exit()
        
    return edge_list, percentage_names


def read_and_write_html(path):
    with open(path, 'r') as f:
        html_file = f.read()
        start_idx = html_file.index('<script type="text/javascript">var wwdata')
        end_idx = html_file.index('</script>', start_idx) + 9
        html_data = html_file[start_idx:end_idx]
    
    with open('./template.html', 'r') as f:
        html_file = f.read()
        start_idx = html_file.index('<script\n        type="text/javascript">var wwdata')
        end_idx = html_file.index('</script>', start_idx) + 9
        # print(html_file[start_idx:end_idx])
        html_final = html_file.replace(html_file[start_idx:end_idx], html_data)
    
    with open(path, 'w') as f:
        f.write(html_final)


def main(name,
         data='bib',
         display_name='Xovee Xu',
         min_edge_weight=1,
         color_by='strength',
         size_by='strength',
         charge=150,
         link_length=150,
         #  color_map='Reds',
         scale_link_opacity=1,
         scale_link_width=1,
         name_to_match='Xovee Xu',
         radius=10,
         show_node_names=0,
         hide_menu=0,
         show_legend=1,
         frequent_co_authors=None,
         show_percentage_names=0,
         canvas_height=700,
         canvas_width=1000,
         ):

    # load data
    if data == 'xml':
        co_author_lst = load_dblp_xml(path=name + '.xml')
    elif data == 'bib':
        co_author_lst = load_bib(path=name + '.bib')
    else:
        print("Wrong 'data' keyword, should be 'bib' or 'xml'.")
        exit()

    # build graph
    edge_list, percentage_names = build_graph(co_author_lst, 
        min_edge_weight, frequent_co_authors=frequent_co_authors, 
        show_percentage_names=show_percentage_names)

    number_co_authors = len(set([u for (u, v, w) in edge_list] + [v for (u, v, w) in edge_list]))

    # build webweb's web
    web = Web(title=name_to_match)


    web.networks.xovee(
        adjacency=edge_list,
    )

    # display options
    web.display.colorBy = color_by
    web.display.sizeBy = size_by
    web.display.charge = charge
    web.display.linkLength = link_length
    web.display.scaleLinkOpacity = scale_link_opacity
    web.display.scaleLinkWidth = scale_link_width
    web.display.nameToMatch = name_to_match
    web.display.radius = radius
    web.display.showNodeNames = show_node_names
    web.display.hideMenu = hide_menu
    web.display.showLegend = show_legend
    web.display.frequentCoAuthors = percentage_names
    web.display.h = canvas_height
    web.display.w = canvas_width
    web.display.numberCoAuthor = number_co_authors
    web.display.displayName = display_name

    # web.show()

    web.save(name + '.html')

    read_and_write_html(name + '.html')

    # change display name


if __name__ == '__main__':
    args = {
        'name': 'xovee-xu',
        'data': 'bib',  # 'bib' or 'xml'
        'display_name': 'Xovee Xu',
        'min_edge_weight': 1,
        'color_by': 'strength',  # 'degree' or 'strength'
        'size_by': 'strength',  # 'degree' or 'strength'
        'charge': 256,
        'link_length': 200,
        'scale_link_opacity': 1,
        'scale_link_width': 1,
        'name_to_match': "",
        'radius': 15,
        'show_node_names': 0,
        'hide_menu': 0,
        'show_legend': 0,
        'show_percentage_names': 10,  # percentage; 0: don't show; perferably 5-15%;
        'frequent_co_authors': None,  # a list of co-author names
        'canvas_height': 700,
        'canvas_width': 1000,
    }

    main(**args)


