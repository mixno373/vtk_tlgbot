class CRMClient:
    
    def __init__(self, **kwargs):
        self.uid = int(kwargs.get('uid', 0))
        self.surname = str(kwargs.get('surname', ''))
        self.name = str(kwargs.get('name', ''))
        self.midname = str(kwargs.get('midname', ''))
        self.phone = str(kwargs.get('phone', ''))
        self.secondphone = str(kwargs.get('secondphone', ''))
        self.description = str(kwargs.get('description', ''))
        self.know_from = str(kwargs.get('from', ''))

    def __str__(self):
        return "<CRMClient: ({self.uid}) '{self.surname} {self.name} {self.midname}', тел.: {self.phone} ({self.secondphone}), узнал из {self.know_from}>"

    def __repr__(self):
        return "<CRMClient: ({self.uid}) '{self.surname} {self.name} {self.midname}', тел.: {self.phone} ({self.secondphone}), узнал из {self.know_from}>"
