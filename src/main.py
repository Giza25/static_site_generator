from textnode import TextNode

def main():
    a = TextNode("Hello World", "Normal Text")
    b = TextNode("This is Bold", "Bold Text")
    print(a)
    print(b)
    print(a == b)


main()