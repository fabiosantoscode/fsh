import fsh

def test_tokenise():
    assert fsh.tokenise('') == []
    assert fsh.tokenise('foo bar') == ['foo', ' ', 'bar']
    assert fsh.tokenise('$foo') == ['$foo']

def test_parse():
    assert fsh.parse('') == []
    assert fsh.parse('foo bar') == [fsh.Statement('foo', ['bar'])]
    assert fsh.parse('a = b') == [fsh.SetVariable('a', 'b')]

def test_function():
    assert fsh.execute('''function foo {
        echo bar
    }''', {}, {}) == [fsh.Function('foo', [], [['echo', 'bar']])]

