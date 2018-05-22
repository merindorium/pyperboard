import re

from markdown.extensions import Extension
from markdown.inlinepatterns import Pattern
from markdown.preprocessors import Preprocessor
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
    METHODS = ['get', 'post', 'put', 'patch', 'delete', 'options', 'head']

    PARENT_ELEMENT_CLASS = 'api-endpoint'

    def handleMatch(self, m):
        endpoint_method = m.group('method').lower()
        endpoint_url = m.group('url')

        if endpoint_method not in self.METHODS:
            return None

        return self._get_endpoint_elem(endpoint_method, endpoint_url)

    def _get_endpoint_elem(self, endpoint_method: str, endpoint_url: str) -> etree.Element:
        elem = etree.Element('div')
        elem.set('class', self.PARENT_ELEMENT_CLASS)

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


class WebsocketEventPattern(ApiEndpointPattern):
    METHODS = ['on', 'emit']
    PARENT_ELEMENT_CLASS = 'websocket'


class SegmentPreprocessor(Preprocessor):
    SEGMENT_RE = re.compile(r'@@@(?P<segment_group>[\S]+?)\|(?P<segment_name>[\S]+?)\n(?P<data>[\s\S]+?)?\n@@@',
                            re.MULTILINE | re.DOTALL | re.VERBOSE)
    SEGMENT_CLASS = 'segment'
    SEGMENT_WRAP = '<div id="{segment_group}__{segment_name}" ' \
                   'class="{segment_class}" data-segment={segment_name} markdown>{data}' \
                   '</div>'

    def run(self, lines):
        text = '\n'.join(lines)

        while True:

            matched = self.SEGMENT_RE.search(text)

            if matched:

                segment_name = matched.group('segment_name')
                segment_group = matched.group('segment_group')
                segment_data = matched.group('data')

                segment = self.SEGMENT_WRAP.format(segment_class=self.SEGMENT_CLASS,
                                                   segment_group=segment_group,
                                                   segment_name=segment_name,
                                                   data=segment_data)

                text = '{}\n{}\n{}'.format(
                    text[:matched.start()],
                    segment,
                    text[matched.end():]
                )

            else:
                break

        return text.split('\n')


class SegmentMenuPattern(Pattern):
    SEGMENT_MENU_CLASS = 'segment-menu'
    SEGMENT_MENU_ITEM_CLASS = 'segment-menu-item'
    SEGMENT_DATASET_NAME = 'group'

    def handleMatch(self, m):
        segment_group = m.group('segment_group')
        segment_menu = self._get_segment_menu(segment_group)

        return segment_menu

    def _get_segment_menu(self, segment_group: str) -> etree.Element:
        segment_menu = etree.Element('nav')
        segment_menu.set('class', self.SEGMENT_MENU_CLASS)
        segment_menu.set('data-{}'.format(self.SEGMENT_DATASET_NAME), segment_group)

        return segment_menu


class RestApiExtension(Extension):
    REQUEST_ATTRIBUTE_RE = r'\[(?P<attribute>\w+):(?P<type>\W+)\]'
    API_ENDPOINT_RE = r'\[(?P<method>\w+)\|(?P<url>\S+)\]'
    SOCKET_EVENT_RE = r'\[(?P<method>\w+)\|(?P<url>[a-zA-Z0-9_ ]+)\]'

    def extendMarkdown(self, md, md_globals):
        md.inlinePatterns.add('attribute_field', RequestAttributePattern(self.REQUEST_ATTRIBUTE_RE, md), '_end')
        md.inlinePatterns.add('api_endpoint', ApiEndpointPattern(self.API_ENDPOINT_RE, md), '_end')
        md.inlinePatterns.add('socket_events', WebsocketEventPattern(self.SOCKET_EVENT_RE, md), '_end')


class SegmentExtension(Extension):
    SEGMENT_MENU_RE = r'\[segment-menu\|(?P<segment_group>[\S]+)\]'

    def extendMarkdown(self, md, md_globals):
        md.preprocessors.add('segment', SegmentPreprocessor(md), '_begin')
        md.inlinePatterns.add('segment_menu', SegmentMenuPattern(self.SEGMENT_MENU_RE, md), '_end')
