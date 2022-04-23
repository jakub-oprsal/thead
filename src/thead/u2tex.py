dictionary = {
    'À': r'\`A', 'Á': r"\'A", 'Â': r'\^A', 'Ã': r'\~A', 'Ä': r'\"A',
    'Å': r'\r{A}', 'Æ': r'\AE', 'Ç': r'\c{C}', 'È': r'\`E', 'É': r"\'E",
    'Ê': r'\^E', 'Ë': r'\"E', 'Ì': r'\`I', 'Í': r"\'I", 'Î': r'\^I',
    'Ï': r'\"I', 'Ð': r'\DH', 'Ñ': r'\~N', 'Ò': r'\`O', 'Ó': r"\'O",
    'Ô': r'\^O', 'Õ': r'\~O', 'Ö': r'\"O', 'Ø': r'\O', 'Ù': r'\`U',
    'Ú': r"\'U", 'Û': r'\^U', 'Ü': r'\"U', 'Ý': r"\'Y", 'ß': r'\ss',
    'à': r'\`a', 'á': r"\'a", 'â': r'\^a', 'ã': r'\~a', 'ä': r'\"a',
    'å': r'\r{a}', 'æ': r'\ae', 'ç': r'\c{c}', 'è': r'\`e', 'é': r"\'e",
    'ê': r'\^e', 'ë': r'\"e', 'ì': r'\`i', 'í': r"\'i", 'î': r'\^i',
    'ï': r'\"i', 'ð': r'\dh', 'ñ': r'\~n', 'ò': r'\`o', 'ó': r"\'o",
    'ô': r'\^o', 'õ': r'\~o', 'ö': r'\"o', 'ø': r'\o', 'ù': r'\`u',
    'ú': r"\'u", 'û': r'\^u', 'ü': r'\"u', 'ý': r"\'y", 'ÿ': r'\"y',
    'Ā': r'\=A', 'ā': r'\=a', 'Ă': r'\u{A}', 'ă': r'\u{a}', 'Ą': r'\k{A}',
    'ą': r'\k{a}', 'Ć': r"\'C", 'ć': r"\'c", 'Ĉ': r'\^C', 'ĉ': r'\^c',
    'Ċ': r'\.C', 'ċ': r'\.c', 'Č': r'\v{C}', 'č': r'\v{c}', 'Ď': r'\v{D}',
    'ď': r'\v{d}', 'Đ': r'\DJ', 'đ': r'\dj', 'Ē': r'\=E', 'ē': r'\=e',
    'Ĕ': r'\u{E}', 'ĕ': r'\u{e}', 'Ė': r'\.E', 'ė': r'\.e', 'Ę': r'\k{E}',
    'ę': r'\k{e}', 'Ě': r'\v{E}', 'ě': r'\v{e}', 'Ĝ': r'\^G', 'ĝ': r'\^g',
    'Ğ': r'\u{G}', 'ğ': r'\u{g}', 'Ġ': r'\.G', 'ġ': r'\.g', 'Ģ': r'\c{G}',
    'ģ': r'\c{g}', 'Ĥ': r'\^H', 'ĥ': r'\^h', 'Ĩ': r'\~I', 'ĩ': r'\~i',
    'Ī': r'\=I', 'ī': r'\=i', 'Ĭ': r'\u{I}', 'ĭ': r'\u{i}', 'Į': r'\k{I}',
    'į': r'\k{i}', 'İ': r'\.I', 'Ĵ': r'\^J', 'ĵ': r'\^j', 'Ķ': r'\c{K}',
    'ķ': r'\c{k}', 'Ĺ': r"\'L", 'ĺ': r"\'l", 'Ļ': r'\c{L}', 'ļ': r'\c{l}',
    'Ľ': r'\v{L}', 'ľ': r'\v{l}', 'Ł': r'\L', 'ł': r'\l', 'Ń': r"\'N",
    'ń': r"\'n", 'Ņ': r'\c{N}', 'ņ': r'\c{n}', 'Ň': r'\v{N}', 'ň': r'\v{n}',
    'Ŋ': r'\NG', 'ŋ': r'\ng', 'Ō': r'\=O', 'ō': r'\=o', 'Ŏ': r'\u{O}',
    'ŏ': r'\u{o}', 'Ő': r'\H{O}', 'ő': r'\H{o}', 'Ŕ': r"\'R", 'ŕ': r"\'r",
    'Ŗ': r'\c{R}', 'ŗ': r'\c{r}', 'Ř': r'\v{R}', 'ř': r'\v{r}', 'Ś': r"\'S",
    'ś': r"\'s", 'Ŝ': r'\^S', 'ŝ': r'\^s', 'Ş': r'\c{S}', 'ş': r'\c{s}',
    'Š': r'\v{S}', 'š': r'\v{s}', 'Ţ': r'\c{T}', 'ţ': r'\c{t}', 'Ť': r'\v{T}',
    'ť': r'\v{t}', 'Ũ': r'\~U', 'ũ': r'\~u', 'Ū': r'\=U', 'ū': r'\=u',
    'Ŭ': r'\u{U}', 'ŭ': r'\u{u}', 'Ů': r'\r{U}', 'ů': r'\r{u}', 'Ű': r'\H{U}',
    'ű': r'\H{u}', 'Ų': r'\k{U}', 'ų': r'\k{u}', 'Ŵ': r'\^W', 'ŵ': r'\^w',
    'Ŷ': r'\^Y', 'ŷ': r'\^y', 'Ÿ': r'\"Y', 'Ź': r"\'Z", 'ź': r"\'z",
    'Ż': r'\.Z', 'ż': r'\.z', 'Ž': r'\v{Z}', 'ž': r'\v{z}'}


def u2tex(string):
   return ''.join(dictionary.get(char, char) for char in string)