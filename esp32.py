import os
import json
import httpx
from loguru import logger

def main():
    try:
        url = "https://espressif.github.io/arduino-esp32/package_esp32_index.json"
        logger.info("GET[%s]: "%(url))
        with httpx.Client() as client:
            response = client.get(url)
            response.raise_for_status()
            reply = response.json()
            logger.info("Recv: %s"%({"packages": [{"name": reply["packages"][0]["name"], "maintainer": reply["packages"][0]["maintainer"], "websiteURL": reply["packages"][0]["websiteURL"], "email": reply["packages"][0]["email"], "help": reply["packages"][0]["help"], "platforms": len(reply["packages"][0]["platforms"]), "tools": len(reply["packages"][0]["tools"])}]}))
            for platform in reply["packages"][0]["platforms"]:
                if platform["url"].startswith("https://github.com/"):
                    platform["url"] = "https://ghfast.top/" + platform["url"]
            for tool in reply["packages"][0]["tools"]:
                for system in tool["systems"]:
                    if system["url"].startswith("https://github.com/"):
                        system["url"] = "https://ghfast.top/" + system["url"]
            
            pwd = os.getcwd()
            dir = os.path.join(pwd, "json")
            if not os.path.exists(dir):
                os.mkdir(dir)
            fileName = os.path.join(pwd, "package_esp32_index.json")
            if os.path.exists(fileName):
                os.remove(fileName)
            with open(fileName, "w") as f:
                f.write(json.dumps(reply, indent=4))
    except Exception as e:
        logger.error(e)

if __name__ == "__main__":
    main()