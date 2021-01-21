from typing import Optional
from mypy.nodes import ClassDef, ListExpr, NameExpr, SymbolTableNode, TypeInfo
from mypy.plugin import ClassDefContext, Plugin
from mypy.semanal import SemanticAnalyzer



def lookup_in_subsets(typeinfo: TypeInfo, name: str):
    subsets: Optional[SymbolTableNode] = typeinfo._subsets_
    for subset in subsets.items:
        subset_typeinfo = subset.node
        res = subset_typeinfo.names.get(name) or lookup_in_subsets(subset_typeinfo, name)
        if res:
            return res


def custom_get(self: TypeInfo, name: str):
    if name in ('__subsets__', '__supersets__'):
        return self.names.get(name)

    if name.startswith('__'):
        return TypeInfo.get(self, name)
    
    if name in self.names:
        return self.names.get(name)
    else:
        return lookup_in_subsets(self, name)


def customize_setenum_typeinfo(classdef_ctx: ClassDefContext):
    if not classdef_ctx.cls.base_type_exprs:
        return

    base_cls_expr = classdef_ctx.cls.base_type_exprs[0]
    if not isinstance(base_cls_expr, NameExpr):
        return
    
    if not (
        base_cls_expr.node
        and isinstance(base_cls_expr.node, TypeInfo)
        and base_cls_expr.node.defn.fullname == 'setenum.SetEnum'
    ):
        return
    
    current_cls: ClassDef = classdef_ctx.cls
    current_info: TypeInfo = classdef_ctx.cls.info
    api: SemanticAnalyzer = classdef_ctx.api

    print('[DEBUG] Analyze', current_cls.fullname)
    current_info.get = custom_get.__get__(current_cls.info)

    # TODO: this is strange way to find subsets values
    subsets, supersets = ListExpr(items=[]), ListExpr(items=[])
        
    for assign_stmt in current_cls.defs.body:
        # Multiple assignments are not allowed
        if len(assign_stmt.lvalues) != 1:
            api.fail('Avoid using multiple assignment with SetEnum', assign_stmt)
            continue
        
        lvalue = assign_stmt.lvalues[0]
        if not isinstance(lvalue, NameExpr):
            api.fail('Too hard to deduce for now', assign_stmt)
            continue

        if lvalue.name == '__subsets__':
            subsets = assign_stmt.rvalue
        elif lvalue.name == '__supersets__':
            supersets = assign_stmt.rvalue
    
    # TODO: read about mypy caching, and how it can affect this
    current_info._subsets_ = subsets
    
    for subset_name in subsets.items:
        subset_typeinfo: TypeInfo = api.lookup_qualified(subset_name.name, classdef_ctx).node
        subset_typeinfo.mro.insert(1, classdef_ctx.cls.info)

    for superset_name in supersets.items:
        superset_typeinfo = api.lookup_qualified(superset_name.name, classdef_ctx).node
        classdef_ctx.cls.info.mro.insert(1, superset_typeinfo)

        # .accept() binds new_name_expr.node to correct TypeInfo
        new_name_expr: NameExpr = NameExpr(classdef_ctx.cls.name)
        new_name_expr.accept(classdef_ctx.api)
        # We expect superset_typeinfo._subsets_ to be populated:
        #
        # __subsets__ can only target to class that is defined before current one
        # as classes are analyzed in order of definition, references superset typeinfo
        # is already analyzed with this plugin, thus has _subsets_ attribute
        superset_typeinfo._subsets_.items.append(new_name_expr)
    

class CustomPlugin(Plugin):
    def get_base_class_hook(self, fullname: str):
        if fullname == 'setenum.SetEnum':
            return customize_setenum_typeinfo


def plugin(version: str):
    # no version restrictions yet
    return CustomPlugin
