import os
import google.generativeai as genai


safety_settings = [
	{"category": "HARM_CATEGORY_HARASSMENT", "threshold": "BLOCK_NONE"},
	{"category": "HARM_CATEGORY_HATE_SPEECH", "threshold": "BLOCK_NONE"},
	{"category": "HARM_CATEGORY_SEXUALLY_EXPLICIT", "threshold": "BLOCK_NONE"},
	{"category": "HARM_CATEGORY_DANGEROUS_CONTENT", "threshold": "BLOCK_NONE"}
]

GOOGLE_API_KEY = str(input("ENTER GOOGLE_API_KEY: "))
genai.configure(api_key=GOOGLE_API_KEY)
# model = genai.GenerativeModel('gemini-pro')
model = genai.GenerativeModel(model_name="gemini-1.5-flash", safety_settings=safety_settings)
query = str(input("Submit a query to Gemini: ")) # FDA drug approval 2024
response = model.generate_content(query)


# remove vietnamese
s1 = u'ÀÁÂÃÈÉÊÌÍÒÓÔÕÙÚÝàáâãèéêìíòóôõùúýĂăĐđĨĩŨũƠơƯưẠạẢảẤấẦầẨẩẪẫẬậẮắẰằẲẳẴẵẶặẸẹẺẻẼẽẾếỀềỂểỄễỆệỈỉỊịỌọỎỏỐốỒồỔổỖỗỘộỚớỜờỞởỠỡỢợỤụỦủỨứỪừỬửỮữỰựỲỳỴỵỶỷỸỹ'
s0 = u'AAAAEEEIIOOOOUUYaaaaeeeiioooouuyAaDdIiUuOoUuAaAaAaAaAaAaAaAaAaAaAaAaEeEeEeEeEeEeEeEeIiIiOoOoOoOoOoOoOoOoOoOoOoOoUuUuUuUuUuUuUuYyYyYyYy'
def remove_accents(input_str):
	s = ''
	# print(input_str.encode('utf-8'))
	for c in input_str:
		if c in s1:
			s += s0[s1.index(c)]
		else:
			s += c
	return s


# file  name and path
query_edit= remove_accents(query)
query_edit = query_edit.replace(' ', '_').replace('?', '')
query_txt = query_edit + '.txt'
query_txt_path = os.path.join('../gemini_export', query_txt)
query_md = query_edit + '.md'
query_md_path = os.path.join('../gemini_export', query_md)
query_html = query_edit + '.html'
query_html_path = os.path.join('../gemini_export', query_html)


# save to file markdown
f = open(query_md_path, "a+", encoding="utf-8")
f.write('# ' + query.capitalize() + '\n')
for line in  response.text:
    f.write(line)    # Write inside file 
f.close()


# os.startfile(query_txt_path)
# os.startfile(query_md_path)

import markdown

markdown.markdownFromFile(input=query_md_path, output=query_html_path)

os.startfile(query_html_path)