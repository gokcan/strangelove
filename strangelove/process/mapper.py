class Mapper:
    @staticmethod
    def to_numeric_integer(input: list):
        """Maps any value list(str|int) to incremental numeric ids"""
        map_csr = []

        set_csr = set(input)
        for index, value in enumerate(set_csr):
            assert isinstance(value, (int, str))
            map_csr.append((value, index))

        # cache numeric values into map
        map_inverse =  dict((v, k) for k, v in map_csr)
        map_origin = dict(map_csr)
        return (map_inverse, map_origin, list([float(map_origin[value]) for value in input]))