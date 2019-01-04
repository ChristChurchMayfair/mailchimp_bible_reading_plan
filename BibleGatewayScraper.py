from lxml import html
from lxml import etree
import httplib2
import urllib
import re


class BibleGatewayScraper:

    def __init__(self, base_url):
        self.base_url = base_url
        self.h = httplib2.Http(".cache")

    def get_passage_by_reference(self, reference, version='NIV'):

        nice_reference = reference.pretty()

        args = {'search': nice_reference, 'version': version}

        encoded_args = urllib.parse.urlencode(args)

        passage_url = self.base_url + '/passage/?' + encoded_args

        (response, content) = self.h.request(passage_url, "GET")

        string_content = content.decode("utf-8")

        cross_refs_removed = re.sub('<sup class=\'crossreference\'\s+data-link=\'\(&lt;a href=&quot;#cen-[A-Z]*-[0-9]*[A-Z]*&quot;\s+title=&quot;See\s+cross-reference\s+[A-Z]*&quot;&gt;[A-Z]*&lt;\/a&gt;\)\' data-cr=\'#cen-[A-Z]*-[0-9]*[A-Z]*\'><\/sup>', '', string_content)

        footnotes_removed = re.sub('<sup data-fn=\'#fen-[A-Z]*-\d*[a-z]*\' class=\'footnote\' data-link=\'\[&lt;a href=&quot;#fen\-[A-Z]*\-\d*[a-z]*&quot; title=&quot;See footnote [a-z]*&quot;&gt;[a-z]*&lt;\/a&gt;\]\'>\[<a href="#fen\-[A-Z]*\-\d*[a-z]*" title="See footnote [a-z]*">[a-z]*<\/a>\]<\/sup>','', cross_refs_removed)

        h1s_styled = re.sub('<h1 ','<h1 style="font-size:1.2em;"', footnotes_removed)

        tree = html.fromstring(h1s_styled)

        passage_div = tree.xpath('//div[contains(@class, \'text-html\')]')[0]

        # Remove things we don't need

        for hidden_cross_ref in passage_div.xpath("//div[contains(@class, \'crossrefs\')]"):
            hidden_cross_ref.getparent().remove(hidden_cross_ref)

        for footnotes in passage_div.xpath("//div[contains(@class, \'footnotes\')]"):
            footnotes.getparent().remove(footnotes)

        # for chapternum in passage_div.xpath("//span[contains(@class, \'chapternum\')]"):
        #     chapternum.getparent().remove(chapternum)

        # for passage_version in passage_div.xpath("//span[contains(@class, \'passage-display-version\')]"):
        #     passage_version.getparent().remove(passage_version)
        #
        # for heading in passage_div.xpath("//span[contains(@class, \'passage-display-bcv\')]"):
        #     heading.getparent().remove(heading)

        for h3 in passage_div.xpath("//h3"):
            h3.getparent().remove(h3)

        return etree.tostring(passage_div).decode('utf-8').strip().replace(u'\xa0', u' ')
