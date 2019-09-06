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
            'Overall time',
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
                msg = self.getOverallTimeInfo(wp)
            sublime.message_dialog(msg)

        elif menu[i] == 'Overall time':
            msg = self.getOverallTimeInfo(wp)
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

    def getOverallTimeInfo(self, wplan):
        ratios = self.getRatiosString(wplan.Workshop['Types'])
        return (
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
            '\n'
            '\nRatios:'
            '\n{}'
        ).format(
            wplan.Workshop['Workshop'],
            wplan.Workshop['Author'],
            wplan.Workshop['Length string'],
            wplan.Workshop['Start absolute string'],
            wplan.Workshop['End absolute string'],
            ratios
        )

    def getRatiosString(self, typ):
        out = ''
        for x in typ:
            out += '\t{} -- {} -- {} %\n'.format(
                x, typ[x]['Length string'], typ[x]['Length percentage']
            )
        return out

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
        self.used_materials = list(wplan.Workshop['Materials'].keys())
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


class WorkshopplanlistCommand(sublime_plugin.TextCommand):
    def run(self, edit):
        self.initContent()
        self.initMenu()

    def initMenu(self):
        self.menu = self.generateMenu()
        sublime.active_window().show_quick_panel(
            self.menu, on_highlight=self.select, on_select=None
        )

    def initContent(self):
        self.cursor_start = self.view.sel()[0].begin()
        self.all_region = sublime.Region(0, self.view.size())
        self.all_content = self.view.substr(self.all_region)
        self.wp = WPlan(self.all_content)

    def generateMenu(self):
        out = []
        for x in self.wp.Blocks:
            head = '{}  --  {}'.format(
                x['Title'],
                x['Type']
            )
            sub = '{} ==> {} - {}'.format(
                x['Length string'],
                x['Start absolute string'],
                x['End absolute string']
            )
            out.append([head, sub])
        return out

    def select(self, i):
        if i == -1:
            return False

        else:
            try:
                self.highlight(i)
            except Exception:
                return False

    def highlight(self, i):
        where = self.generateRegionFromWP(i)
        self.view.sel().clear()
        self.view.sel().add(where)
        self.view.show(where)
        self.update_view()

    def update_view(self):
        """
        Update the view.

        This method only exists due to a Sublime plugin bug.
        """
        self.view.add_regions("bug", sublime.Region(0, 0))
        self.view.erase_regions("bug")

    def generateRegionFromWP(self, index):
        return sublime.Region(
            self.wp.Blocks[index]['Position start'],
            self.wp.Blocks[index]['Position end']
        )
