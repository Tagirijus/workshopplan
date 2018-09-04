import sublime
import sublime_plugin
from .general.wplan import WPlan
from .general.wplan import TYPES


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
            'Add material'
        ]

    def select(self, i):
        menu = self.generateMenu()
        wp = WPlan(self.all_content)

        if i == -1:
            return False

        elif menu[i] == 'Time':
            index = wp.getActualIndex(self.cursor_start)
            if index != -1:
                msg = (
                    'Block information'
                    '\n'
                    '\nTitle:'
                    '\n\t{}'
                    '\n'
                    '\nLength:'
                    '\n\t{}'
                    '\n'
                    '\nTime (relative):'
                    '\n\t{} - {}'
                    '\n'
                    '\nTime (absolute):'
                    '\n\t{} - {}'
                    '\n'
                    '\nOverall length:'
                    '\n\t{}'
                ).format(
                    wp.Blocks[index]['Title'],
                    wp.Blocks[index]['Length string'],
                    wp.Blocks[index]['Start relative string'],
                    wp.Blocks[index]['End relative string'],
                    wp.Blocks[index]['Start absolute string'],
                    wp.Blocks[index]['End absolute string'],
                    wp.Workshop['Length string']
                )
            else:
                msg = (
                    'Workshop title:'
                    '\n\t{}'
                    '\n'
                    '\nAuthor:'
                    '\n\t{}'
                    '\n'
                    '\nOverall length:'
                    '\n\t{}'
                    '\n'
                    '\nTime:'
                    '\n\t{} - {}'
                ).format(
                    wp.Workshop['Workshop'],
                    wp.Workshop['Author'],
                    wp.Workshop['Length string'],
                    wp.Workshop['Start absolute string'],
                    wp.Workshop['End absolute string'],
                )
            sublime.message_dialog(msg)

        elif menu[i] == 'Material':
            material_uses = []
            material_blocks = ''
            for x in wp.Workshop['Materials']:
                material_uses.append(
                    '- {} ({})'.format(x, len(wp.Workshop['Materials'][x]))
                )
                material_blocks += '\'{}\' used in:\n{}\n\n'.format(
                    x, ', '.join(wp.Workshop['Materials'][x])
                )
            msg = (
                'Materials:\n'
                '\nUsages:\n{}'
                '\n'
                '\n{}'
            ).format(
                '\n'.join(material_uses),
                material_blocks
            )
            sublime.message_dialog(msg)

        elif menu[i] == 'Add type':
            self.typeChoser()

        elif menu[i] == 'Add material':
            self.materialChoser(wp)

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
