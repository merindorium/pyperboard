from markdown.extensions import Extension
from markdown.inlinepatterns import Pattern
from markdown.util import etree


class RequestAttributePattern(Pattern):
    ATTRIBUTE_TYPES = {
        '?': 'optional',
        '!': 'required'
    }

    def handleMatch(self, m):
        attribute_name = m.group('attribute')
        attribute_type_mark = m.group('type')

        try:
            attribute_type = self.ATTRIBUTE_TYPES[attribute_type_mark]
        except KeyError:
            return None
        else:
            return self._get_attribute_elem(attribute_name, attribute_type)

    def _get_attribute_elem(self, attribute_name: str, attribute_type: str) -> etree.Element:
        elem = etree.Element('div')
        elem.set('class', 'attribute')

        attribute_name_elem = self._get_attribute_name_elem(attribute_name)
        attribute_type_elem = self._get_attribute_type_elem(attribute_type)
        delimiter_elem = etree.Element('br')

        elem.append(attribute_name_elem)
        elem.append(delimiter_elem)
        elem.append(attribute_type_elem)

        return elem

    @staticmethod
    def _get_attribute_name_elem(attribute_name: str) -> etree.Element:
        elem = etree.Element('code')
        elem.text = attribute_name

        return elem

    @staticmethod
    def _get_attribute_type_elem(attribute_type: str) -> etree.Element:
        elem = etree.Element('span')
        elem.set('class', attribute_type)
        elem.text = attribute_type

        return elem


class RequestAttributeExtension(Extension):
    REQUEST_ATTRIBUTE_RE = r'\[(?P<attribute>\w+):(?P<type>\W+)\]'

    def extendMarkdown(self, md, md_globals):
        md.inlinePatterns.add('attribute_field', RequestAttributePattern(self.REQUEST_ATTRIBUTE_RE, md), '_end')
