import re
import base64



with open('matmod.html','r',encoding="utf-8") as f:
    html_er=f.read()

pattern = re.compile('url\(&quot;data:image/jpeg;base64.*?\)')
pattern2 = re.compile('url\(&quot;data:image/jpeg;base64,|&quot;\)')
result = re.findall(pattern, html_er)


page=1
for pageImg in result:
    clearBase64String = pageImg.replace('url(&quot;data:image/jpeg;base64,', "").replace('&quot;)', "")

    with open(f"out/book1/matmodDisser_{page}.jpeg", "wb") as fh:
      fh.write(base64.urlsafe_b64decode(clearBase64String))
    print(f"page {page} saved")
    page=page+1