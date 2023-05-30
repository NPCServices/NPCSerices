from pathlib import Path
import markdown
import markmoji

__folder__ = Path(__file__).parent
encoding = "utf-8"

# read template
template = (__folder__ / "template.html").read_text(encoding=encoding)

# setup compiler
md = markdown.Markdown(extensions=["extra", "admonition", "nl2br", "meta", markmoji.Markmoji()])

# start content and nav bar
content = ""
nav = []

# get content files
for file in __folder__.glob("*.md"):
    # skip README file
    if file.stem == "README":
        continue

    # get content for this section
    section = file.read_text(encoding=encoding)

    # add nav item
    nav.append(
        f"<a href=#{file.stem.lower()}>{file.stem}</a>"
    )

    # open section tag with nav anchor and add title
    content += (
        f"<a id={file.stem.lower()}></a>\n"
        f"<section>\n"
        f"<header>{file.stem}</header>\n"
    )
    # write content
    content += md.convert(section)
    # close section tag
    content += (
        f"</section>\n"
        f"\n"
    )

# insert content and navbar
template = template.replace("{{content}}", content)
template = template.replace("{{nav}}", "|\n".join(nav))

# save
with open("index.html", "w") as f:
    f.write(template)