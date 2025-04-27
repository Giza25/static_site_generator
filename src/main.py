from textnode import TextNode, MDTextType

def main():
    a = TextNode("Hello World", MDTextType.NORMAL_TEXT)
    b = TextNode("This is Bold", MDTextType.BOLD_TEXT)
    print(a)
    print(b)
    print(a == b)


main()