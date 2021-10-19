class ORMException(Exception):
    def __init__(self, message: str = None):
        self.message = message
        super(ORMException, self).__init__(self.message)


class ResourceNotExists(ORMException):
    def __init__(self, rsc: str, all_rscs: list):
        self.message = f"resource '{rsc}' doesn't exist. "\
                       f"available resources are {', '.join(all_rscs)}"
        super().__init__(self.message)


class ResourceInstanceNotFound(ORMException):
    def __init__(self, rsc_mod, rsc_ins_id: int):
        self.model = rsc_mod
        self.rsc = rsc_mod.__tablename__
        self.rsc_ins_id = rsc_ins_id
        self.message = f"'{self.rsc}' {self.rsc_ins_id} is not found"
        super().__init__(self.message)


class ResourceInstanceExisted(ORMException):
    def __init__(self):
        self.message = "resource instance already exists"
        super(ResourceInstanceExisted, self).__init__(self.message)


class ResourceAttributeNotExists(ORMException):
    def __init__(self, rsc: str, att: str, all_att: list[str]):
        self.message = f"resource {rsc} doesn't have attribute {att}. all attributes of {rsc} are {', '.join(all_att)}"
        super(ResourceAttributeNotExists, self).__init__(self.message)


class RelatedResourceNotFound(ORMException):
    def __init__(self, rsc_mod, rel_rsc: str):
        self.rsc_mod = rsc_mod
        self.rsc = rsc_mod.__tablename__
        self.rel_rsc = rel_rsc
        self.all_rel_rsc = [a for a in rsc_mod.__dict__.keys() if a[:1] != '_']
        self.message = f"'{self.rsc}' resource doesn't have related resource '{self.rel_rsc}'. " \
                       f"all related resource are {', '.join(self.all_rel_rsc)}"
        super().__init__(self.message)


class RelatedResourceInstanceNotFound(ORMException):
    def __init__(self, rsc_ins, rel_rsc: str, rel_rsc_id: int):
        self.rsc_ins = rsc_ins
        self.rsc_mod = type(rsc_ins)
        self.rsc = self.rsc_mod.__tablename__
        self.rel_rsc = rel_rsc
        self.rel_rsc_id = rel_rsc_id
        self.message = f"'{self.rsc}' {self.rsc_ins.id} " \
                       f"doesn't have related resource '{self.rel_rsc}' {rel_rsc_id}."
        super().__init__(self.message)


class RequireAdmin(ORMException):
    def __init__(self):
        self.message = "require role admin"
        super(RequireAdmin, self).__init__(self.message)


class RequireGroupAdmin(ORMException):
    def __init__(self):
        self.message = "require role group admin"
        super(RequireGroupAdmin, self).__init__(self.message)


class RequireHandler(ORMException):
    def __init__(self):
        self.message = "require role handler"
        super(RequireHandler, self).__init__(self.message)


class RequireOwnership(ORMException):
    def __init__(self):
        self.message = "require ownership"
        super(RequireOwnership, self).__init__(self.message)


class ResourceCantSearchByName(ORMException):
    def __init__(self, rsc: str):
        self.rsc = rsc
        self.message = f"resource {rsc} can not search by name"
        super(ResourceCantSearchByName, self).__init__(self.message)


class IndelibleResourceInstance(ORMException):
    def __init__(self):
        self.message = "resource instance's indelible"
        super(IndelibleResourceInstance, self).__init__(self.message)


# raise NotRelatedResource(Model.User, 'abc')
# raise RelatedResourceNotFound('abc')
