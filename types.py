import torch
import enum
from typing import List, Tuple, Optional, Dict

# TSAllType := TSType | TSModuleType
# 
# TSType := TSMultiType | TSPrimitiveType | TSStructuralType | 
#           TSBuiltinNominalType | TSCustomNominalType
# TSModuleType := "torch.nn.Module" and subclasses
# 
# TSMultiType := "Any"
# TSPrimitiveType := "int" | "float" | "double" | "bool" | "str" | NoneType
# TSStructualType :=  TSTuple | TSList | TSDict | TSOptional | TSFuture |
#                     TSRRef
# TSBuiltinNominalType := TSTensor | "torch.collections.namedtuple" | 
#                   "torch.device" | "torch.stream" | "torch.dtype" | 
#                   "torch.nn.ModuleList" | "torch.nn.ModuleDict" | ...
# TSCustomNominalType := TSEnum | TSClass | TSInterface
# 
# TSTuple := "Tuple" "[" (TSType ",")+ "]"
# TSList := "List" "[" TSType "]"
# TSOptional := "Optional" "[" TSType "]"
# TSFuture := "Future" "[" TSType "]"
# TSRRef := "RRef" "[" TSType "]"
# TSDict := "Dict" "[" KeyType "," TSType "]"
# KeyType := "str" | "int" | "float" | "bool" | TSTensor| "Any"
# 
# TSTensor := "torch.tensor" and subclasses
# TSInterface := classes w/ attr "____torch_script_interface__"


class TSTypes:

    @staticmethod
    def TSAllType(nest_depth):
        res = []
        res.extend(TSTypes.TSType(nest_depth))
        res.extend(TSTypes.TSModuleType(nest_depth))
        return res

    @staticmethod
    def TSModuleType(nest_depth):
        # TODO: Use a dummy module for testing
        return ["torch.nn.Module"]

    @staticmethod
    def TSType(nest_depth):
        res = []
        res.extend(TSTypes.TSMultiType())
        res.extend(TSTypes.TSPrimitiveType())
        res.extend(TSTypes.TSStructuralType(nest_depth))
        res.extend(TSTypes.TSBuiltinNominalType())
        res.extend(TSTypes.TSCustomNominalType())
        return res

    @staticmethod
    def TSMultiType():
        return ["Any"]

    @staticmethod
    def TSBuiltinNominalType():
        res = []
        res.extend(TSTypes.TSTensor())
        res.append("torch.collections.namedtuple")
        res.append("torch.device")
        res.append("torch.stream")
        res.append("torch.dtype")
        res.append("torch.nn.ModuleList")
        res.append("torch.nn.ModuleDict")
        return res

    @staticmethod
    def TSTensor():
        return ["torch.Tensor"]

    @staticmethod
    def TSCustomNominalType():
        res = []
        res.extend(TSTypes.TSEnum())
        res.extend(TSTypes.TSClass())
        res.extend(TSTypes.TSInterface())
        return res

    @staticmethod
    def TSEnum():
        # TODO: Add a derived enum for testing
        return ["enum.Enum"]

    @staticmethod
    def TSClass():
        # TODO: Add a JIT class for testing
        return []

    @staticmethod
    def TSInterface():
        # TODO: Add an interface for testing
        return []

    @staticmethod
    def TSPrimitiveType():
        # TODO: How to express None type?
        return ["int", "float", "double", "bool", "str"]

    @staticmethod
    def TSStructuralType(nest_depth):
        res = []
        res.extend(TSTypes.TSTuple(nest_depth))
        res.extend(TSTypes.TSList(nest_depth))
        res.extend(TSTypes.TSDict(nest_depth))
        res.extend(TSTypes.TSOptional(nest_depth))
        res.extend(TSTypes.TSFuture(nest_depth))
        res.extend(TSTypes.TSRRef(nest_depth))
        return res

    def TSTuple(nest_depth):
        if nest_depth == 0:
            return []
        else:
            nest_depth = nest_depth - 1

        # TODO: Here we are testing Tuple of only 1 element, which is same as
        # multiple-element tuples in theory.
        res = []
        for t in TSTypes.TSType(nest_depth):
            res.append("Tuple[" + t + "]")
        return res

    def TSList(nest_depth):
        if nest_depth == 0:
            return []
        else:
            nest_depth = nest_depth - 1

        res = []
        for t in TSTypes.TSType(nest_depth):
            res.append("List[" + t + "]")
        return res


    def TSOptional(nest_depth):
        if nest_depth == 0:
            return []
        else:
            nest_depth = nest_depth - 1

        res = []
        for t in TSTypes.TSType(nest_depth):
            res.append("Optional[" + t + "]")
        return res

    def TSFuture(nest_depth):
        # TODO: Future is not supported yet
        return []

    def TSRRef(nest_depth):
        # TODO: RRef is not supported yet
        return []

    def TSDict(nest_depth):
        if nest_depth == 0:
            return []
        else:
            nest_depth = nest_depth - 1

        res = []
        for k in TSTypes.TSKeyType():
            for v in TSTypes.TSType(nest_depth):
                res.append("Dict[" + k + ", " + v + "]")
        return res

    def TSKeyType():
        res = ["str", "int", "floatl", "bool", "Any"]
        res.extend(TSTypes.TSTensor())
        return res
	
for t in TSTypes.TSAllType(nest_depth=2):
    print(t)
