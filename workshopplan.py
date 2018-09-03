import sublime
import sublime_plugin
from .general.wplan import WPlan
from .general.wplan import TYPES
from .general.settings import Settings


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
            'Material',
            'Add type',
            'Add material',
            'Test'
        ]

    def select(self, i):
        menu = self.generateMenu()
        wp = WPlan(self.all_content)

        if i == -1:
            return False

        elif menu[i] == 'Time':
            all_time = wp.getTimeSum()
            index = wp.getActualIndex(self.cursor_start)
            if index != -1:
                title = wp.Blocks[index]['Title']
                time = wp.getActualTimeStr(index)
                duration = wp.getDurationStr(index)
                msg = (
                    'Block information'
                    '\n\nTitle:\t\t\t{}'
                    '\nTime:\t\t\t{}'
                    '\nDuration:\t\t{}'
                    '\n\nOverall time:\t{}'
                ).format(
                    title, time, duration, all_time
                )
            else:
                msg = (
                    'Workshop title:\n\t{}'
                    '\nAuthor:\n\t{}'
                    '\nOverall time:\n\t{}'
                ).format(
                    wp.Workshop['Workshop'],
                    wp.Workshop['Author'],
                    all_time
                )
            sublime.message_dialog(msg)

        elif menu[i] == 'Material':
            materials = wp.getMaterials()
            material_uses = []
            material_blocks = ''
            for x in materials:
                material_uses.append(
                    '- {} ({})'.format(x, len(materials[x]))
                )
                material_blocks += '\'{}\' used in:\n{}\n\n'.format(
                    x, ', '.join(materials[x])
                )
            msg = 'Materials:\n\nUsages:\n{}\n\n{}'.format(
                '\n'.join(material_uses),
                material_blocks
            )
            sublime.message_dialog(msg)

        elif menu[i] == 'Add type':
            self.typeChoser()

        elif menu[i] == 'Add material':
            self.materialChoser(wp)

        elif menu[i] == 'Test':
            S = Settings()
            print(S.settings)

    def typeChoser(self):
        sublime.active_window().show_quick_panel(
            TYPES, on_select=self.selectType
        )

    def selectType(self, i):
        if i == -1:
            return False
        else:
            try:
                insert_me = TYPES[i]
                self.view.run_command('insert', {'characters': insert_me})
            except Exception:
                return False

    def materialChoser(self, wplan):
        self.used_materials = list(wplan.getMaterials().keys())
        sublime.active_window().show_quick_panel(
            self.used_materials, on_select=self.selectMaterial
        )

    def selectMaterial(self, i):
        if i == -1:
            return False
        else:
            try:
                insert_me = '\n- ' + self.used_materials[i]
                self.view.run_command('insert', {'characters': insert_me})
            except Exception:
                return False
