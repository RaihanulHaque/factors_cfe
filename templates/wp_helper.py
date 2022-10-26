class wp:
    def __init__(self):
        pass

    def wp_h2(self, text):
        return f"<!-- wp:heading {{\"level\":2}} --><h2>{text}</h2><!-- /wp:heading -->"

    def wp_h3(self, text):
        return f"<!-- wp:heading {{\"level\":3}} --><h3>{text}</h3><!-- /wp:heading -->"

    def wp_paragraph(self, text):
        return f"<!-- wp:paragraph --><p>{text}</p><!-- /wp:paragraph -->"

    def wp_table(self, text):
        table = f"""<!-- wp:table {{\"hasFixedLayout\":true,\"className\":\" is -style-stripes prime-factorization-table\"}} -->
        <figure class=\"wp-block-table is-style-stripes prime-factorization-table\">
        <table class=\"has-fixed-layout\">
            <tbody>
                {text}
            </tbody>
        </table>
        <figcaption>Prime Factorization of {self.n}</figcaption>
        </figure>
        <!-- /wp:table -->"""
        return table

    def wp_paragraph_center(self, text):
        return f"<!-- wp:paragraph {{\"align\":\"center\"}} --><p class = \"has-text-align-center\" >{text}</p> <!-- /wp:paragraph -->"

    def image_add_tree(self):
        locString = f"<!-- wp:image {{\"id\":452,\"sizeSlug\":\"full\",\"linkDestination\":\"none\" }} -->"
        locString += f"<figure class=\"wp-block-image size-full\"><img src=\"https://calculator4engineers.com/wp-content/uploads/2022/10/factor-tree-method.jpg\" alt=\"\" class=\"wp-image-452\"/></figure>"
        locString += "<!-- /wp:image -->"
        return locString

    def image_add_division(self):
        locString = f"<!-- wp:image {{\"id\":471,\"sizeSlug\":\"full\",\"linkDestination\":\"none\" }} -->"
        locString += f"<figure class=\"wp-block-image size-full\"><img src=\"https://calculator4engineers.com/wp-content/uploads/2022/10/division-method.jpg\" alt=\"\" class=\"wp-image-471\"/></figure>"
        locString += "<!-- /wp:image -->"
        return locString

    def sub(self, text):
        return f"<sub>{text}</sub>"

    def sup(self, text):
        return f"<sup>{text}</sup>"

    def strong(self, text):
        return f"<strong>{text}</strong>"
