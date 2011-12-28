def create_button(text='', layout=None, tooltip=None, icon=None):
    if text:
        button.setText(tr(text))
    if tooltip is not None:
        button.setToolTip(tooltip)
class DockTitleBarWidget(QtGui.QWidget):
    def __init__(self, parent, title):
        QtGui.QWidget.__init__(self, parent)
        self.label = label = QtGui.QLabel()
        font = label.font()
        font.setCapitalization(QtGui.QFont.SmallCaps)
        label.setFont(font)
        label.setText(title)

        self.close_button = QtGui.QPushButton()
        self.close_button.setFlat(True)
        self.close_button.setFixedSize(QtCore.QSize(16, 16))
        self.close_button.setIcon(qtutils.titlebar_close_icon())

        self.toggle_button = QtGui.QPushButton()
        self.toggle_button.setFlat(True)
        self.toggle_button.setFixedSize(QtCore.QSize(16, 16))
        self.toggle_button.setIcon(qtutils.titlebar_normal_icon())

        self.corner_layout = QtGui.QHBoxLayout()
        self.corner_layout.setMargin(0)
        self.corner_layout.setSpacing(defs.spacing)

        layout = QtGui.QHBoxLayout()
        layout.setMargin(2)
        layout.setSpacing(defs.spacing)
        layout.addWidget(label)
        layout.addStretch()
        layout.addLayout(self.corner_layout)
        layout.addWidget(self.toggle_button)
        layout.addWidget(self.close_button)
        self.setLayout(layout)

        self.connect(self.toggle_button, SIGNAL('clicked()'),
                     self.toggle_floating)

        self.connect(self.close_button, SIGNAL('clicked()'),
                     self.parent().toggleViewAction().trigger)

    def toggle_floating(self):
        self.parent().setFloating(not self.parent().isFloating())

    def set_title(self, title):
        self.label.setText(title)

    def add_corner_widget(self, widget):
        self.corner_layout.addWidget(widget)


    titlebar = DockTitleBarWidget(dock, title)
    dock.setTitleBarWidget(titlebar)
def create_toolbutton(text=None, layout=None, tooltip=None, icon=None):
    button = QtGui.QToolButton()
class ExpandableGroupBox(QtGui.QGroupBox):
        self.expanded = True
        self.arrow_icon_size = 16
    def set_expanded(self, expanded):
        if expanded == self.expanded:
            self.emit(SIGNAL('expanded(bool)'), expanded)
            return
        self.expanded = expanded
            widget.setHidden(not expanded)
        self.emit(SIGNAL('expanded(bool)'), expanded)
            icon_size = self.arrow_icon_size
            offset = self.arrow_icon_size + defs.spacing
            adjusted = option.rect.adjusted(0, 0, -offset, 0)
            top_left = adjusted.topLeft()
            self.set_expanded(not self.expanded)
        painter.translate(self.arrow_icon_size + defs.spacing, 0)
        painter.drawText(option.rect, QtCore.Qt.AlignLeft, self.title())
        point = option.rect.adjusted(0, -4, 0, 0).topLeft()
        icon_size = self.arrow_icon_size
        if self.expanded:
        else:
            painter.drawPrimitive(style.PE_IndicatorArrowRight, option)
    def __init__(self, parent, provider=None):
        self._model = GitRefModel(parent, provider=provider)
    def __init__(self, parent=None, provider=None):
        self.refcompleter = GitRefCompleter(self, provider=provider)
        self.refcompleter.popup().installEventFilter(self)

    def eventFilter(self, obj, event):
        """Fix an annoyance on OS X

        The completer popup steals focus.  Work around it.
        This affects dialogs without QtCore.Qt.WindowModal modality.

        """
        if obj == self.refcompleter.popup():
            if event.type() == QtCore.QEvent.FocusIn:
                return True
        return False

    def mouseReleaseEvent(self, event):
        super(GitRefLineEdit, self).mouseReleaseEvent(event)
        self.refcompleter.complete()


class GitRefDialog(QtGui.QDialog):
    def __init__(self, title, button_text, parent, provider=None):
        super(GitRefDialog, self).__init__(parent)
        self.setWindowTitle(title)

        self.label = QtGui.QLabel()
        self.label.setText(title)

        self.lineedit = GitRefLineEdit(self, provider=provider)
        self.setFocusProxy(self.lineedit)

        self.ok_button = QtGui.QPushButton()
        self.ok_button.setText(self.tr(button_text))
        self.ok_button.setIcon(qtutils.apply_icon())

        self.close_button = QtGui.QPushButton()
        self.close_button.setText(self.tr('Close'))

        self.button_layout = QtGui.QHBoxLayout()
        self.button_layout.setMargin(0)
        self.button_layout.setSpacing(defs.button_spacing)
        self.button_layout.addStretch()
        self.button_layout.addWidget(self.ok_button)
        self.button_layout.addWidget(self.close_button)

        self.main_layout = QtGui.QVBoxLayout()
        self.main_layout.setMargin(defs.margin)
        self.main_layout.setSpacing(defs.spacing)

        self.main_layout.addWidget(self.label)
        self.main_layout.addWidget(self.lineedit)
        self.main_layout.addLayout(self.button_layout)
        self.setLayout(self.main_layout)

        qtutils.connect_button(self.ok_button, self.accept)
        qtutils.connect_button(self.close_button, self.reject)

        self.connect(self.lineedit, SIGNAL('textChanged(QString)'),
                     self.text_changed)

        self.setWindowModality(QtCore.Qt.WindowModal)
        self.ok_button.setEnabled(False)

    def text(self):
        return unicode(self.lineedit.text())

    def text_changed(self, txt):
        self.ok_button.setEnabled(bool(self.text()))

    @staticmethod
    def ref(title, button_text, parent, provider=None):
        dlg = GitRefDialog(title, button_text, parent, provider=provider)
        dlg.show()
        dlg.raise_()
        dlg.setFocus()
        if dlg.exec_() == GitRefDialog.Accepted:
            return dlg.text()
        else:
            return None


class GitRefProvider(QtCore.QObject):
    def __init__(self, pre=None):
        super(GitRefProvider, self).__init__()
        if pre:
            self.pre = pre
        else:
            self.pre = []
        self.model = model = cola.model()
        msg = model.message_updated
        model.add_observer(msg, self.emit_updated)

    def emit_updated(self):
        self.emit(SIGNAL('updated()'))

    def matches(self):
        model = self.model
        return self.pre + model.local_branches + model.remote_branches + model.tags

    def dispose(self):
        self.model.remove_observer(self.emit_updated)
    def __init__(self, parent, provider=None):

        if provider is None:
            provider = GitRefProvider()
        self.provider = provider
        self.connect(self.provider, SIGNAL('updated()'),
                     self.update_matches)

        self.provider.dispose()
        for match in self.provider.matches():
def rgba(r, g, b, a=255):
    c = QColor()
    c.setRgb(r, g, b)
    c.setAlpha(a)
    return c
    'color_text':           rgba(0x00, 0x00, 0x00),
    'color_add':            rgba(0xcd, 0xff, 0xe0),
    'color_remove':         rgba(0xff, 0xd0, 0xd0),
    'color_header':         rgba(0xbb, 0xbb, 0xbb),
        diff_head = self.mkformat(fg=self.color_header)
        diff_head_bold = self.mkformat(fg=self.color_header, bold=True)
        diff_add = self.mkformat(fg=self.color_text, bg=self.color_add)
        diff_remove = self.mkformat(fg=self.color_text, bg=self.color_remove)
            bad_ws = self.mkformat(fg=Qt.black, bg=Qt.red)
        diff_old_rgx = TERMINAL(r'^--- ')
        diff_new_rgx = TERMINAL(r'^\+\+\+ ')
        diff_ctx_rgx = TERMINAL(r'^@@ ')

        diff_hd1_rgx = TERMINAL(r'^diff --git a/.*b/.*')
        diff_hd2_rgx = TERMINAL(r'^index \S+\.\.\S+')
        diff_hd3_rgx = TERMINAL(r'^new file mode')
        diff_hd4_rgx = TERMINAL(r'^deleted file mode')
        diff_add_rgx = TERMINAL(r'^\+')
        diff_rmv_rgx = TERMINAL(r'^-')
        diff_bar_rgx = TERMINAL(r'^([ ]+.*)(\|[ ]+\d+[ ]+[+-]+)$')
        diff_sts_rgx = (r'(.+\|.+?)(\d+)(.+?)([\+]*?)([-]*?)$')
        diff_sum_rgx = (r'(\s+\d+ files changed[^\d]*)'
                        r'(:?\d+ insertions[^\d]*)'
                        r'(:?\d+ deletions.*)$')

        self.create_rules(diff_old_rgx,     diff_head,
                          diff_new_rgx,     diff_head,
                          diff_ctx_rgx,     diff_head_bold,
                          diff_bar_rgx,     (diff_head_bold, diff_head),
                          diff_hd4_rgx,     diff_head,
                          diff_sts_rgx,     (None, diff_head,
                                             None, diff_head,
                                             diff_head),
                          diff_sum_rgx,     (diff_head,
                                             diff_head,
                                             diff_head))
            font.setPointSize(12)