from ... import compat_attr as attr

REQUIRED_VERSION = "0.2"


@attr.s()
class StagingFileMetadata(object):
    attributes = attr.ib(type=dict)
    filename = attr.ib(type=str)
    relative_path = attr.ib(type=str)
    sha256sum = attr.ib(type=str)


@attr.s()
class StagingMetadata(object):
    # A private class modelling the content of staging metadata files

    # Filename from which metadata was loaded.
    filename = attr.ib(type=str, default=None)

    # Metadata per file, keyed by relative path within staging area
    file_metadata = attr.ib(type=dict, default=attr.Factory(dict))

    @classmethod
    def from_data(cls, data, filename="<unknown file>"):
        header = data.get("header") or {}
        version = str(header.get("version"))

        # TODO: make a jsonschema and then validate it here.

        # Currently the only supported version...
        if version != REQUIRED_VERSION:
            raise ValueError(
                "%s has unsupported version (has: %s, required: %s)"
                % (filename, version, REQUIRED_VERSION)
            )

        payload = data.get("payload") or {}
        files = payload.get("files") or []
        file_metadata = {}

        for entry in files:
            md = StagingFileMetadata(
                attributes=entry.get("attributes") or {},
                filename=entry.get("filename"),
                relative_path=entry["relative_path"],
                sha256sum=entry["sha256sum"],
            )
            if md.relative_path in file_metadata:
                raise ValueError(
                    "File %s listed twice in %s" % (md.relative_path, filename)
                )
            file_metadata[md.relative_path] = md

        return cls(filename=filename, file_metadata=file_metadata)


@attr.s()
class StagingLeafDir(object):
    # A private class modelling a leaf directory within a staging area.
    file_type = attr.ib(type=str)
    dest = attr.ib(type=str)
    path = attr.ib(type=str)
