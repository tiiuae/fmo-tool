import logging

from copy import deepcopy
from enum import IntFlag
from typing import Dict
from types import NoneType

logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO)


class FMO_Options(IntFlag):
    MANDATORY = 0x00
    OPTIONAL = 0x01
    CANNOT_BE_CREATED = 0x02
    READ_ONLY = 0x04
    SET_OF_VALS = 0x08
    LIST_OF_VALS = 0x10


class FMO_Annotation(object):
    def __init__(self, T, v, options=FMO_Options.MANDATORY, validator=None):
        self._T = type(T)
        self._v = v
        self._options = options
        self._validator = validator

    @property
    def T(self):
        return self._T

    @property
    def options(self):
        return self._options

    @property
    def validator(self):
        return self._validator

    @property
    def v(self):
        return self._v

#    def __str__(self):
#        return f"Annotation[T: {self.T} v: {self.v} opts: {self.options} val: {self.validator}]"

#    def __repr__(self):
#        return f"Annotation[T: {self.T} v: {self.v} opts: {self.options} val: {self.validator}]"


hyperMonitoringService = {
    'enable':  FMO_Annotation(bool(), bool(), FMO_Options.MANDATORY),
}

hyperDDPService = {
    'enable':  FMO_Annotation(bool(), bool(), FMO_Options.MANDATORY),
    # TODO: Need to be able to validate lists of paramiters )
    'devices': [],
}

hyperDPFService = {
    'enable':  FMO_Annotation(bool(), bool(), FMO_Options.MANDATORY),
    'ipaddress': "",
    'ipaddress-path': "",
    'config-path': "",
    # TODO: Need to be able to validate lists of paramiters )
    'configuration': [],
}

hyperDCIService = {
    'enable':  FMO_Annotation(bool(), bool(),
                              FMO_Options.MANDATORY | FMO_Options.READ_ONLY),
    'backup-path': "",
    'compose-path': "",
    'docker-url': "",
    'docker-url-path': "",
    'pat-path': "",
    'preloaded-images': "",
    'update-path': "",
    'docker-mtu': 1500,
}

hyperConfigServices = {
    'dynamic-portforwarding-service': FMO_Annotation({}, hyperDPFService,
                                                     FMO_Options.OPTIONAL),
    'monitoring-service': FMO_Annotation({}, hyperMonitoringService,
                                         FMO_Options.OPTIONAL),
    'fmo-dynamic-device-passthrough': FMO_Annotation({}, hyperDDPService,
                                                     FMO_Options.OPTIONAL),
    'fmo-dci': FMO_Annotation({}, hyperDCIService, FMO_Options.OPTIONAL),
}

hyperConfigExtraModules = {
    'services': FMO_Annotation({}, hyperConfigServices, FMO_Options.OPTIONAL),
}

hyperConfigVM = {
    'name':  FMO_Annotation("", "", FMO_Options.READ_ONLY),
    'ipaddr':  FMO_Annotation("", "", FMO_Options.READ_ONLY),
    'extraModules': FMO_Annotation({}, hyperConfigExtraModules,
                                   FMO_Options.OPTIONAL),
}

hyperConfigFMOSystem = {
    'alias': "",
    'ipaddr': "",
    'defaultGW': "",
    'dockerCR': "",
    'RAversion': "",
}

hyperConfigSystem = {
    'name': FMO_Annotation("", "", FMO_Options.READ_ONLY),
    'release': FMO_Annotation("", "", FMO_Options.READ_ONLY),
    'vms': FMO_Annotation({}, hyperConfigVM,
                          FMO_Options.OPTIONAL | FMO_Options.SET_OF_VALS),
    'fmo-system': FMO_Annotation({}, hyperConfigFMOSystem,
                                 FMO_Options.MANDATORY),
}


def is_fmo_annotation(v):
    return isinstance(v, FMO_Annotation)


def is_fmo_annotation_optional(v):
    if not is_fmo_annotation(v):
        return False
    return bool(v.options & FMO_Options.OPTIONAL)


def is_fmo_annotation_object(v):
    if not is_fmo_annotation(v):
        return False
    return v.T is dict


def is_fmo_annotation_set_of_vals(v):
    if not is_fmo_annotation(v):
        return False
    return bool(get_fmo_annotation_options(v) &
                FMO_Options.SET_OF_VALS)


def is_fmo_annotation_has_validator(v):
    if not is_fmo_annotation(v):
        return False
    return v.validator is not None


def get_fmo_annotation_validator(v):
    if not is_fmo_annotation(v):
        return None
    return v.validator


def get_fmo_annotation_type(v):
    if not is_fmo_annotation(v):
        return NoneType
    return v.T


def get_fmo_annotation_options(v):
    if not is_fmo_annotation(v):
        return 0x00
    return v.options


class FMO_Schema(object):
    __parent = None
    __config: Dict = None
    __schema: Dict = None
    __set_of_params_field = None

    def __init__(self, config: Dict,
                 schema_init: Dict = hyperConfigSystem,
                 parent=None, parent_field=None, set_of_params_field=None):
        self.__config = config
        self.__schema = deepcopy(schema_init)
        self.__parent = parent
        self.__parent_field = parent_field
        self.__set_of_params_field = set_of_params_field

        self.__validate_config()

    def __validate_config_keywords(self, config_keys, schema_keys):
        if not config_keys:
            # TODO: is empty dict -- means no values set?
            return
        diff = config_keys - schema_keys
        if diff:
            raise Exception(f"Unknown config keys: {diff} "
                            f"Expected: {schema_keys}")

        unknowns = []
        diff = schema_keys - config_keys
        if diff:
            for d in diff:
                v = self.__schema[d]
                if not (is_fmo_annotation(v) and
                        is_fmo_annotation_optional(v)):
                    unknowns.append(d)
        if unknowns:
            raise Exception(
                f"Following mandatory keys have not been found: {unknowns}")

    def __validate_config_fields(self, config_keys, schema_keys):
        for k in config_keys:
            schm_val = self.__schema[k]
            conf_val = self.__config[k]
            is_object = is_fmo_annotation_object(schm_val)
            is_annotation = is_fmo_annotation(schm_val)
            is_set_of_vals = is_fmo_annotation_set_of_vals(schm_val)
            has_validator = is_fmo_annotation_has_validator(schm_val)
            schm_t = get_fmo_annotation_type(schm_val) \
                if is_annotation else type(schm_val)
            conf_t = type(conf_val)

            logger.debug(f"Check key: {k} schm_val: {schm_val} "
                         f"conf_val: {conf_val}")

            if conf_t is not schm_t:
                raise Exception(f"Types of key: '{k}' "
                                f"mismatch: '{conf_t}' expected: '{schm_t}'")

            if is_annotation and has_validator:
                valid = get_fmo_annotation_validator(schm_val)()
                if not valid:
                    raise Exception(f"Validation of key: {k} "
                                    f"with value: {conf_val} has failed")

            if is_annotation and is_object:
                new_opts = schm_val.options & ~FMO_Options.SET_OF_VALS
                new_schm = FMO_Annotation({}, schm_val.v,
                                          new_opts, schm_val.validator)
                dummy_annotation = dict.fromkeys(conf_val.keys(), new_schm)
                sinit = dummy_annotation if is_set_of_vals else schm_val.v
                try:
                    _ = FMO_Schema(config=conf_val,
                                   schema_init=sinit,
                                   parent=self, parent_field=k)
                except Exception as e:
                    raise Exception(f"Validation failed for '{k}'", *e.args)

    def __validate_config(self):
        logger.debug("Start validation")
        logger.debug(f"Schema:\n{self.__schema}")
        logger.debug(f"Config:\n{self.__config}")
        logger.debug(f"Parrent: {self.__parent}")

        config_keys = set(self.__config.keys())
        schema_keys = set(self.__schema.keys())

        self.__validate_config_keywords(config_keys, schema_keys)
        self.__validate_config_fields(config_keys, schema_keys)

    def __setitem__(self, key, item):
        key_t = type(item)
        schm_val = self.__schema.get(key)
        is_annotation = is_fmo_annotation(schm_val)
        schm_t = get_fmo_annotation_type(schm_val) \
            if is_annotation else type(schm_val)
        opt = get_fmo_annotation_options(schm_val) \
            if is_annotation else FMO_Options.MANDATORY

        if key not in self.__schema:
            raise KeyError(f"Key: '{key}' not in schema")

        if key_t != schm_t:
            raise KeyError(f"Unexpected key type: {key_t}, expected: {schm_t}")

        if opt & FMO_Options.READ_ONLY:
            raise KeyError(f"Value with key: {key} is readonly")

        # TODO: empty case, is it good to create all fields here?
        if len(self.__config) == 0:
            for k in self.__schema.keys():
                annotation = is_fmo_annotation(self.__schema[k])
                val = self.__schema[k].v if annotation else self.__schema[k]
                optional = is_fmo_annotation_optional(self.__schema[k]) \
                    if annotation else False
                if optional:
                    continue
                self.__config[k] = val

        self.__config[key] = item

        if self.__parent is None or self.__parent_field is None:
            return
        self.__parent[self.__parent_field] = self.__config

    def __getitem__(self, key):
        schm_val = self.__schema[key]
        conf_val = self.__config.get(key, {})
        is_object = is_fmo_annotation_object(schm_val)
        is_set_of_vals = is_fmo_annotation_set_of_vals(schm_val)
        set_of_vals = schm_val if is_set_of_vals else None

        if is_object:
            new_opts = schm_val.options & ~FMO_Options.SET_OF_VALS
            new_schm = FMO_Annotation({}, schm_val.v,
                                      new_opts, schm_val.validator)
            dummy_annotation = dict.fromkeys(conf_val.keys(), new_schm)
            sinit = dummy_annotation if is_set_of_vals else schm_val.v
            return FMO_Schema(conf_val,
                              sinit,
                              parent=self, parent_field=key,
                              set_of_params_field=set_of_vals)
        else:
            return self.__config[key]

#    def __repr__(self):
#        return repr(self.__config)

#    def __str__(self):
#        return str(self.__config)

    def __len__(self):
        return len(self.__config)

    def __iter__(self):
        return iter(self.__config)

    def keys(self):
        return self.__config.keys()

    def values(self):
        return self.__config.values()

    def get(self, key, default):
        try:
            return self[key]
        except KeyError:
            return default

    def get_config(self):
        self.__validate_config()
        return deepcopy(self.__config)
