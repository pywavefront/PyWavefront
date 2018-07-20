"""
Parser and metadata handler for cached binary versions of obj files
"""
import gzip
import json
import logging
import os
import struct
from datetime import datetime

from pywavefront.material import Material, MaterialParser

logger = logging.getLogger("pywavefront")


def cache_name(file_name):
    """Generate the name of the binary cache file"""
    return "{}.bin".format(file_name)


def meta_name(file_name):
    """Generate the name of the meta file"""
    return "{}.json".format(file_name)


class CacheLoader(object):
    material_parser_cls = MaterialParser

    def __init__(self, file_name, wavefront, strict=False, create_materials=False, encoding='utf-8', parse=True, **kwargs):
        self.wavefront = wavefront
        self.file_name = file_name
        self.encoding = encoding
        self.create_materials = create_materials
        self.strict = strict
        self.dir = os.path.dirname(file_name)
        self.meta = None

    def parse(self):
        # Load materials
        if not os.path.exists(meta_name(self.file_name)) or not os.path.exists(cache_name(self.file_name)):
            logger.info("%s has no cache files", self.file_name)
            return False

        logger.info("%s loading cached version", self.file_name)

        self.meta = Meta.from_file(meta_name(self.file_name))
        self._parse_materials()
        self._load_vertex_buffers()

        return True

    def _load_vertex_buffers(self):
        """Load each vertex buffer into each material"""
        fd = gzip.open(cache_name(self.file_name), 'rb')

        for buff in self.meta.vertex_buffers:

            mat = self.wavefront.materials.get(buff['material'])
            if not mat:
                mat = Material(name=buff['material'], is_default=True)
                self.wavefront.materials[mat.name] = mat

            mat.vertex_format = buff['vertex_format']
            mat.vertices = struct.unpack('{}f'.format(buff['byte_length'] // 4), fd.read(buff['byte_length']))

        fd.close()

    def _parse_materials(self):
        """Load mtl files"""
        for mtl_file in self.meta.materials:
            mtllib = mtl_file
            try:
                materials = self.material_parser_cls(mtllib, encoding=self.encoding, strict=self.strict).materials
            except IOError:
                if self.create_materials:
                    return
                raise

            for name, material in materials.items():
                self.wavefront.materials[name] = material


class CacheWriter(object):

    def __init__(self, file_name, wavefront, meta):
        self.file_name = file_name
        self.wavefront = wavefront
        self.meta = meta

    def write(self):
        logger.info("%s creating cache", self.file_name)

        offset = 0
        fd = gzip.open(cache_name(self.file_name), 'wb')

        for mat in self.wavefront.materials.values():

            if len(mat.vertices) == 0:
                continue

            self.meta.add_vertex_buffer(
                mat.name,
                mat.vertex_format,
                offset,
                len(mat.vertices) * 4,
            )
            offset += len(mat.vertices) * 4
            fd.write(struct.pack('{}f'.format(len(mat.vertices)), *mat.vertices))

        fd.close()
        self.meta.write(meta_name(self.file_name))


class Meta(object):
    """
    Metadata for binary obj cache files
    """
    format_version = "0.1"

    def __init__(self, **kwargs):
        self._materials = kwargs.get('materials') or []
        self._vertex_buffers = kwargs.get('vertex_buffers') or []
        self._version = kwargs.get('version') or self.format_version
        self._created_at = kwargs.get('created_at') or datetime.now().isoformat()

    def add_vertex_buffer(self, material, vertex_format, byte_offset, byte_length):
        """Add a vertex buffer"""
        self._vertex_buffers.append({
            "material": material,
            "vertex_format": vertex_format,
            "byte_offset": byte_offset,
            "byte_length": byte_length,
        })

    def add_material(self, material):
        """Add an mtl material file name"""
        self._materials.append(material)

    @classmethod
    def from_file(cls, path):
        with open(path, 'r') as fd:
            data = json.loads(fd.read())

        return cls(**data)

    def write(self, path):
        """Save the metadata as json"""
        with open(path, 'w') as fd:
            fd.write(json.dumps(
                {
                    "created_at": self._created_at,
                    "version": self._version,
                    "materials": self._materials,
                    "vertex_buffers": self._vertex_buffers,
                },
                indent=2,
            ))

    @property
    def version(self):
        return self._version

    @property
    def created_at(self):
        return self._created_at

    @property
    def vertex_buffers(self):
        return self._vertex_buffers
    
    @property
    def materials(self):
        return self._materials
