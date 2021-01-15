from mypy.nodes import AssignmentStmt, IntExpr, ListExpr, NameExpr, StrExpr, TypeInfo, is_class_var
from mypy.plugin import Plugin


class CustomPlugin(Plugin):
    metadata = {

    }
    def get_customize_class_mro_hook(self, fullname: str):
        def analyze(classdef_ctx):
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
            
            print(1111, 'processing', classdef_ctx.cls.fullname)
            subsets, supersets = ListExpr(items=[]), ListExpr(items=[])
             
            for assign_stmt in classdef_ctx.cls.defs.body:
                if len(assign_stmt.lvalues) == 1 and assign_stmt.lvalues[0].name == '__subsets__':
                    subsets = assign_stmt.rvalue
                if len(assign_stmt.lvalues) == 1 and assign_stmt.lvalues[0].name == '__supersets__':
                    supersets = assign_stmt.rvalue

            for subset_name in subsets.items:
                res = classdef_ctx.api.lookup_qualified(subset_name.name, classdef_ctx).node
                res.mro.insert(1, classdef_ctx.cls.info)

            for superset_name in supersets.items:
                res = classdef_ctx.api.lookup_qualified(superset_name.name, classdef_ctx).node
                classdef_ctx.cls.info.mro.insert(1, res)

            classdef_ctx.cls.defs.body.append(AssignmentStmt(
                lvalues=[NameExpr(name='DJANGO')],
                rvalue=StrExpr('asd')
            ))            
           
                
        # see explanation below
        return analyze

def plugin(version: str):
    # no version restrictions yet
    return CustomPlugin