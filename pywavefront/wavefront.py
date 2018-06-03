from pywavefront import ObjParser


class Wavefront(object):
    # Can be used to override the parser when extending the class
    parser_cls = ObjParser

    """Import a wavefront .obj file."""
    def __init__(self, file_name, strict=False, encoding="utf-8", parse=True):
        """
        Create a Wavefront instance
        :param file_name: file name and path of obj file to read
        :param strict: Enable strict mode
        :param parse: Should parse be called immediately or manually called later?
        """
        self.file_name = file_name

        self.materials = {}
        self.meshes = {}        # Name mapping
        self.mesh_list = []     # Also includes anonymous meshes

        self.parser = self.parser_cls(self, self.file_name, strict=strict, encoding=encoding, parse=parse)

    def parse(self):
        """Manually call the parser. This is used when parse=False"""
        self.parser.parse()

    def add_mesh(self, the_mesh):
        self.mesh_list.append(the_mesh)
        self.meshes[the_mesh.name] = the_mesh
