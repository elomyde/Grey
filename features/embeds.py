import discord
GREY_IMAGE_URL = "https://cdn.discordapp.com/avatars/790571552345030686/b00a86de8949e75b3e245451eb2029b7.png"

help_regular = discord.Embed(title = "🛠️ Commands", colour=discord.Colour(0xe6e6e6))
help_regular.set_author(name="Grey", icon_url= GREY_IMAGE_URL)
help_regular.add_field(name="Prefix", value="Grey uses '=' as a prefix. `ex) =help`", inline = False)
help_regular.add_field(name="Invitation", value="`invite`\nMake a invitation for your server.", inline = False)
help_regular.add_field(name="Vote", value="`vote item`\n`vote a or b or ...`\naliases : `v`\nCreate a vote!\nYou can create a single Yes-or-no vote\nor a vote with up to eight items.", inline = False)

help_fun = discord.Embed(title = "🎮 Fun commands", colour=discord.Colour(0xe6e6e6))
help_fun.set_author(name="Grey", icon_url=GREY_IMAGE_URL)
help_fun.add_field(name="UwU", value="`UwU`, `uwu`\nUwU", inline = False)
help_fun.add_field(name="minesweeper", value="`mines x y z`\naliases : `mine`, `m`\nMake minesweeper, size of x * y with z mines.", inline = False)
help_fun.add_field(name="Grey patpat", value="`greypatpat`\naliases : `gpp`, `gp`\nGrey will patpat you!", inline = False)
help_fun.add_field(name="Change the avatar of Grey", value="`changeavatar`\naliases : `ca`\nChange an avatar of Grey, can only be used once per five minutes.", inline = False)
help_fun.add_field(name="Convert emoji to text", value="`emojitext emoji text`\naliases : `etext`, `et`\nConvert your text to emoji! text length must be shorter than 9 characters.", inline = False)
help_fun.add_field(name="Age converters", value="`saturnage age`\naliases:`sa`\nConvert your Earth-age into gorgeous Saturn-age\n`earthage age`\naliases : `ea`\nConvert your Saturn-age into Earth-age", inline = False)
help_fun.add_field(name="Q&A", value="`Q_A`\naliases : `QA`, `qa`, `QnA`, `qna`\nGet a random ZUTOMAYO Q&A from various sources.", inline = False)