def single_word(line, pattern):
    if pattern in line: return True
    else: return False


def multi_word(line, pattern):
    words = pattern.split('.*')
    for word in words:
        line = line.split(word)
        if len(line) == 1: return False
        line = line[1]
    return True


class Grep:

    treated_pattern = []
    treated_text = []

    def __init__(self, pattern, text, sensitive = False):
        self.pattern = pattern
        self.text = text
        self.sensitive = sensitive
        self.check_pattern()
        self.check_text()

    def add_pattern(self,p):
        if '\\|' in p:
            self.treated_pattern += p.split('\\|')
        else: self.treated_pattern.append(p)

    def check_pattern(self):
        if type(self.pattern) == list:
            for p in self.pattern:
                self.add_pattern(p)
        else:
            self.add_pattern(self.pattern)

    def check_text(self):
        if type(self.text) == list:
            for item in self.text:
                self.treated_text += item.split('\n')
        else:
            self.treated_text += self.text.split('\n')

    def scan_pattern(self):
        results = []
        if self.sensitive:
            for line in self.treated_text:
                for pattern in self.treated_pattern:
                    if '.*' in pattern:
                        if multi_word(line, pattern):
                            results.append(line)
                    else:
                        if single_word(line, pattern):
                            results.append(line)
        else:
            for line in self.treated_text:
                sline = line.lower()
                for pattern in self.treated_pattern:
                    pattern = pattern.lower()
                    if '.*' in pattern:
                        if multi_word(sline, pattern):
                            results.append(line)
                    else:
                        if single_word(sline, pattern):
                            results.append(line)
        return results


def grep(pattern, text, sensitive = False):
    consult = Grep(pattern=pattern, text = text, sensitive= sensitive)
    return consult.scan_pattern()
