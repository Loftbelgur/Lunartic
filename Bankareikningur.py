class bankareikningur:
    def __init__(self):
        self.reikningur = 0
        # Smiður: Nullstillir stodu reiknings

    def legg_inn(self , upphaed):
        # Leggur upphaed ut af reikningi+
        self.reikningur += upphaed

    def taka_ut(self, upphaed):
        if upphaed > 0:
            return True
        else:
            return False
    def saekja_stodu(self):
        if self.reikningur < 0:
            raise ValueError('Negative balance on account')
        return self.reikningur

    """def main():
        a = bankareikningur()
        print(a.reikningur)

    if __name__ == "__main__":
        main()"""
