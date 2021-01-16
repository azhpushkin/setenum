from mypy.nodes import AssignmentExpr, AssignmentStmt, IntExpr, ListExpr, NameExpr, StrExpr, TupleExpr, TypeInfo, is_class_var
from mypy.plugin import Plugin

import copy


class CustomPlugin(Plugin):
    metadata = {}

    def get_base_class_hook(self, fullname: str):
        def analyze(asd):
            print(123, asd.cls.name)q

        if fullname == 'setenum.SetEnumMeta':
            return analyze
    
    def get_metaclass_hook(self, fullname: str):
        # print(333, fullname)
        return None
    
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
            
            self.metadata[classdef_ctx.cls.fullname] = []

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
                else:
                    self.metadata[classdef_ctx.cls.fullname].append(assign_stmt)

            for subset_name in subsets.items:
                res: TypeInfo = classdef_ctx.api.lookup_qualified(subset_name.name, classdef_ctx).node
                res.mro.insert(1, classdef_ctx.cls.info)

                # TODO: why copy is not working?
                for assign in self.metadata[res.defn.fullname]:
                    classdef_ctx.cls.defs.body.append(AssignmentStmt(
                        lvalues=[NameExpr(name=assign.lvalues[0].name)],
                        rvalue=assign.rvalue
                    ))

            for superset_name in supersets.items:
                res = classdef_ctx.api.lookup_qualified(superset_name.name, classdef_ctx).node
                classdef_ctx.cls.info.mro.insert(1, res)

                # for assign in self.metadata[classdef_ctx.cls.fullname]:
                #     res.defn.defs.body.append(AssignmentStmt(
                #         lvalues=[NameExpr(name='DJANGO')],
                #         rvalue=assign.rvalue
                #     ))
                

            
            # MRO is modified BEFORE class initialization, but modifying this shit afterwards is useless
            # we need to use something else, e.g. from this part:
            # https://github.com/python/mypy/blob/8296a3123a1066184a6c5c4bc54da1ff14983c56/mypy/semanal.py#L1157
            # TODO: try to use 
            
                
        # see explanation below
        return analyze

def plugin(version: str):
    # no version restrictions yet
    return CustomPlugin