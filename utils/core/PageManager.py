class PageManager:
    def __init__(self, parent):
        self.parent = parent
        self.currentPage = None
        self.history = []

    def show_page(self, pageClass, *args, **kwargs):
        if self.currentPage:
            self.currentPage.destroy_frame()
        self.currentPage = pageClass(self.parent, *args, **kwargs)
        back = self.currentPage.create_frame()

        # if not the same page as before, add to history
        if len(self.history) <= 0 or self.history[-1].__class__.__name__ != pageClass.__name__:
            self.history.append(self.currentPage)
        
        if back:
            self.back()

    def back(self):
        if len(self.history) > 1:
            self.history.pop()
            self.currentPage = self.history[-1]
            self.currentPage.create_frame()
    
    def clear_history(self):
        self.history = []