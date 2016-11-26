class ArgsErrorException(Exception):
    status_code=400
    def __init__(self,msg,status_code=400):
        super(ArgsErrorException,self).__init__(msg)
        self.msg=msg
        self.status_code=status_code


