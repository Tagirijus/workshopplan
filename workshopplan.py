import sublime
import sublime_plugin
from .general.wplan import WPlan
from .general import wplan


class WorkshopplanCommand(sublime_plugin.TextCommand):
    def run(self, edit):
        self.initMenu()
        self.initContent()

    def initMenu(self):
        self.data = self.generateMenu()
        sublime.active_window().show_quick_panel(
            self.data, on_select=self.select
        )

    def initContent(self):
        self.all_region = sublime.Region(0, self.view.size())
        self.all_content = self.view.substr(self.all_region)

    def generateMenu(self):
        return [
            'Test',
            'Total time',
            'Summerize'
        ]

    def select(self, i):
        if i == 0:
            wp = WPlan(self.all_content)
            print(wp.Elements)
            # sublime.message_dialog(msg)

        elif i == 1:
            wp = WPlan(self.all_content)
            sublime.message_dialog(wp.getTimeSum())
