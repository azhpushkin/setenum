from mypy.nodes import AssignmentExpr, AssignmentStmt, Block, ClassDef, IntExpr, ListExpr, NameExpr, StrExpr, SymbolTable, TupleExpr, TypeInfo, is_class_var
from mypy.plugin import ClassDefContext, Plugin

import copy


class CustomTypeInfo(TypeInfo):
    def get(self, name: str):
        print("CUSTOM CALLED YAHOO!!", name)
        for cls in self.mro:
            n = cls.names.get(name)
            if n:
                return n
        return None


def asd(ctx: ClassDefContext):
    defn = ctx.cls

    print('OLD TABLE IN CLASS', ctx.api.current_symbol_table())
    ctx.api.leave_class()
    # Unlink classdef from old_info
    old_info = ctx.cls.info
    old_info.defn = ClassDef(ctx.cls.name + '_OLD', defs=Block([]))
    old_info._fullname = old_info.defn.name
    print('OLD INFO', old_info)
    print('OLD TABLE', ctx.api.current_symbol_table())
    table = ctx.api.current_symbol_table()
    table.pop(ctx.cls.name)
    print('!!!', table.keys())

    
    
    
    new_info = CustomTypeInfo(SymbolTable(), defn, ctx.api.cur_mod_id)
    
    defn.info = new_info
    new_info.defn = defn
    new_info._fullname = new_info.name

    

    base_types, _ = ctx.api.analyze_base_classes(defn.base_type_exprs)

    ctx.api.add_symbol(defn.name, defn.info, defn)
    
    print('NEW TABLE', ctx.api.current_symbol_table())
    defn.info.type_vars = [tvar.name for tvar in defn.type_vars]
    
    
    
    with ctx.api.scope.class_scope(defn.info):
        ctx.api.configure_base_classes(defn, base_types)
        ctx.api.analyze_metaclass(defn)
        
        ctx.api.enter_class(defn.info)

        # Reset defs body to make sure accept() will process them again
        for item in defn.defs.body:
            item.lvalues[0].node = None
            
        defn.defs.accept(ctx.api)
        ctx.api.leave_class()
    
    print('NEW TABLE AFTER WITH', ctx.api.current_symbol_table())
    print('!!! TYPE', new_info)
    ctx.api.enter_class(new_info)
    print('NEW TABLE IN CLASS', ctx.api.current_symbol_table())
    print(ctx.cls.defs.body)


    

class CustomPlugin(Plugin):
    def get_base_class_hook(self, fullname: str):
        if fullname == 'setenum.SetEnum':
            return asd


class X:

    # def get_base_class_hook(self, fullname: str):
    #     def analyze(asd):
    #         print(123, asd.cls.info)

    #     if fullname == 'setenum.SetEnum':
    #         return analyze
    
    # def get_attribute_hook(self, fullname: str):
    #     print('<<<<', fullname)
    #     return None

    # def get_type_analyze_hook(self, fullname):    
        
    #     def asd(ctx):
    #         print('>>>>', ctx.type, type(ctx.type))
            
    #         t = ctx.type
    #         sym = ctx.api.lookup_qualified(t.name, t)

    #         return ctx.api.analyze_type_with_type_info(sym.node, t.args, t)

    #     if fullname.startswith('setenum'):
    #         return asd

    
    def get_customize_class_mro_hook(self, fullname: str):
        def analyze(classdef_ctx):
            if fullname == "example_test.X":
                return
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

            # for superset_name in supersets.items:
            #     res = classdef_ctx.api.lookup_qualified(superset_name.name, classdef_ctx).node
            #     classdef_ctx.cls.info.mro.insert(1, res)

                # for assign in self.metadata[classdef_ctx.cls.fullname]:
                #     res.defn.defs.body.append(AssignmentStmt(
                #         lvalues=[NameExpr(name='DJANGO')],
                #         rvalue=assign.rvalue
                #     ))

                # print('!!11', classdef_ctx.cls.info)
                # print('!!22', res.names.values(), type(res.names))
                

            
            # MRO is modified BEFORE class initialization, but modifying this shit afterwards is useless
            # we need to use something else, e.g. from this part:
            # https://github.com/python/mypy/blob/8296a3123a1066184a6c5c4bc54da1ff14983c56/mypy/semanal.py#L1157
            # TODO: try to use 
            
            print(111, fullname, classdef_ctx.cls.info.mro)
            print('############')
           
                
        # see explanation below
        return analyze

def plugin(version: str):
    # no version restrictions yet
    return CustomPlugin