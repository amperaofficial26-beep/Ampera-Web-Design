"""Spesifikasi 170 komponen bar, digabung dari empat paket.

Pintu masuk: from ui_builder.components.specs import BAR_SPECS

Urutan penggabungan (sama seperti sebelumnya):
1. inti              - core.py   (20 komponen)
2. tambahan lama     - extra.py  (50 komponen)
3. Pro               - pro.py    (50 komponen)
4. tambahan terbaru  - addons.py (50 komponen)

Konstanta bersama (GROUP_ORDER, STATUS_KINDS, dst.) ada di common.py dan
diekspor ulang di sini, sehingga impor lama dari bar_specs tetap bisa dipakai.
"""
from ui_builder.components.specs.addons import COMPONENT_BAR_SPECS
from ui_builder.components.specs.common import (
    ALIGN_KINDS, GROUP_ORDER, ICON_HINT, INPUT_KIND_LIST, PLAY_KINDS,
    STATUS_ICONS, STATUS_KINDS, STOCK_KINDS, VIEW_KINDS,
)
from ui_builder.components.specs.core import CORE_BAR_SPECS
from ui_builder.components.specs.extra import EXTRA_BAR_SPECS
from ui_builder.components.specs.pro import PRO_BAR_SPECS, PRO_GROUP_ORDER

__all__ = [
    "ALIGN_KINDS", "BAR_SPECS", "COMPONENT_BAR_SPECS", "GROUP_ORDER", "ICON_HINT",
    "INPUT_KIND_LIST", "PLAY_KINDS", "STATUS_ICONS", "STATUS_KINDS", "STOCK_KINDS",
    "VIEW_KINDS",
]

# Urutan sama seperti versi sebelumnya: inti + tambahan lama, lalu Pro, lalu terbaru.
BAR_SPECS = {**CORE_BAR_SPECS, **EXTRA_BAR_SPECS}
BAR_SPECS.update(PRO_BAR_SPECS)
for _group in PRO_GROUP_ORDER:
    if _group not in GROUP_ORDER:
        GROUP_ORDER.append(_group)
# Tambahan baru bersifat aditif: komponen lama dan paket Pro tetap tersedia.
BAR_SPECS.update(COMPONENT_BAR_SPECS)
del _group
