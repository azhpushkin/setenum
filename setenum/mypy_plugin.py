from typing import Optional
from mypy.nodes import (
    AssignmentStmt, Block, ClassDef, ListExpr,
    NameExpr, SymbolTable, SymbolTableNode, TypeInfo
)
from mypy.plugin import ClassDefContext, Plugin



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
    

class CustomPlugin(Plugin):
    
    def get_base_class_hook(self, fullname: str):
        if fullname == 'setenum.SetEnum':
            return self.analyze
    
    # def get_customize_class_mro_hook(self, fullname: str):
    #     # TODO: return analyze only for setenum ancestors or IDK
    #     return analyze

    @classmethod
    def analyze(cls, classdef_ctx):
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
        
        print('### Analyze', classdef_ctx.cls.fullname)
        classdef_ctx.cls.info.get = custom_get.__get__(classdef_ctx.cls.info)

        # TODO: this is strange way to find subsets values
        subsets, supersets = ListExpr(items=[]), ListExpr(items=[])
            
        for assign_stmt in classdef_ctx.cls.defs.body:
            # Multiple assignments are not allowed
            if len(assign_stmt.lvalues) != 1:
                classdef_ctx.api.fail('Avoid using multiple assignment with SetEnum', assign_stmt)
                continue
            
            lvalue = assign_stmt.lvalues[0]
            if not isinstance(lvalue, NameExpr):
                classdef_ctx.api.fail('Too hard to deduce for now', assign_stmt)
                continue

            if lvalue.name == '__subsets__':
                subsets = assign_stmt.rvalue
            elif lvalue.name == '__supersets__':
                supersets = assign_stmt.rvalue
        
        # TODO: read about mypy caching, and how it can affect this
        classdef_ctx.cls.info._subsets_ = subsets
        
        for subset_name in subsets.items:
            res: TypeInfo = classdef_ctx.api.lookup_qualified(subset_name.name, classdef_ctx).node
            res.mro.insert(1, classdef_ctx.cls.info)

        for superset_name in supersets.items:
            new_name_expr: NameExpr = NameExpr(classdef_ctx.cls.name)
            new_name_expr.accept(classdef_ctx.api)
            
            res = classdef_ctx.api.lookup_qualified(superset_name.name, classdef_ctx).node
            classdef_ctx.cls.info.mro.insert(1, res)

            res._subsets_.items.append(new_name_expr)
                
        

def plugin(version: str):
    # no version restrictions yet
    return CustomPlugin