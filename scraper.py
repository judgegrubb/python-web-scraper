from lxml import html
import requests

page = requests.get('http://www.acs.utah.edu/uofu/stu/scheduling?term=1158&dept=CS&classtype=g')
tree = html.fromstring(page.text)

classes = tree.xpath('//tr[@valign="top"]')

classNumbers = []
catalogNumbers = []
sections = []
components = []
units = []
titles = []
daysTaught = []
times = []
locations = []
instructors = []


for c in classes:
	cdata = c.xpath('td')
	if len(cdata) == 16:
		classNumbers.append(cdata[1].xpath('font/text()')[0])
		catalogNumbers.append(cdata[3].xpath('font/a/text()')[0])
		sections.append(cdata[4].xpath('font/text()')[0])
		components.append(cdata[5].xpath('font/text()')[0])
		units.append(cdata[6].xpath('font/text()')[0])

		titletext = cdata[7].xpath('font/text()')
		if titletext == [u'\xa0']:
			titles.append(cdata[7].xpath('font/a/text()')[0][18:])
		else:
			titles.append(titletext[0][18:])

		daysTaught.append(cdata[8].xpath('font/text()')[0])
		times.append(cdata[9].xpath('font/text()')[0])

		locationtext = cdata[10].xpath('font/text()')
		if locationtext == [u'\xa0']:
			locations.append(cdata[10].xpath('font/a/text()')[0])
		else:
			locations.append(locationtext[0])

		instructortext = cdata[12].xpath('font/text()')
		if instructortext == [u'\xa0']:
			instructors.append(cdata[12].xpath('font/a/text()')[0])
		else:
			instructors.append(instructortext[0])


print classNumbers
print catalogNumbers
print sections
print components
print units
print titles
print daysTaught
print times
print locations
print instructors