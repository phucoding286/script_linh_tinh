# Welcome everyone to come my Github page!
- Today i will share a meschat module for you can create your own bots. Let's view part of setup this

## On PC
1. require libaries as follows
```
pip install selenium webdriver-manager emoji
```
2. go to python shell and using these commands
```
>> from webdriver_manager.chrome import ChromeDriverManager
```
```
# let's attention this! if on your PC haven't Chrome but have other browsers like Edge
# you can using different commands like
```
```
>> from webdriver_manager.microsoft import EdgeChroniumDriverManager
# and then you can using as follows
>> print(EdgeChroniumDriverManager().install())
# so if it's appeer a path, mean is complete!
```
- view details in: https://pypi.org/project/webdriver-manager/

## On Android termux
1. allow acess memories
```
termux-setup-storage
```
2. update package
```
yes | pkg update -y && yes | pkg upgrade -y
```
3. install python pip
```
yes | pkg install python-pip -y
```
4. require libaries as follows
```
pip install selenium webdriver-manager emoji
```
5. install selenium
```
pip install selenium==4.9.1
```
6. install chronium
```
yes | pkg install x11-repo -y
yes | pkg install tur-repo -y
yes | pkg install chromium -y
```
7. install driver via webdriver manager in python shell
```
>> from webdriver_mânger.chrome import ChromeDriverManager
>> print(ChromeDriverManager().install())
```


## Example Code
```
from meschat import MesChat

email = "meschat@example.com"
passw = "example123"
link_chat_group = "https://messenger.com/example/

meschat = MesChat(email_or_phone=email, password=passw, group_or_chat=link_chat_group)

while True:
    if meschat.current_inp != meschat.his_inp:
        if meschat.current_inp == "hi":
            meschat.send_message(inp="hello again :)")
```

## thank you for visit my project. Let's support me via social media if you can. Thank you

- my facebook: https://www.facebook.com/profile.php?id=61562099241369
- my youtube: https://www.youtube.com/@phucoding286
