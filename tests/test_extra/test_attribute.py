"""Test attribute selectors."""
import soupsieve as sv
from .. import util


class TestAttribute(util.TestCase):
    """Test attribute selectors."""

    MARKUP = """
    <div id="div">
    <p id="0">Some text <span id="1"> in a paragraph</span>.</p>
    <a id="2" href="http://google.com">Link</a>
    <span id="3">Direct child</span>
    <pre id="pre">
    <span id="4">Child 1</span>
    <span id="5">Child 2</span>
    <span id="6">Child 3</span>
    </pre>
    </div>
    """

    def test_attribute_not_equal_no_quotes(self):
        """Test attribute with value that does not equal specified value (no quotes)."""

        # No quotes
        self.assert_selector(
            self.MARKUP,
            'body [id!=\\35]',
            ["div", "0", "1", "2", "3", "pre", "4", "6"],
            flags=util.HTML5
        )

    def test_attribute_not_equal_quotes(self):
        """Test attribute with value that does not equal specified value (quotes)."""

        # Quotes
        self.assert_selector(
            self.MARKUP,
            "body [id!='5']",
            ["div", "0", "1", "2", "3", "pre", "4", "6"],
            flags=util.HTML5
        )

    def test_attribute_not_equal_double_quotes(self):
        """Test attribute with value that does not equal specified value (double quotes)."""

        # Double quotes
        self.assert_selector(
            self.MARKUP,
            'body [id!="5"]',
            ["div", "0", "1", "2", "3", "pre", "4", "6"],
            flags=util.HTML5
        )

    def test_bad_attribute_unclused(self):
        """Test bad attribute fails for syntax error, not timeout error."""

        self.assert_raises_no_timeout('[a="' + ('x' * 300), sv.SelectorSyntaxError)

    def test_bad_attribute_unclosed_single_quote(self):
        """Test bad attribute with an unclosed single quoted value fails for syntax error, not timeout error."""

        self.assert_raises_no_timeout("[a='" + ('x' * 300), sv.SelectorSyntaxError)

    def test_bad_attribute_unclosed_escaped_newlines(self):
        """Test bad attribute with unclosed value of escaped newlines fails for syntax error, not timeout error."""

        self.assert_raises_no_timeout('[a="' + ('\\\r' * 300), sv.SelectorSyntaxError)
        self.assert_raises_no_timeout("[a='" + ('\\\f' * 300), sv.SelectorSyntaxError)

    def test_attribute_quoted_escaped_newlines(self):
        """Test that escaped newlines are still allowed in quoted attribute values."""

        markup = '<div id="1" title="ab"></div><div id="2" title="a b"></div>'

        for newline in ('\r\n', '\n', '\r', '\f'):
            self.assert_selector(
                markup,
                '[title="a\\{}b"]'.format(newline),
                ["1"],
                flags=util.HTML5
            )
            self.assert_selector(
                markup,
                "[title='a\\{}b']".format(newline),
                ["1"],
                flags=util.HTML5
            )
