import re
import math


class Ngc2Ve():
    def __init__(self):
        self.enable_cross_optimization = False
        self.cross_tolerance = 0.01

    def init_variables(self):
        self.regMatch = {}
        self.line_count = 0
        self.output_line_count = 0
        self.prev_p = [999999, 999999, 999999, 999999, 999999]  # high number so we detect the change on first move
        self.prev_cross = 99999999
        self.prev_cross_line = None
        self.currentInFile = None
        self.currentOutFile = None
        self.crossList = []
        self.crossLength = 0.0
        self.totalCross = []
        self.filament_d = 1.75
        self.retracted = True
        self.lastx = 0
        self.lasty = 0
        self.lastz = 0
        self.lasta = 0
        self.lastf = 0
        self.filament_area = (self.filament_d ** 2) * math.pi / 4
        self.outputData = []

    def _get_code_int(self, line, code):
        if code not in self.regMatch:
            self.regMatch[code] = re.compile(code + r'([^\s]+)', flags=re.IGNORECASE)
        m = self.regMatch[code].search(line)
        if m is None:
            return None
        try:
            return int(m.group(1))
        except ValueError:
            return None

    def _get_code_float(self, line, code):
        if code not in self.regMatch:
            self.regMatch[code] = re.compile(code + r'([^\s]+)', flags=re.IGNORECASE)
        m = self.regMatch[code].search(line)
        if m is None:
            return None
        try:
            return float(m.group(1))
        except ValueError:
            return None

    def _simplify_line(self, g, p, c):
        #print "i, g,p,c=", i, g,p,c
        s = "G" + str(g) + " "
        if (p[0] is not None) and (p[0] != self.prev_p[0]):
            self.prev_p[0] = p[0]
            s = s + "X{0:g}".format(p[0]) + " "
        if (p[1] is not None) and (p[1] != self.prev_p[1]):
            self.prev_p[1] = p[1]
            s = s + "Y{0:g}".format(p[1]) + " "
        if (p[2] is not None) and (p[2] != self.prev_p[2]):
            self.prev_p[2] = p[2]
            s = s + "Z{0:g}".format(p[2]) + " "
        if (p[3] is not None) and (p[3] != self.prev_p[3]):
            self.prev_p[3] = p[3]
            s = s + "F{0:g}".format(p[3]) + " "
        if p[4] is not None:
            s = s + "I{0:g}".format(p[4]) + " "
        if p[5] is not None:
            s = s + "J{0:g}".format(p[5]) + " "
        if c is not None:
            s = s + "; " + c
        s = s.rstrip()
        self._output_line(s)

    def _compare_value(self, newValue, oldValue, tolerance):
        return (newValue < (oldValue * (1.0 - tolerance))) \
            or (newValue > (oldValue * (1.0 + tolerance)))

    def _init_cross(self):
        self.crossList = []
        self.crossLength = 0.0
        self.prev_cross = 999999999

    def _optimize_cross(self):
        if len(self.crossList) > 0 and self.crossLength > 0.0:
            crossMed = sum(self.crossList) / self.crossLength
            self._output_cross(crossMed, self.prev_cross_line)
            self._init_cross()

    def _simplify_cross(self, cross, length):
        if self._compare_value(cross, self.prev_cross, self.cross_tolerance):
            if self.enable_cross_optimization:
                self._optimize_cross()
            self.crossList = [cross * length]
            self.crossLength = length
            self.prev_cross = cross
            self.prev_cross_line = self.output_line_count
            self._output_cross(cross)
        else:
            self.crossList.append(cross * length)
            self.crossLength += length

    def _output_cross(self, cross, line_number=None):
        s = "M700 P{0:g}".format(cross) + " "
        if not line_number:
            self._output_line(s)
        else:
            self._update_line(s, line_number)

    def _output_line(self, line):
        self.outputData.append(line + '\n')
        self.output_line_count = self.output_line_count + 1

    def _update_line(self, line, number):
        if number < len(self.outputData):
            self.outputData[number] = line + '\n'

    def _prepare_processing(self):
        self.init_variables()

    def _process_line(self, line):
        self.line_count = self.line_count + 1
        line = line.rstrip()
        original_line = line
        if type(line) is tuple:
            line = line[0]

        if ';' in line or '(' in line:
            sem_pos = line.find(';')
            par_pos = line.find('(')
            pos = sem_pos
            if pos is None:
                pos = par_pos
            elif par_pos is not None:
                if par_pos > sem_pos:
                    pos = par_pos
            comment = line[pos + 1:].strip()
            line = line[0:pos]
        else:
            comment = None

        # we only try to simplify G1 coordinated moves
        G = self._get_code_int(line, 'G')
        if G == 1:    # Move
            x = self._get_code_float(line, 'X')
            y = self._get_code_float(line, 'Y')
            z = self._get_code_float(line, 'Z')
            a = self._get_code_float(line, 'A')
            f = self._get_code_float(line, 'F')

            retract = False
            unretract = False
            move = False

            if (a is None):
                move = True
            elif (x is None) and (y is None) and (z is None):
                if (a - self.lasta) > 0:
                    unretract = True
                else:
                    retract = True

            if x is None:
                x = self.lastx
            if y is None:
                y = self.lasty
            if z is None:
                z = self.lastz
            if a is None:
                a = self.lasta
            if f is None:
                f = self.lastf

            diffx = x - self.lastx
            diffy = y - self.lasty
            diffz = z - self.lastz
            diffa = a - self.lasta

            dead = False
            if (diffx == 0.0) and (diffy == 0.0) and (diffz == 0.0) \
               and (diffa == 0.0):
                dead = True

            if retract:
                self._output_line("G22 ; retract")
                self.retracted = True
            elif unretract:
                self._output_line("G23 ; unretract")
                self.retracted = False
            elif move:
                if not self.retracted:  # handle moves without retraction
                    self._simplify_cross(0.0, 0.0)
                self._simplify_line(G, [x, y, z, f, None, None], comment)
            elif dead:
                pass  # pass dead moves
            else:
                length = math.hypot(diffx, diffy)
                if diffz != 0.0:
                    length = math.hypot(length, diffz)
                volume = diffa * self.filament_area
                cross_section = volume / length
                self._simplify_cross(cross_section, length)
                self._simplify_line(G, [x, y, z, f, None, None], comment)

            self.lastx = x
            self.lasty = y
            self.lastz = z
            self.lasta = a
            self.lastf = f

        elif (G == 2) or (G == 3):
            x = self._get_code_float(line, 'X')
            y = self._get_code_float(line, 'Y')
            z = self._get_code_float(line, 'Z')
            a = self._get_code_float(line, 'A')
            f = self._get_code_float(line, 'F')
            i = self._get_code_float(line, 'I')
            j = self._get_code_float(line, 'J')

            if x is None:
                x = self.lastx
            if y is None:
                y = self.lasty
            if z is None:
                z = self.lastz
            if a is None:
                a = self.lasta
            if f is None:
                f = self.lastf

            diffa = a - self.lasta
            centerx = self.lastx + i
            centery = self.lasty + j

            print("x: " + str(x))
            print("y: " + str(y))
            print("a: " + str(a))
            print("centerx: " + str(centerx))
            print("centery: " + str(centery))
            print("lastx: " + str(self.lastx))
            print("lasty: " + str(self.lasty))
            print("i: " + str(i))
            print("j: " + str(j))
            r = (i ** 2 + j ** 2) ** 0.5
            w = ((x - self.lastx) ** 2 + (y - self.lasty) ** 2) ** 0.5
            angle = 2 * math.asin(w / (2 * r))
            innerp = centerx * x + centery * y
            len1 = (centerx ** 2 + centery ** 2) ** 0.5
            len2 = (x ** 2 + y ** 2) ** 0.5
            a1 = math.acos(innerp / (len1 * len2))
            innerp = centerx * self.lastx + centery * self.lasty
            len2 = (self.lastx ** 2 + self.lasty ** 2) ** 0.5
            a2 = math.acos(innerp / (len1 * len2))
            if G == 2:
                if a2 < a1:
                    a2 += math.pi * 2
                    angle2 = a2 - a1
            else:
                if a1 < a2:
                    a1 += math.pi * 2
                angle2 = a1 - a2
            print("a1: %f" % a1)
            print("a2: %f" % a2)
            length = angle2 * r
            print("length %f" % length)
            volume = diffa * self.filament_area
            print("volume %f" % volume)
            cross_section = volume / length
            print("cross_section %f" % cross_section)
            #height = cross_section / nozzle_d
            #print "height",height
            self._simplify_cross(cross_section, length)
            self._simplify_line(G, [x, y, z, f, i, j], comment)

            self.lastx = x
            self.lasty = y
            self.lastz = z
            self.lasta = a
            self.lastf = f

        else:
            # any other move signifies the end of a list of line segments,
            # so we simplify them.

            # store retraction to detect unretracted moves without extrusion (infill)
            if (G == 22):
                self.retracted = True
            elif (G == 23):
                self.retracted = False

            if (G == 0) or (G == 92):    # Rapid - remember position
                x = self._get_code_float(line, 'X')
                y = self._get_code_float(line, 'Y')
                z = self._get_code_float(line, 'Z')
                a = self._get_code_float(line, 'A')

                if x is None:
                    x = self.lastx
                if y is None:
                    y = self.lasty
                if z is None:
                    z = self.lastz
                if a is None:
                    a = self.lasta

                self.lastx = x
                self.lasty = y
                self.lastz = z
                self.lasta = a

                if G != 92:
                    self._simplify_line(G, [x, y, z, None, None, None], comment)
            else:
                self._output_line(original_line)

    def _finalize_processing(self, data):
        self._output_line("; GCode file processed by ngc2ve")
        self._output_line("; Input Line Count = " + str(self.line_count))
        self._output_line("; Output Line Count = " + str(self.output_line_count))

        data.append(''.join(self.outputData))

    def process(self, data):
        self._prepare_processing()

        for index, layer in enumerate(data):
            if self.enable_cross_optimization:
                self._init_cross()
            for line in layer.split('\n'):
                if line is '':
                    continue
                self._process_line(line)
            if self.enable_cross_optimization:
                self._optimize_cross()
            data[index] = ''.join(self.outputData)
            self.outputData = []

        self._finalize_processing(data)
