from typing import Union, Optional, List

from flags import MessageType
from bson import ObjectId
from django.test import TestCase

from extutils.checker import arg_type_ensure, NonSafeDataTypeConverter, TypeCastingFailed


# noinspection PyTypeChecker
class TestArgTypeEnsure(TestCase):
    def test_normal_valid(self):
        i_out = "1"
        f_out = 7
        l_out = (8, 7)
        d_out = [[8, 7], [6, 5]]
        b_out = 1
        t_out = [8, 7]
        o_out = "5e8c08d00000000000000000"

        @arg_type_ensure
        def fn(i: int, f: float, l: list, d: dict, b: bool, t: tuple, o: ObjectId):
            nonlocal i_out, f_out, l_out, d_out, b_out, t_out, o_out

            i_out = i
            f_out = f
            l_out = l
            d_out = d
            b_out = b
            t_out = t
            o_out = o

        fn(i_out, f_out, l_out, d_out, b_out, t_out, o_out)

        self.assertEquals(1, i_out)
        self.assertEquals(7.0, f_out)
        self.assertListEqual([8, 7], l_out)
        self.assertDictEqual({8: 7, 6: 5}, d_out)
        self.assertEquals(True, b_out)
        self.assertTupleEqual((8, 7), t_out)
        self.assertEquals(ObjectId("5e8c08d00000000000000000"), o_out)

    def test_normal_fail(self):
        l_out = 7

        @arg_type_ensure
        def fn(l: list):
            nonlocal l_out

            l_out = l

        fn(l_out)

        self.assertEquals(7, l_out)

    def test_normal_optional(self):
        a1_out = 7
        a2_out = None
        a3_out = "7"

        @arg_type_ensure
        def fn(a1: Optional[str], a2: Optional[str], a3: Optional[str]):
            nonlocal a1_out, a2_out, a3_out

            a1_out = a1
            a2_out = a2
            a3_out = a3

        fn(a1_out, a2_out, a3_out)

        self.assertEquals("7", a1_out)
        self.assertEquals(None, a2_out)
        self.assertEquals("7", a3_out)

    def test_normal_union_match_first(self):
        l_out = 7

        @arg_type_ensure
        def fn(l: Union[int, str]):
            nonlocal l_out

            l_out = l

        fn(l_out)

        self.assertEquals(7, l_out)

    def test_normal_union_match_second(self):
        l_out = "7"

        @arg_type_ensure
        def fn(l: Union[int, str]):
            nonlocal l_out

            l_out = l

        fn(l_out)

        self.assertEquals("7", l_out)

    def test_normal_union_multi_match(self):
        a1_out = True
        a2_out = 5.5

        @arg_type_ensure
        def fn(a1: Union[int, str, bool], a2: Union[int, str, bool]):
            nonlocal a1_out, a2_out

            a1_out = a1
            a2_out = a2

        fn(a1_out, a2_out)

        self.assertEquals(True, a1_out)
        self.assertEquals(5, a2_out)

    def test_normal_union_not_match_castable(self):
        l_out = True

        @arg_type_ensure
        def fn(l: Union[int, str]):
            nonlocal l_out

            l_out = l

        fn(l_out)

        self.assertEquals(1, l_out)

    def test_normal_union_not_match_uncastable(self):
        l_out = [1]

        @arg_type_ensure(converter=NonSafeDataTypeConverter)
        def fn(l: Union[int, float]):
            nonlocal l_out

            l_out = l

        with self.assertRaises(TypeCastingFailed, msg=f"TypeCastingFailed not raised. Final output: {l_out}"):
            fn(l_out)

    def test_normal_flag(self):
        a1_out = 1
        a2_out = MessageType.LOCATION
        a3_out = "1"

        @arg_type_ensure
        def fn(a1: MessageType, a2: MessageType, a3: MessageType):
            nonlocal a1_out, a2_out, a3_out

            a1_out = a1
            a2_out = a2
            a3_out = a3

        fn(a1_out, a2_out, a3_out)

        self.assertEquals(MessageType.TEXT, a1_out)
        self.assertEquals(MessageType.LOCATION, a2_out)
        self.assertEquals("1", a3_out)
        
    def test_normal_nested_union(self):
        a1_out = "1"
        a2_out = [1]
        a3_out = 1

        @arg_type_ensure
        def fn(a1: Union[int, List[int]], a2: Union[int, List[int]], a3: Union[int, List[int]]):
            nonlocal a1_out, a2_out, a3_out

            a1_out = a1
            a2_out = a2
            a3_out = a3

        fn(a1_out, a2_out, a3_out)

        self.assertEquals(1, a1_out)
        self.assertEquals([1], a2_out)
        self.assertEquals(1, a3_out)

    def test_normal_union_prioritized_list(self):
        a1_out = "1"
        a2_out = [1]
        a3_out = 1

        @arg_type_ensure
        def fn(a1: Union[List[int], int], a2: Union[List[int], int], a3: Union[List[int], int]):
            nonlocal a1_out, a2_out, a3_out

            a1_out = a1
            a2_out = a2
            a3_out = a3

        fn(a1_out, a2_out, a3_out)

        self.assertEquals(1, a1_out)
        self.assertEquals([1], a2_out)
        self.assertEquals(1, a3_out)

    def test_nonsafe_fail(self):
        l_out = 7

        @arg_type_ensure(converter=NonSafeDataTypeConverter)
        def fn(l: list):
            nonlocal l_out

            l_out = l

        with self.assertRaises(TypeCastingFailed):
            fn(l_out)
