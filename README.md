# static_site
- [HTML elements reference](https://developer.mozilla.org/en-US/docs/Web/HTML/Reference/Elements)  
- [Markdown cheatsheet](https://www.markdownguide.org/cheat-sheet/)  
- [Python http server](https://docs.python.org/3/library/http.server.html) - `python3 -m http.server` serves files relative to current directory. port can be specified (default is 8000)
- [Python data model](https://docs.python.org/3/reference/datamodel.html#object.__eq__) - section 3.3 lists special method names such as `__eq__`, `__repr__` etc  
- [Python unittest from std lib](https://docs.python.org/3/library/unittest.html) - unittesting in python
- [Python regex module](https://docs.python.org/3/library/re.html)
- [Regex site](https://regexr.com/) - amazing regex site
    - [Coding train video](https://www.youtube.com/watch?v=c9HbsUSWilw) - talks about capture groups and at 8:38 onwards, talks about greedy vs lazy quantifiers


### **markdown\_blocks.py**
>markdown\_to\_blocks(markdown: str) -> List\[str]  
>- returns list of blocks (List\[str]) from markdown (splits  "\\n\\n")  

>block\_to\_block\_type(block: str) -> BlockType
>- returns BlockType of block based on starting/ending characters 

### **class BlockType(Enum):**  
&nbsp;   PARAGRAPH = "PARAGRAPH" -> `<p>`  
&nbsp;   HEADING = "HEADING" -> `<h?>` (might need to use parent + 1)   
&nbsp;   CODE = "CODE" -> `<code>`  
&nbsp;   QUOTE = "QUOTE" -> `<blockquote>`  
&nbsp;   UNORDERED\_LIST = "UNORDERED\_LIST" -> `<ul>`  
&nbsp;   ORDERED\_LIST = "ORDERED\_LIST" -> `<ol>`  

### **textnode.py**

>text\_node\_to\_html\_node(text\_node: TextNode) -> LeafNode  
>- returns LeafNode with tag corresponding to inline tag, value set as text where appropriate (eg: text for text/italic/bold/link, "" for image), properties set to respective 

### **inline\_markdown.py**

>text\_to\_textnodes(text: str) -> List\[TextNode]



