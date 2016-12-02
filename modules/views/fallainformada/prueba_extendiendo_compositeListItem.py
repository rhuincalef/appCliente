from kivy.adapters.models import SelectableDataItem
from kivy.uix.behaviors import ButtonBehavior
from kivy.uix.button import Button
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.listview import ListItemButton, ListItemLabel, \
        CompositeListItem, ListView, SelectableView
from kivy.uix.gridlayout import GridLayout
from kivy.properties import ListProperty
from kivy.properties import ObjectProperty

import inspect
from kivy.event import EventDispatcher
from kivy.adapters.adapter import Adapter
from kivy.properties import DictProperty
from kivy.properties import BooleanProperty
from kivy.properties import OptionProperty
from kivy.properties import NumericProperty
from kivy.lang import Builder

class MyListItemButton(SelectableView, Button):
    ''':class:`~kivy.uix.listview.ListItemButton` mixes
    :class:`~kivy.uix.listview.SelectableView` with
    :class:`~kivy.uix.button.Button` to produce a button suitable for use in
    :class:`~kivy.uix.listview.ListView`.
    '''

    selected_color = ListProperty([1., 0., 0., 1])
    '''
    :data:`selected_color` is a :class:`~kivy.properties.ListProperty`,
    default to [1., 0., 0., 1].
    '''

    deselected_color = ListProperty([0., 1., 0., 1])
    '''
    :data:`selected_color` is a :class:`~kivy.properties.ListProperty`,
    default to [0., 1., 0., 1].
    '''

    # CLYDE: Added composite
    composite = ObjectProperty(None)

    def __init__(self, **kwargs):
        super(MyListItemButton, self).__init__(**kwargs)

        # CLYDE: I don't recall why this is here, but it must have caused us
        #        some problems. Commented out the background_color set.
        # Set Button bg color to be deselected_color.
        #self.background_color = self.deselected_color

    def select(self, *args):
        self.background_color = self.selected_color
        if type(self.parent) is CompositeListItem:
            self.parent.select_from_child(self, *args)

    def deselect(self, *args):
        self.background_color = self.deselected_color
        if type(self.parent) is CompositeListItem:
            self.parent.deselect_from_child(self, *args)

    def select_from_composite(self, *args):
        self.background_color = self.selected_color

    def deselect_from_composite(self, *args):
        self.background_color = self.deselected_color

    def __repr__(self):
        return '<%s text=%s>' % (self.__class__.__name__, self.text)


class MyListItemLabel(SelectableView, Label):
    ''':class:`~kivy.uix.listview.ListItemLabel` mixes
    :class:`~kivy.uix.listview.SelectableView` with
    :class:`~kivy.uix.label.Label` to produce a label suitable for use in
    :class:`~kivy.uix.listview.ListView`.
    '''

    # CLYDE: Added composite
    composite = ObjectProperty(None)

    def __init__(self, **kwargs):
        super(MyListItemLabel, self).__init__(**kwargs)

    def select(self, *args):
        self.bold = True
        if type(self.parent) is CompositeListItem:
            self.parent.select_from_child(self, *args)

    def deselect(self, *args):
        self.bold = False
        if type(self.parent) is CompositeListItem:
            self.parent.deselect_from_child(self, *args)

    def select_from_composite(self, *args):
        self.bold = True

    def deselect_from_composite(self, *args):
        self.bold = False

    def __repr__(self):
        return '<%s text=%s>' % (self.__class__.__name__, self.text)


class CompositeListAdapter(Adapter, EventDispatcher):
    '''
    A base class for adapters interfacing with lists, dictionaries or other
    collection type data, adding selection, view creation and management
    functonality.
    '''

    data = ListProperty([])
    '''The data list property is redefined here, overriding its definition as
    an ObjectProperty in the Adapter class. We bind to data so that any
    changes will trigger updates. See also how the
    :class:`~kivy.adapters.DictAdapter` redefines data as a
    :class:`~kivy.properties.DictProperty`.

    :data:`data` is a :class:`~kivy.properties.ListProperty` and defaults
    to [].
    '''

    selection = ListProperty([])
    '''The selection list property is the container for selected items.

    :data:`selection` is a :class:`~kivy.properties.ListProperty` and defaults
    to [].
    '''

    selection_mode = OptionProperty('single',
            options=('none', 'single', 'multiple'))
    '''Selection modes:

       * *none*, use the list as a simple list (no select action). This option
         is here so that selection can be turned off, momentarily or
         permanently, for an existing list adapter.
         A :class:`~kivy.adapters.listadapter.ListAdapter` is not meant to be
         used as a primary no-selection list adapter.  Use a
         :class:`~kivy.adapters.simplelistadapter.SimpleListAdapter` for that.

       * *single*, multi-touch/click ignored. Single item selection only.

       * *multiple*, multi-touch / incremental addition to selection allowed;
         may be limited to a count by selection_limit

    :data:`selection_mode` is an :class:`~kivy.properties.OptionProperty` and
    defaults to 'single'.
    '''

    propagate_selection_to_data = BooleanProperty(False)
    '''Normally, data items are not selected/deselected because the data items
    might not have an is_selected boolean property -- only the item view for a
    given data item is selected/deselected as part of the maintained selection
    list. However, if the data items do have an is_selected property, or if
    they mix in :class:`~kivy.adapters.models.SelectableDataItem`, the
    selection machinery can propagate selection to data items. This can be
    useful for storing selection state in a local database or backend database
    for maintaining state in game play or other similar scenarios. It is a
    convenience function.

    To propagate selection or not?

    Consider a shopping list application for shopping for fruits at the
    market. The app allows for the selection of fruits to buy for each day of
    the week, presenting seven lists: one for each day of the week. Each list is
    loaded with all the available fruits, but the selection for each is a
    subset. There is only one set of fruit data shared between the lists, so
    it would not make sense to propagate selection to the data because
    selection in any of the seven lists would clash and mix with that of the
    others.

    However, consider a game that uses the same fruits data for selecting
    fruits available for fruit-tossing. A given round of play could have a
    full fruits list, with fruits available for tossing shown selected. If the
    game is saved and rerun, the full fruits list, with selection marked on
    each item, would be reloaded correctly if selection is always propagated to
    the data. You could accomplish the same functionality by writing code to
    operate on list selection, but having selection stored in the data
    ListProperty might prove convenient in some cases.

    :data:`propagate_selection_to_data` is a
    :class:`~kivy.properties.BooleanProperty` and defaults to False.
    '''

    allow_empty_selection = BooleanProperty(True)
    '''The allow_empty_selection may be used for cascading selection between
    several list views, or between a list view and an observing view. Such
    automatic maintenance of the selection is important for all but simple
    list displays. Set allow_empty_selection to False and the selection is
    auto-initialized and always maintained, so any observing views
    may likewise be updated to stay in sync.

    :data:`allow_empty_selection` is a
    :class:`~kivy.properties.BooleanProperty` and defaults to True.
    '''

    selection_limit = NumericProperty(-1)
    '''When the selection_mode is multiple and the selection_limit is
    non-negative, this number will limit the number of selected items. It can
    be set to 1, which is equivalent to single selection. If selection_limit is
    not set, the default value is -1, meaning that no limit will be enforced.

    :data:`selection_limit` is a :class:`~kivy.properties.NumericProperty` and
    defaults to -1 (no limit).
    '''

    cached_views = DictProperty({})
    '''View instances for data items are instantiated and managed by the
    adapter. Here we maintain a dictionary containing the view
    instances keyed to the indices in the data.

    This dictionary works as a cache. get_view() only asks for a view from
    the adapter if one is not already stored for the requested index.

    :data:`cached_views` is a :class:`~kivy.properties.DictProperty` and
    defaults to {}.
    '''

    __events__ = ('on_selection_change', )

    def __init__(self, **kwargs):
        super(CompositeListAdapter, self).__init__(**kwargs)

        self.bind(selection_mode=self.selection_mode_changed,
                  allow_empty_selection=self.check_for_empty_selection,
                  data=self.update_for_new_data)

        self.update_for_new_data()

    def delete_cache(self, *args):
        self.cached_views = {}

    def get_count(self):
        return len(self.data)

    def get_data_item(self, index):
        if index < 0 or index >= len(self.data):
            return None
        return self.data[index]

    def selection_mode_changed(self, *args):
        if self.selection_mode == 'none':
            for selected_view in self.selection:
                self.deselect_item_view(selected_view)
        else:
            self.check_for_empty_selection()

    def get_view(self, index):
        if index in self.cached_views:
            return self.cached_views[index]
        item_view = self.create_view(index)
        if item_view:
            self.cached_views[index] = item_view
        return item_view

    def create_view(self, index):
        '''This method is more complicated than the one in
        :class:`kivy.adapters.adapter.Adapter` and
        :class:`kivy.adapters.simplelistadapter.SimpleListAdapter`, because
        here we create bindings for the data item and its children back to
        self.handle_selection(), and do other selection-related tasks to keep
        item views in sync with the data.
        '''
        item = self.get_data_item(index)
        if item is None:
            return None

        item_args = self.args_converter(index, item)

        item_args['index'] = index

        if self.cls:
            view_instance = self.cls(**item_args)
        else:
            view_instance = Builder.template(self.template, **item_args)

        if self.propagate_selection_to_data:
            # The data item must be a subclass of SelectableDataItem, or must
            # have an is_selected boolean or function, so it has is_selected
            # available.  If is_selected is unavailable on the data item, an
            # exception is raised.
            #
            if isinstance(item, SelectableDataItem):
                if item.is_selected:
                    self.handle_selection(view_instance)
            elif type(item) == dict and 'is_selected' in item:
                if item['is_selected']:
                    self.handle_selection(view_instance)
            elif hasattr(item, 'is_selected'):
                if (inspect.isfunction(item.is_selected)
                        or inspect.ismethod(item.is_selected)):
                    if item.is_selected():
                        self.handle_selection(view_instance)
                else:
                    if item.is_selected:
                        self.handle_selection(view_instance)
            else:
                msg = "ListAdapter: unselectable data item for {0}"
                raise Exception(msg.format(index))

        view_instance.bind(on_release=self.handle_selection)

        for child in view_instance.children:
            child.bind(on_release=self.handle_selection)

        # CLYDE: Added this:
        if view_instance.is_selected:
            self.selection.append(view_instance)

        return view_instance

    def on_selection_change(self, *args):
        '''on_selection_change() is the default handler for the
        on_selection_change event.
        '''
        pass

    def handle_selection(self, view, hold_dispatch=False, *args):

        # CLYDE: Added this if:
        if type(view) is not MyCompositeListItem:
            view = view.composite

        if view not in self.selection:
            if self.selection_mode in ['none', 'single'] and \
                    len(self.selection) > 0:
                for selected_view in self.selection:
                    self.deselect_item_view(selected_view)
            if self.selection_mode != 'none':
                if self.selection_mode == 'multiple':
                    if self.allow_empty_selection:
                        # If < 0, selection_limit is not active.
                        if self.selection_limit < 0:
                            self.select_item_view(view)
                        else:
                            if len(self.selection) < self.selection_limit:
                                self.select_item_view(view)
                    else:
                        self.select_item_view(view)
                else:
                    self.select_item_view(view)
        else:
            self.deselect_item_view(view)
            if self.selection_mode != 'none':
                # If the deselection makes selection empty, the following call
                # will check allows_empty_selection, and if False, will
                # select the first item. If view happens to be the first item,
                # this will be a reselection, and the user will notice no
                # change, except perhaps a flicker.
                #
                self.check_for_empty_selection()

        if not hold_dispatch:
            self.dispatch('on_selection_change')

    def select_data_item(self, item):
        self.set_data_item_selection(item, True)

    def deselect_data_item(self, item):
        self.set_data_item_selection(item, False)

    def set_data_item_selection(self, item, value):
        if isinstance(item, SelectableDataItem):
            item.is_selected = value
        elif type(item) == dict:
            item['is_selected'] = value
        elif hasattr(item, 'is_selected'):
            if (inspect.isfunction(item.is_selected)
                    or inspect.ismethod(item.is_selected)):
                item.is_selected()
            else:
                item.is_selected = value

    def select_item_view(self, view):
        view.select()
        view.is_selected = True
        self.selection.append(view)

        # [TODO] sibling selection for composite items
        #        Needed? Or handled from parent?
        #        (avoid circular, redundant selection)
        #if hasattr(view, 'parent') and hasattr(view.parent, 'children'):
         #siblings = [child for child in view.parent.children if child != view]
         #for sibling in siblings:
             #if hasattr(sibling, 'select'):
                 #sibling.select()

        if self.propagate_selection_to_data:
            data_item = self.get_data_item(view.index)
            self.select_data_item(data_item)

    def select_list(self, view_list, extend=True):
        '''The select call is made for the items in the provided view_list.

        Arguments:

            view_list: the list of item views to become the new selection, or
            to add to the existing selection

            extend: boolean for whether or not to extend the existing list
        '''
        if not extend:
            self.selection = []

        for view in view_list:
            self.handle_selection(view, hold_dispatch=True)

        self.dispatch('on_selection_change')

    def deselect_item_view(self, view):
        view.deselect()
        view.is_selected = False
        self.selection.remove(view)

        # [TODO] sibling deselection for composite items
        #        Needed? Or handled from parent?
        #        (avoid circular, redundant selection)
        #if hasattr(view, 'parent') and hasattr(view.parent, 'children'):
         #siblings = [child for child in view.parent.children if child != view]
         #for sibling in siblings:
             #if hasattr(sibling, 'deselect'):
                 #sibling.deselect()

        if self.propagate_selection_to_data:
            item = self.get_data_item(view.index)
            self.deselect_data_item(item)

    def deselect_list(self, l):
        for view in l:
            self.handle_selection(view, hold_dispatch=True)

        self.dispatch('on_selection_change')

    # [TODO] Could easily add select_all() and deselect_all().

    def update_for_new_data(self, *args):
        self.delete_cache()
        self.initialize_selection()

    def initialize_selection(self, *args):
        if len(self.selection) > 0:
            self.selection = []
            self.dispatch('on_selection_change')

        self.check_for_empty_selection()

    def check_for_empty_selection(self, *args):
        if not self.allow_empty_selection:
            if len(self.selection) == 0:
                # Select the first item if we have it.
                v = self.get_view(0)
                if v is not None:
                    self.handle_selection(v)

    # [TODO] Also make methods for scroll_to_sel_start, scroll_to_sel_end,
    #        scroll_to_sel_middle.

    def trim_left_of_sel(self, *args):
        '''Cut list items with indices in sorted_keys that are less than the
        index of the first selected item if there is a selection.
        '''
        if len(self.selection) > 0:
            first_sel_index = min([sel.index for sel in self.selection])
            self.data = self.data[first_sel_index:]

    def trim_right_of_sel(self, *args):
        '''Cut list items with indices in sorted_keys that are greater than
        the index of the last selected item if there is a selection.
        '''
        if len(self.selection) > 0:
            last_sel_index = max([sel.index for sel in self.selection])
            self.data = self.data[:last_sel_index + 1]

    def trim_to_sel(self, *args):
        '''Cut list items with indices in sorted_keys that are les than or
        greater than the index of the last selected item if there is a
        selection. This preserves intervening list items within the selected
        range.
        '''
        if len(self.selection) > 0:
            sel_indices = [sel.index for sel in self.selection]
            first_sel_index = min(sel_indices)
            last_sel_index = max(sel_indices)
            self.data = self.data[first_sel_index:last_sel_index + 1]

    def cut_to_sel(self, *args):
        '''Same as trim_to_sel, but intervening list items within the selected
        range are also cut, leaving only list items that are selected.
        '''
        if len(self.selection) > 0:
            self.data = self.selection
class DataItem(SelectableDataItem):
    def __init__(self, **kwargs):
       super(DataItem, self).__init__(**kwargs)
       self.name = kwargs.get('name', '')
       self.is_selected = kwargs.get('is_selected', False)

data_items = [DataItem(name='cat', is_selected=False),
              DataItem(name='dog', is_selected=False),
              DataItem(name='frog', is_selected=False),
              DataItem(name='armadillo', is_selected=False),
              DataItem(name='fox', is_selected=False),
              DataItem(name='racoon', is_selected=False),
              DataItem(name='cow', is_selected=True),
              DataItem(name='horse', is_selected=False),
              DataItem(name='giraffe', is_selected=False),
              DataItem(name='elephant', is_selected=True),
              DataItem(name='deer', is_selected=False),
              DataItem(name='bear', is_selected=False)]


class MyCompositeListItem(ButtonBehavior, SelectableView, BoxLayout):
    ''':class:`~kivy.uix.listview.CompositeListItem` mixes
    :class:`~kivy.uix.listview.SelectableView` with :class:`BoxLayout` for a
    generic container-style list item, to be used in
    :class:`~kivy.uix.listview.ListView`.
    '''

    background_color = ListProperty([1, 1, 1, 1])
    '''ListItem sublasses Button, which has background_color, but
    for a composite list item, we must add this property.

    :data:`background_color` is a :class:`~kivy.properties.ListProperty`,
    default to [1, 1, 1, 1].
    '''

    selected_color = ListProperty([1., 0., 0., 1])
    '''
    :data:`selected_color` is a :class:`~kivy.properties.ListProperty`,
    default to [1., 0., 0., 1].
    '''

    deselected_color = ListProperty([.33, .33, .33, 1])
    '''
    :data:`deselected_color` is a :class:`~kivy.properties.ListProperty`,
    default to [.33, .33, .33, 1].
    '''

    representing_cls = ObjectProperty(None)
    '''Which component view class, if any, should represent for the
    composite list item in __repr__()?

    :data:`representing_cls` is an :class:`~kivy.properties.ObjectProperty`,
    default to None.
    '''

    def __init__(self, **kwargs):
        super(MyCompositeListItem, self).__init__(**kwargs)

        # Example data:
        #
        #    'cls_dicts': [{'cls': ListItemButton,
        #                   'kwargs': {'text': "Left"}},
        #                   'cls': ListItemLabel,
        #                   'kwargs': {'text': "Middle",
        #                              'is_representing_cls': True}},
        #                   'cls': ListItemButton,
        #                   'kwargs': {'text': "Right"}]

        # There is an index to the data item this composite list item view
        # represents. Get it from kwargs and pass it along to children in the
        # loop below.
        index = kwargs['index']

        for cls_dict in kwargs['cls_dicts']:
            cls = cls_dict['cls']
            cls_kwargs = cls_dict.get('kwargs', None)

            if cls_kwargs:
                cls_kwargs['index'] = index
                cls_kwargs['is_selected'] = self.is_selected
                cls_kwargs['composite'] = self

                # CLYDE: this code is affecting the value of self, so the
                #        parent is wrong when that happens for buttons.
                #        So, these lines commented out.

                #if 'selection_target' not in cls_kwargs:
                    #cls_kwargs['selection_target'] = self

                #if 'text' not in cls_kwargs:
                    #cls_kwargs['text'] = kwargs['text']

                #if 'is_representing_cls' in cls_kwargs:
                    #self.representing_cls = cls

                view_instance = cls(**cls_kwargs)
            else:
                cls_kwargs = {}
                cls_kwargs['index'] = index
                cls_kwargs['is_selected'] = self.is_selected
                cls_kwargs['composite'] = self

                if 'text' in kwargs:
                    cls_kwargs['text'] = kwargs['text']
                view_instance = cls(**cls_kwargs)

            if self.is_selected:
                view_instance.select_from_composite()
            else:
                view_instance.deselect_from_composite()

            self.add_widget(view_instance)

    def select(self, *args):
        self.background_color = self.selected_color
        for child in self.children:
            child.is_selected = True
            child.select_from_composite()

    def deselect(self, *args):
        self.background_color = self.deselected_color
        for child in self.children:
            child.is_selected = False
            child.deselect_from_composite()

    def select_from_child(self, child, *args):
        for c in self.children:
            if c is not child:
                child.is_selected = True
                c.select_from_composite(*args)

    def deselect_from_child(self, child, *args):
        for c in self.children:
            if c is not child:
                child.is_selected = False
                c.deselect_from_composite(*args)

    def __repr__(self):
        if self.representing_cls is not None:
            return '<%r>, representing <%s>' % (
                self.representing_cls, self.__class__.__name__)
        else:
            return '<%s>' % (self.__class__.__name__)










class MainView(GridLayout):
    '''Uses :class:`CompositeListItem` for list item views comprised by two
    :class:`ListItemButton`s and one :class:`ListItemLabel`. Illustrates how
    to construct the fairly involved args_converter used with
    :class:`CompositeListItem`.
    '''

    def __init__(self, **kwargs):
        kwargs['cols'] = 2
        super(MainView, self).__init__(**kwargs)

        # This is quite an involved args_converter, so we should go through the
        # details. A CompositeListItem instance is made with the args
        # returned by this converter. The first three, text, size_hint_y,
        # height are arguments for CompositeListItem. The cls_dicts list contains
        # argument sets for each of the member widgets for this composite:
        # ListItemButton and ListItemLabel.
        args_converter = \
            lambda row_index, obj: \
                {'text': obj.name,
                 'size_hint_y': None,
                 'height': 25,
                 'is_selected': obj.is_selected,
                 'cls_dicts': [{'cls': MyListItemButton,
                                'kwargs': {'text': obj.name}},
                               {'cls': MyListItemLabel,
                                'kwargs': {'text': "Middle-{0}".format(obj.name),
                                           'is_representing_cls': True}},
                               {'cls': MyListItemButton,
                                'kwargs': {'text': obj.name}}]}

        list_adapter = CompositeListAdapter(data=data_items,
                                            args_converter=args_converter,
                                            selection_mode='multiple',
                                            allow_empty_selection=True,
                                            cls=MyCompositeListItem)

        # Use the adapter in our ListView:
        list_view = ListView(adapter=list_adapter)

        self.add_widget(list_view)


if __name__ == '__main__':
    from kivy.base import runTouchApp
    runTouchApp(MainView(width=800))