import re


class GCode2Ngc():
    def __init__(self):
        self.replacements = [
            [r'(G(?:0|1|2|3|28|92).*)(?:E)([-\+]?[\d\.].*)', r'\1A\2'],
            [r'G10', r'G22'],
            [r'G11', r'G23'],
            [r'(M(?:104|106|109|140|141|190|191).*)(?:S)([\d\.].*)', r'\1P\2'],
            [r'.*M82.*', '']
        ]

        self.endCode = 'M2 ; end of program'
        self.endTerm = r'(?:\s*M2.*|\s%.*)'

        self.regMatch = []
        self.endRegex = None

        self.hasProgramEnd = False

    def compile_regex(self):
        for self.regexString, self.replacement in self.replacements:
            regex = re.compile(self.regexString, flags=re.IGNORECASE)
            self.regMatch.append([regex, self.replacement])
        self.endRegex = re.compile(self.endTerm, flags=re.IGNORECASE)

    def do_regex_replacements(self, line):
        for regex, replacement in self.regMatch:
            line = regex.sub(replacement, line)
        return line

    def prepare_processing(self):
        self.hasProgramEnd = False
        self.compile_regex()

    def process_layer(self, layer):
        newline = self.do_regex_replacements(layer)
        if (not self.hasProgramEnd) and self.endRegex.match(newline):  # check for end of program
            self.hasProgramEnd = True
        return newline

    def finalize_processing(self, data):
        if not self.hasProgramEnd:
            data.append(self.endCode + '\n')

    def process(self, data):
        self.prepare_processing()

        for index, layer in enumerate(data):
            data[index] = self.process_layer(layer)

        self.finalize_processing(data)
