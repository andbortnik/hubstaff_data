from dominate.tags import table, tr, td, html, body, div, tbody


def render_html_table(rows):
    h = html()
    with h.add(body()).add(div(id='content')):
        with table().add(tbody()):
            for row in rows:
                l = tr()
                for cell in row:
                    l.add(td(cell))
    return h.render()
