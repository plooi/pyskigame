import util
#from 
class Track:
    def __init__(self):
        self.points = []
        self.segments = []
    def add_point(self, point, index=None):
        if index == None:
            index = len(self.points)
        self.points.insert(index, point)
        return self
    def generate_segments(self):
        self.segments = []
        for i in range(len(self.points)):
            self.segments.append(Segment  (self.points[i], self.points[circular_add(i, 1, len(self.points))])  )
        return self
    def __iter__(self):
        for seg in self.segments:
            yield seg
    def __getitem__(self, i):
        return self.points[i]
            
class Segment:
    def __init__(self, p1, p2):
        self.p1 = p1
        self.p2 = p2
        self.hr = util.get_angle(p1.z, p1.x, p2.z, p2.x)
        self.speed = p1.speed
        self.time_duration = self._calc_time_duration()
    def _calc_time_duration(self):
        distance = ( (self.p1.x-self.p2.x)**2 + (self.p1.y-self.p2.y)**2 + (self.p1.z-self.p2.z)**2 )**.5
        return distance/self.speed
    def get_time_duration(self):
        return self.time_duration
    def horizontal_angle(self):
        return self.hr
    def travel(self, time):
        fraction = time/self.time_duration
        inverted_fraction = 1-fraction
        return [
                    self.p1.x * inverted_fraction + self.p2.x * fraction,
                    self.p1.y * inverted_fraction + self.p2.y * fraction,
                    self.p1.z * inverted_fraction + self.p2.z * fraction,
                    ]


class Point:
    def __init__(self, x, y, z, v):
        self.x=x
        self.y=y
        self.z=z
        self.speed=v
    def __getitem__(self, i):
        if i == 0: return self.x
        if i == 1: return self.y
        if i == 2: return self.z
        raise Exception("invalid index")
    def __setitem__(self, i, value):
        if i == 0: self.x = value
        elif i == 1: self.y = value
        elif i == 2: self.z = value
        else: raise Exception("invalid index")
    
def circular_add(a, b, max):
    ret = a+b
    while ret >= max:
        ret -= max
    return ret
