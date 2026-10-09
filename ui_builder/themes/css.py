"""CSS gabungan: ikon, gaya semua komponen bar (preview & ekspor), dan tampilan editor.

Potongan CSS per paket ada di components/css/ (core, extra, pro, addons) dan efek kaca
ada di themes/glass.py. Berkas ini hanya menyusunnya dalam urutan yang sama seperti dulu.
"""
from ui_builder.components.css.addons import BAR_CSS_ADDONS
from ui_builder.components.css.core import BAR_CSS_CORE
from ui_builder.components.css.extra import BAR_CSS_EXTRA
from ui_builder.components.css.pro import BAR_CSS_PRO
from ui_builder.themes.glass import APP_CSS_GLASS, GLASS_PAGE_CSS

ICON_LINK = (
    '<link rel="preconnect" href="https://fonts.googleapis.com">'
    '<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Material+Symbols+Rounded:'
    'opsz,wght,FILL,GRAD@24,400,0..1,0">'
)

# Urutan penyusunan: inti -> tambahan lama -> Pro -> tambahan terbaru.
BAR_CSS = BAR_CSS_CORE + BAR_CSS_EXTRA + BAR_CSS_PRO + BAR_CSS_ADDONS

# Tampilan aplikasi editor Streamlit (glassmorphism). Definisinya di themes/glass.py
# supaya mudah disetel ulang lewat token --g-* (blur, warna kaca, garis tepi, bayangan).
APP_CSS = APP_CSS_GLASS

__all__ = ["APP_CSS", "BAR_CSS", "GLASS_PAGE_CSS", "ICON_LINK"]
