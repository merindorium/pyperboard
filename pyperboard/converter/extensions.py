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


class ApiEndpointPattern(Pattern):
    ENDPOINT_METHODS = ['get', 'post', 'put', 'patch', 'delete', 'options', 'head']

    def handleMatch(self, m):
        endpoint_method = m.group('method').lower()
        endpoint_url = m.group('url')

        if endpoint_method not in self.ENDPOINT_METHODS:
            return None

        return self._get_endpoint_elem(endpoint_method, endpoint_url)

    def _get_endpoint_elem(self, endpoint_method: str, endpoint_url: str) -> etree.Element:
        elem = etree.Element('div')
        elem.set('class', 'api-endpoint')

        endpoint_method_elem = self._get_endpoint_method_elem(endpoint_method)
        endpoint_url_elem = self._get_endpoint_url_elem(endpoint_url)

        elem.append(endpoint_method_elem)
        elem.append(endpoint_url_elem)

        return elem

    @staticmethod
    def _get_endpoint_method_elem(endpoint_method: str) -> etree.Element:
        elem = etree.Element('div')
        elem.set('class', f'method method-{endpoint_method}')
        elem.text = endpoint_method

        return elem

    @staticmethod
    def _get_endpoint_url_elem(endpoint_url: str) -> etree.Element:
        elem = etree.Element('div')
        elem.set('class', 'url')
        elem.text = endpoint_url

        return elem


class RestApiExtension(Extension):
    REQUEST_ATTRIBUTE_RE = r'\[(?P<attribute>\w+):(?P<type>\W+)\]'
    API_ENDPOINT_RE = r'\[(?P<method>\w+)\|(?P<url>\S+)\]'

    def extendMarkdown(self, md, md_globals):
        md.inlinePatterns.add('attribute_field', RequestAttributePattern(self.REQUEST_ATTRIBUTE_RE, md), '_end')
        md.inlinePatterns.add('api_endpoint', ApiEndpointPattern(self.API_ENDPOINT_RE, md), '_end')
