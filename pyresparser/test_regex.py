import re

def test_mobile_regex():
    text = "Call me at (+91) 8087996634 or +919530030470"
    # The new regex we want to test
    mob_num_regex = r'''((\+?\d{1,3}[-.\s]?)?\(?\+?\d{1,3}\)?[-.\s]?\d{3}[-.\s]?\d{3}[-.\s]?\d{4}|\(\d{3}\)[-.\s]*\d{3}[-.\s]?\d{4}|\d{3}[-.\s]?\d{4})'''
    
    phone = re.findall(re.compile(mob_num_regex), text)
    print(f"Found: {phone}")

if __name__ == "__main__":
    test_mobile_regex()
