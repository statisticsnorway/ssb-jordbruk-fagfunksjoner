"""Uses a registry pattern to build the Produksjonstilskudd codelist based on all currently created Produksjonskode objects, as they add themselves to the _PRODUKSJONSKODER_REGISTRY list as they are created.
"""

import re

_PRODUKSJONSKODER_REGISTRY: list["Produksjonskode"] = []

VALID_MEASUREMENT_UNITS = {"antall", "dekar"}


class Produksjonstilskudd:
    def __init__(self) -> None:
        self.codes = _PRODUKSJONSKODER_REGISTRY

        categories = set()
        for code in self.codes:
            for group in code.groups:
                categories.add(group)
        self.categories = list(sorted(categories))

    def get_codes(self, categories=None):
        if categories is None:
            categories = self.categories
        if isinstance(categories, str):
            categories = [categories]
        if not isinstance(categories, list):
            raise TypeError(
                f"Received object of type {type(categories)}, expected type str or list."
            )

        relevant_codes = []
        for code in self.codes:
            if any(group in categories for group in code.groups):
                relevant_codes.append(code)
        return relevant_codes

    def __str__(self):
        return f"Produksjonstilskudd object with {len(self.codes)} Produksjonskoder registered."


class Produksjonskode:
    def __init__(
        self,
        code,
        label,
        groups,
        measured_in,
        description=None,
        valid_from=None,
        valid_to=None,
        replaces=None,
        replaced_by=None,
    ):
        if not re.fullmatch(r"\d{3}", code):  # Checks that the code is 3 digits.
            raise ValueError(
                f"Invalid code: {code}. Must be exactly 3 digits (e.g., '101')."
            )

        if not isinstance(groups, list):
            raise TypeError(f"Invalid type: {type(groups)}. groups must be a list")

        _invalid_values = [value for value in groups if not isinstance(value, str)]
        if _invalid_values:
            raise ValueError(
                f"All values in groups must be strings. Invalid values: {_invalid_values}"
            )

        if measured_in not in VALID_MEASUREMENT_UNITS:
            raise ValueError(
                f"Invalid measurement unit: {measured_in}. Must be one of {VALID_MEASUREMENT_UNITS}"
            )

        self.code = code
        self.label = label
        self.description = description if description else None
        self.valid_from = valid_from if valid_from else None
        self.valid_to = valid_to if valid_to else None
        self.replaces = replaces if replaces else []
        self.replaced_by = replaced_by if replaced_by else []
        self.groups = groups if groups else []
        self.measured_in = measured_in

        _PRODUKSJONSKODER_REGISTRY.append(self)  # Registers itself in the registry

    def __str__(self):
        """Returns a human-readable string representation of the object."""
        return (
            f"Produksjonskode:\n"
            f"  Code: {self.code}\n"
            f"  Label: {self.label}\n"
            f"  Valid From: {self.valid_from}\n"
            f"  Valid To: {self.valid_to if self.valid_to else 'N/A'}\n"
            f"  Replaces: {', '.join(self.replaces) if self.replaces else 'None'}\n"
            f"  Replaced By: {', '.join(self.replaced_by) if self.replaced_by else 'None'}\n"
            f"  Groups: {', '.join(self.groups) if self.groups else 'None'}\n"
            f"  Measured In: {self.measured_in if self.measured_in else 'N/A'}"
        )

    def __repr__(self):
        """Returns a detailed string representation for debugging."""
        return (
            f"Produksjonskode("
            f"code={self.code!r}, label={self.label!r}, "
            f"valid_from={self.valid_from!r}, valid_to={self.valid_to!r}, "
            f"replaces={self.replaces!r}, replaced_by={self.replaced_by!r}, "
            f"groups={self.groups!r}, measured_in={self.measured_in!r})"
        )


Produksjonskode(
    code="001",
    label="Epler",
    description="avling av epler",
    groups=["Frukt", "Frukt avling"],
    measured_in="antall",
)


Produksjonskode(
    code="272",
    label="Epler",
    description="Areal med epler",
    groups=["Frukt", "Frukt areal"],
    measured_in="dekar",
)

print(Produksjonstilskudd())

print(Produksjonstilskudd().categories)

print("get_codes testing")
print(1)
print(Produksjonstilskudd().get_codes())
print(2)
print(Produksjonstilskudd().get_codes("Frukt"))
print(3)
print(Produksjonstilskudd().get_codes("Frukt avling"))
