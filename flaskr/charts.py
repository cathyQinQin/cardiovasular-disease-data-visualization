from collections import Counter;
import math

class Chart:
    def __init__(self, name, plot_type, labels=None, *, xlabel=None, ylabel='Presence of cardiovascular disease'):
        self.name = name
        self.counter = Counter()
        self.datasets = []
        options = {}
        data = {
            'datasets': self.datasets
        }
        self.config = {
            'type': plot_type,
            'options': options,
            'data': data
        }

        if labels:
            data['labels'] = labels

        if (plot_type in ['scatter','bar','bubble']):
            options['scales'] = {
                'x': {
                    'type': 'linear' if labels is None else 'category',
                    'position': 'bottom',
                    'title': {
                        'text': xlabel if xlabel is not None else name,
                        'display': True,
                    }
                },
                'y': {
                    'type': 'linear',
                    'position': 'left',
                    'title': {
                        'text': ylabel,
                        'display': True,
                    }
                }
            }


    def _points_format(self,label,counter):
        data = []
        for x,y in counter.items():
            data.append({'x': x, 'y': y})
        return {
            'label': label,
            'data': data
        }

class BMIChart(Chart):
    def __init__(self):
        super().__init__('BMI', 'scatter')
    
    def aggregate(self, p):
        cardio =  int(p['cardio'])
        if cardio:
            bmi = float(p['weight']) / (float(p['height'])/100)**2
            self.counter[int(bmi)] += cardio
    
    def plot(self):
        self.datasets.append(self._points_format(self.name, self.counter))

class AgeChart(Chart):
    def __init__(self):
        super().__init__('Age', 'scatter')
    
    def aggregate(self, p):
        cardio =  int(p['cardio'])
        if cardio:
            age = round(float(p['age'])/365)
            self.counter[age] += cardio
    
    def plot(self):
        self.datasets.append(self._points_format(self.name, self.counter))

class GenderChart(Chart):
    def __init__(self):
        super().__init__('Gender', 'bar', ['Male', 'Female', 'Total'], ylabel='# of People')
    
    def aggregate(self, p):
        gender = 'm' if int(p['gender']) == 2 else 'f'
        cardio = 'c1' if int(p['cardio']) else 'c0'        
        self.counter[gender + cardio] += 1
    
    def plot(self):
        self.datasets.append({
            'label': 'Have cardiovascular disease',
            'data': [self.counter['mc1'], self.counter['fc1'], self.counter['mc1'] + self.counter['fc1']]
        })
        self.datasets.append({
            'label': 'No cardiovascular disease',
            'data': [self.counter['mc0'], self.counter['fc0'], self.counter['mc0'] + self.counter['fc0']]
        })

class BloodPressureChart(Chart):
    def __init__(self):
        super().__init__('Blood pressure','bubble', xlabel='Systolic blood pressure', ylabel='Diastolic blood pressure')
    
    def aggregate(self, p):
        cardio =  int(p['cardio'])
        hi = round(float(p['ap_hi'])/5)*5
        lo = round(float(p['ap_lo'])/5)*5
        if cardio and hi > 0 and lo > 0 and hi < 300 and lo < 300:
            self.counter[(hi,lo)] += cardio
    
    def plot(self):
        data = []
        for (x,y),c in self.counter.items():
            r = math.ceil(c / 100.0)
            data.append({'x': x, 'y': y, 'r': r})

        self.datasets.append({
            'label': 'Have cardiovascular disease',
            'data': data
        })


class CholesterolGlucoseChart(Chart):
    def __init__(self):
        super().__init__('Cholesterol & Glucose', 'bar', ['normal', 'above normal', 'well above normal'])
    
    def aggregate(self, p):
        cardio = int(p['cardio'])      
        self.counter['c' + p['cholesterol']] += cardio
        self.counter['g' + p['gluc']] += cardio
    
    def plot(self):
        self.datasets.append({
            'label': 'Cholesterol',
            'data': [self.counter['c1'], self.counter['c2'], self.counter['c3']]
        })
        self.datasets.append({
            'label': 'Glucose',
            'data': [self.counter['g1'], self.counter['g2'], self.counter['g3']]
        })


class SubjectiveFeaturesChart(Chart):
    def __init__(self):
        super().__init__('Subjective Features', 'bar', ['Smoking', 'Alcohol intake', 'Physical activity'], ylabel="# of People")
    
    def aggregate(self, p):
        cardio = '1' if int(p['cardio']) else '0' 
        if int(p['smoke']):
            self.counter['s' + cardio] += 1
        if int(p['alco']):
            self.counter['al' + cardio] += 1
        if int(p['active']):
            self.counter['ac' + cardio] += 1
    
    def plot(self):
        self.datasets.append({
            'label': 'Have cardiovascular disease',
            'data': [self.counter['s1'], self.counter['al1'], self.counter['ac1']]
        })
        self.datasets.append({
            'label': 'No cardiovascular disease',
            'data': [self.counter['s0'], self.counter['al0'], self.counter['ac0']]
        })

class Charts:
    def __init__(self):
        self.charts = {}
        self._add(BMIChart())
        self._add(GenderChart())
        self._add(AgeChart())
        self._add(BloodPressureChart())
        self._add(CholesterolGlucoseChart())
        self._add(SubjectiveFeaturesChart())


    def _add(self,chart):
        self.charts[chart.name] = chart
    
    def aggregate(self, p):
        for chart in self.charts.values():
            chart.aggregate(p)
    
    def plot(self):
        for chart in self.charts.values():
            chart.plot()
    
    def names(self):
        return self.charts.keys()

    def get(self, name):
        chart = self.charts.get(name, None)
        if chart is not None:
            return chart.config