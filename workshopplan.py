import sublime
import sublime_plugin
from .general.wplan import WPlan


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
        self.cursor_start = self.view.sel()[0].begin()
        self.all_region = sublime.Region(0, self.view.size())
        self.all_content = self.view.substr(self.all_region)

    def generateMenu(self):
        return [
            'Time',
            'Material'
        ]

    def select(self, i):
        menu = self.generateMenu()
        wp = WPlan(self.all_content)

        if i == -1:
            return False

        elif menu[i] == 'Time':
            index = wp.getActualIndex(self.cursor_start)
            title = wp.Blocks[index].Title
            time = wp.getActualTimeStr(index)
            duration = wp.Blocks[index].getDurationStr()
            all_time = wp.getTimeSum()
            msg = (
                'Title:\t\t\t{}'
                '\nTime:\t\t\t{}'
                '\nDuration:\t\t{}'
                '\n\nOverall time:\t{}'
            ).format(
                title, time, duration, all_time
            )
            sublime.message_dialog(msg)

        elif menu[i] == 'Material':
            materials = wp.getMaterials()
            material_uses = []
            material_blocks = ''
            for x in materials:
                material_uses.append(
                    '{} ({})'.format(x, len(materials[x]))
                )
                material_blocks += '{}: {}\n\n'.format(
                    x, ', '.join(materials[x])
                )
            msg = 'Materials:\n\nUsages:\n{}\n\nIn blocks:\n{}'.format(
                ', '.join(material_uses),
                material_blocks
            )
            sublime.message_dialog(msg)
